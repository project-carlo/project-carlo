"""The labeler's local HTTP server: a JSON API and the built UI, on loopback only.

Standard library only (`http.server`). There is no authentication, so the
server binds to 127.0.0.1 and refuses requests whose Host or Origin is not
local: that keeps other machines out, and stops a web page in the same browser
from reaching it through DNS rebinding or a cross-site form.

API:

- `GET  /api/config`                          mode, classifier version, default labeler
- `GET  /api/bulletins`                       the queue, with label statuses and progress
- `GET  /api/next?after=<parish>/<hash>&parish=<slug>&unlabeled_parishes=1`
                                              the next bulletin to label; with the flag,
                                              cycle the latest of parishes with no label yet
- `GET  /api/bulletins/<parish>/<hash>`       parish, churches, Gemini's output, the label,
                                              and that parish's other bulletins
- `GET  /api/bulletins/<parish>/<hash>/pdf`   the stored PDF Gemini read
- `PUT  /api/labels/<parish>/<hash>`          validate and save a label
"""

from __future__ import annotations

import json
import logging
import mimetypes
import os
import subprocess
from dataclasses import dataclass
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, unquote, urlsplit

from pdf_extract.blobstore import get_store
from pdf_extract.classifiers.gemini import GeminiClassifier
from pdf_extract.labeling.bulletins import (
    bulletin_detail,
    find_bulletin,
    list_bulletins,
    next_bulletin,
    parish_bulletins,
    progress,
)
from pdf_extract.labeling.labels import (
    LabelError,
    is_valid_hash,
    is_valid_slug,
    read_label,
    write_label,
)
from pdf_extract.paths import ROOT
from pdf_extract.storage import connect_db, read_bulletin_pdf

LOGGER = logging.getLogger(__name__)

DEFAULT_PORT = 8766
STATIC_DIR = ROOT / "apps" / "labeler" / "dist"
MAX_BODY_BYTES = 2_000_000
_LOCAL_HOSTNAMES = {"localhost", "127.0.0.1", "[::1]", "::1"}


@dataclass
class LabelerApp:
    db_path: Path
    labels_dir: Path
    static_dir: Path = STATIC_DIR
    mode: str = "live"

    def config(self) -> dict[str, Any]:
        classifier = GeminiClassifier()
        return {
            "mode": self.mode,
            "classifier": classifier.name,
            "classifier_version": classifier.version,
            "remote": get_store().is_remote,
            "labels_dir": str(self.labels_dir),
            "default_labeler": default_labeler(),
        }

    def queue(self) -> list[dict[str, Any]]:
        conn = connect_db(self.db_path)
        try:
            return list_bulletins(conn, self.labels_dir)
        finally:
            conn.close()


def default_labeler() -> str:
    try:
        name = subprocess.run(
            ["git", "config", "user.name"], capture_output=True, text=True, timeout=5,
        ).stdout.strip()
    except (OSError, subprocess.SubprocessError):
        name = ""
    return name or os.environ.get("USER", "")


def _is_local(host_header: str | None) -> bool:
    if not host_header:
        return False
    host = host_header.strip().lower()
    if host.startswith("["):
        host = host.split("]", 1)[0] + "]"
    else:
        host = host.rsplit(":", 1)[0] if host.count(":") == 1 else host
    return host in _LOCAL_HOSTNAMES


class _ApiError(Exception):
    def __init__(self, status: HTTPStatus, message: str) -> None:
        super().__init__(message)
        self.status = status


def make_handler(app: LabelerApp) -> type[BaseHTTPRequestHandler]:
    class Handler(BaseHTTPRequestHandler):
        server_version = "CarloLabeler/1"

        def log_message(self, format: str, *args: Any) -> None:
            LOGGER.debug("%s - %s", self.address_string(), format % args)

        # ── plumbing ──
        def _send(self, status: HTTPStatus, body: bytes, content_type: str,
                  extra: dict[str, str] | None = None) -> None:
            self.send_response(status)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            for k, v in (extra or {}).items():
                self.send_header(k, v)
            self.end_headers()
            if self.command != "HEAD":
                self.wfile.write(body)

        def _json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self._send(status, body, "application/json; charset=utf-8",
                       {"Cache-Control": "no-store"})

        def _guard(self) -> bool:
            origin = self.headers.get("Origin")
            if not _is_local(self.headers.get("Host")) or (
                origin and not _is_local(urlsplit(origin).netloc)
            ):
                self._json({"error": "Only local requests are accepted"}, HTTPStatus.FORBIDDEN)
                return False
            return True

        def _dispatch(self, method: str) -> None:
            if not self._guard():
                return
            url = urlsplit(self.path)
            parts = [unquote(p) for p in url.path.split("/") if p]
            try:
                if parts[:1] == ["api"]:
                    self._api(method, parts[1:], parse_qs(url.query))
                elif method in ("GET", "HEAD"):
                    self._static(url.path)
                else:
                    raise _ApiError(HTTPStatus.METHOD_NOT_ALLOWED, "Method not allowed")
            except _ApiError as e:
                self._json({"error": str(e)}, e.status)
            except LabelError as e:
                self._json({"error": str(e)}, HTTPStatus.BAD_REQUEST)
            except Exception as e:
                LOGGER.exception("Request failed: %s %s", method, self.path)
                self._json({"error": f"{type(e).__name__}: {e}"}, HTTPStatus.INTERNAL_SERVER_ERROR)

        def do_GET(self) -> None:  # noqa: N802
            self._dispatch("GET")

        def do_HEAD(self) -> None:  # noqa: N802
            self._dispatch("HEAD")

        def do_PUT(self) -> None:  # noqa: N802
            self._dispatch("PUT")

        def do_POST(self) -> None:  # noqa: N802
            self._dispatch("POST")

        def do_DELETE(self) -> None:  # noqa: N802
            self._dispatch("DELETE")

        # ── API ──
        def _bulletin_key(self, parish: str, content_hash: str) -> tuple[str, str]:
            if not is_valid_slug(parish) or not is_valid_hash(content_hash):
                raise _ApiError(HTTPStatus.BAD_REQUEST, "Invalid parish slug or content hash")
            return parish, content_hash

        def _api(self, method: str, parts: list[str], query: dict[str, list[str]]) -> None:
            reading = method in ("GET", "HEAD")
            if parts == ["config"] and reading:
                return self._json(app.config())
            if parts == ["bulletins"] and reading:
                queue = app.queue()
                return self._json({"bulletins": queue, "progress": progress(queue)})
            if parts == ["next"] and reading:
                return self._next(query)
            if len(parts) == 3 and parts[0] == "bulletins" and reading:
                return self._detail(*self._bulletin_key(parts[1], parts[2]))
            if len(parts) == 4 and parts[0] == "bulletins" and parts[3] == "pdf" and reading:
                return self._pdf(*self._bulletin_key(parts[1], parts[2]))
            if len(parts) == 3 and parts[0] == "labels" and method == "PUT":
                return self._save(*self._bulletin_key(parts[1], parts[2]))
            raise _ApiError(HTTPStatus.NOT_FOUND, f"No such endpoint: {method} /api/{'/'.join(parts)}")

        def _next(self, query: dict[str, list[str]]) -> None:
            after = None
            if query.get("after"):
                parish, _, content_hash = query["after"][0].partition("/")
                after = self._bulletin_key(parish, content_hash)
            parish_filter = (query.get("parish") or [None])[0] or None
            if parish_filter is not None and not is_valid_slug(parish_filter):
                raise _ApiError(HTTPStatus.BAD_REQUEST, "Invalid parish slug")
            unlabeled_parishes = (query.get("unlabeled_parishes") or [""])[0] in ("1", "true")
            queue = app.queue()
            self._json({
                "bulletin": next_bulletin(
                    queue,
                    after=after,
                    parish_slug=parish_filter,
                    unlabeled_parishes=unlabeled_parishes,
                ),
                "progress": progress(queue),
            })

        def _detail(self, parish: str, content_hash: str) -> None:
            conn = connect_db(app.db_path)
            try:
                detail = bulletin_detail(conn, parish, content_hash)
                queue = list_bulletins(conn, app.labels_dir)
            finally:
                conn.close()
            if detail is None:
                raise _ApiError(HTTPStatus.NOT_FOUND, "No such bulletin")
            detail["label"] = read_label(parish, content_hash, app.labels_dir)
            detail["progress"] = progress(queue)
            detail["parish_bulletins"] = parish_bulletins(queue, parish)
            self._json(detail)

        def _pdf(self, parish: str, content_hash: str) -> None:
            conn = connect_db(app.db_path)
            try:
                known = find_bulletin(conn, parish, content_hash) is not None
            finally:
                conn.close()
            if not known:
                raise _ApiError(HTTPStatus.NOT_FOUND, "No such bulletin")
            data = read_bulletin_pdf(parish, content_hash)
            if data is None:
                raise _ApiError(HTTPStatus.NOT_FOUND, "This bulletin PDF is not in storage")
            self._send(HTTPStatus.OK, data, "application/pdf",
                       {"Cache-Control": "private, max-age=86400"})

        def _save(self, parish: str, content_hash: str) -> None:
            length = int(self.headers.get("Content-Length") or 0)
            if length <= 0 or length > MAX_BODY_BYTES:
                raise _ApiError(HTTPStatus.BAD_REQUEST, "Missing or oversized body")
            if "application/json" not in (self.headers.get("Content-Type") or ""):
                raise _ApiError(HTTPStatus.UNSUPPORTED_MEDIA_TYPE, "Send application/json")
            try:
                body = json.loads(self.rfile.read(length).decode("utf-8"))
            except (UnicodeDecodeError, ValueError) as e:
                raise _ApiError(HTTPStatus.BAD_REQUEST, f"Invalid JSON: {e}") from e
            conn = connect_db(app.db_path)
            try:
                bulletin = find_bulletin(conn, parish, content_hash)
            finally:
                conn.close()
            if bulletin is None:
                raise _ApiError(HTTPStatus.NOT_FOUND, "No such bulletin")
            saved = write_label(
                body, parish_slug=parish, content_hash=content_hash,
                source_url=bulletin["source_url"], labels_dir=app.labels_dir,
            )
            self._json({"label": saved})

        # ── UI ──
        def _static(self, path: str) -> None:
            root = app.static_dir.resolve()
            index = root / "index.html"
            if not index.is_file():
                body = (
                    "<h1>The labeler UI is not built</h1>"
                    "<p>Run <code>pnpm --filter labeler build</code>, or start with "
                    "<code>pnpm label</code>, which builds it first.</p>"
                ).encode("utf-8")
                return self._send(HTTPStatus.OK, body, "text/html; charset=utf-8")
            target = (root / unquote(path).lstrip("/")).resolve()
            if not target.is_relative_to(root) or not target.is_file():
                target = index
            content_type = mimetypes.guess_type(target.name)[0] or "application/octet-stream"
            if target.suffix == ".mjs":
                content_type = "text/javascript"
            cache = "no-cache" if target == index else "public, max-age=31536000, immutable"
            self._send(HTTPStatus.OK, target.read_bytes(), content_type, {"Cache-Control": cache})

    return Handler


def make_server(app: LabelerApp, port: int = DEFAULT_PORT) -> ThreadingHTTPServer:
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(app))
    server.daemon_threads = True
    return server


def serve(app: LabelerApp, port: int = DEFAULT_PORT) -> dict[str, Any]:
    server = make_server(app, port)
    url = f"http://localhost:{server.server_address[1]}/"
    print(f"Labeler ({app.mode}) at {url}  (labels in {app.labels_dir}; Ctrl+C to stop)",
          flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return {"url": url, "mode": app.mode, "labels_dir": str(app.labels_dir)}
