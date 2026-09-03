"""Local HTTP server for the labeling app.

Deliberately stdlib-only: this is a tool you run on your own machine against
your own working copy, and it should keep working without a package install or
a build step. It serves the static UI, a small JSON API over `labelapp`, and
the bulletin PDFs themselves.

Binds to loopback. It reads and writes files under the repository and has no
authentication, so it must not be exposed to a network.
"""

from __future__ import annotations

import json
import logging
import threading
import webbrowser
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlparse

from pdf_extract.pdf_truncate import ensure_truncated_pdf

from labelapp import corpus, events as ev, store
from labelapp.workspace import VALID_FILTERS, VALID_SORTS, Workspace

LOGGER = logging.getLogger(__name__)

STATIC_DIR = Path(__file__).resolve().parent.parent / "static"

CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8",
    ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8",
    ".svg": "image/svg+xml",
    ".json": "application/json; charset=utf-8",
}

MAX_BODY_BYTES = 8 * 1024 * 1024


class LabelServer(ThreadingHTTPServer):
    """Threading server holding the shared workspace behind a lock."""

    daemon_threads = True

    def __init__(self, address: tuple[str, int], workspace: Workspace) -> None:
        super().__init__(address, LabelHandler)
        self.workspace = workspace
        self.lock = threading.Lock()


class LabelHandler(BaseHTTPRequestHandler):
    server: LabelServer  # type: ignore[assignment]
    server_version = "bulletin-label/1.0"
    protocol_version = "HTTP/1.1"

    # ── plumbing ────────────────────────────────────────────────────────────
    def log_message(self, format: str, *args: Any) -> None:
        LOGGER.debug("%s - %s", self.address_string(), format % args)

    def _send(self, status: HTTPStatus, body: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        # A stale UI against a changed workspace is confusing; never cache.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(body)

    def _send_json(self, payload: Any, status: HTTPStatus = HTTPStatus.OK) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self._send(status, body, "application/json; charset=utf-8")

    def _send_error_json(self, status: HTTPStatus, message: str) -> None:
        self._send_json({"error": message}, status)

    def _read_json_body(self) -> Any:
        length = int(self.headers.get("Content-Length") or 0)
        if length <= 0:
            raise ValueError("empty request body")
        if length > MAX_BODY_BYTES:
            raise ValueError("request body too large")
        return json.loads(self.rfile.read(length).decode("utf-8"))

    def _query(self) -> dict[str, list[str]]:
        return parse_qs(urlparse(self.path).query)

    def _param(self, name: str, default: str | None = None) -> str | None:
        values = self._query().get(name)
        return values[0] if values else default

    # ── routing ─────────────────────────────────────────────────────────────
    def do_GET(self) -> None:
        route = urlparse(self.path).path
        try:
            if route.startswith("/api/"):
                self._handle_api_get(route)
            else:
                self._serve_static(route)
        except Exception as exc:
            LOGGER.exception("GET %s failed", route)
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_HEAD(self) -> None:
        self.do_GET()

    def do_POST(self) -> None:
        route = urlparse(self.path).path
        try:
            if route == "/api/label":
                self._save_label()
            elif route == "/api/reload":
                with self.server.lock:
                    self.server.workspace.reload()
                self._send_json({"ok": True})
            else:
                self._send_error_json(HTTPStatus.NOT_FOUND, f"No such endpoint: {route}")
        except ValueError as exc:
            self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:
            LOGGER.exception("POST %s failed", route)
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def do_DELETE(self) -> None:
        route = urlparse(self.path).path
        try:
            if route != "/api/label":
                self._send_error_json(HTTPStatus.NOT_FOUND, f"No such endpoint: {route}")
                return
            source_url = self._param("url")
            if not source_url:
                raise ValueError("url parameter is required")
            with self.server.lock:
                removed = store.delete_label(source_url)
                self.server.workspace.reload_labels()
            self._send_json({"deleted": removed})
        except ValueError as exc:
            self._send_error_json(HTTPStatus.BAD_REQUEST, str(exc))
        except Exception as exc:
            LOGGER.exception("DELETE %s failed", route)
            self._send_error_json(HTTPStatus.INTERNAL_SERVER_ERROR, str(exc))

    def _handle_api_get(self, route: str) -> None:
        if route == "/api/config":
            self._send_json(self._config())
        elif route == "/api/queue":
            self._send_json(self._queue())
        elif route == "/api/task":
            self._task()
        elif route == "/api/pdf":
            self._pdf()
        else:
            self._send_error_json(HTTPStatus.NOT_FOUND, f"No such endpoint: {route}")

    # ── endpoints ───────────────────────────────────────────────────────────
    def _config(self) -> dict[str, Any]:
        workspace = self.server.workspace
        with self.server.lock:
            return {
                "runs": workspace.run_names,
                "available_runs": corpus.available_runs(),
                "run_versions": {
                    name: run.version for name, run in workspace.runs.items()
                },
                "field_labels": ev.FIELD_LABELS,
                "sorts": list(VALID_SORTS),
                "filters": list(VALID_FILTERS),
                "labels_path": str(store.LABELS_PATH),
                "churches_by_parish": workspace.churches_by_parish,
                "parish_names": workspace.parish_names,
                "church_names": workspace.church_names,
            }

    def _queue_params(self) -> dict[str, Any]:
        sort = self._param("sort") or VALID_SORTS[0]
        which = self._param("which") or "all"
        return {
            "sort": sort if sort in VALID_SORTS else VALID_SORTS[0],
            "which": which if which in VALID_FILTERS else "all",
            "parish": self._param("parish") or None,
        }

    def _queue(self) -> dict[str, Any]:
        params = self._queue_params()
        with self.server.lock:
            workspace = self.server.workspace
            return {
                "params": params,
                "progress": workspace.progress(),
                "items": workspace.queue(**params),
            }

    def _task(self) -> None:
        source_url = self._param("url")
        params = self._queue_params()
        with self.server.lock:
            workspace = self.server.workspace
            if not source_url:
                queued = workspace.queue(**params)
                if not queued:
                    self._send_json({"task": None})
                    return
                source_url = queued[0]["bulletin_source_url"]

            review = workspace.review(source_url)
            if review is None:
                self._send_error_json(
                    HTTPStatus.NOT_FOUND, f"Unknown bulletin: {source_url}"
                )
                return

            self._send_json(
                {
                    "task": review,
                    "label": workspace.labels.get(source_url),
                    "summary": workspace.summary(source_url),
                    "parish_name": workspace.parish_names.get(
                        review["parish_slug"], review["parish_slug"]
                    ),
                    "church_names": workspace.church_names,
                    "parish_churches": workspace.churches_by_parish.get(
                        review["parish_slug"], []
                    ),
                    "next_url": workspace.next_url(source_url, **params),
                    "progress": workspace.progress(),
                }
            )

    def _save_label(self) -> None:
        payload = self._read_json_body()
        if not isinstance(payload, dict):
            raise ValueError("expected a JSON object")
        with self.server.lock:
            workspace = self.server.workspace
            saved = store.put_label(payload)
            workspace.reload_labels()
            self._send_json(
                {
                    "label": saved,
                    "summary": workspace.summary(saved["bulletin_source_url"]),
                    "progress": workspace.progress(),
                }
            )

    def _pdf(self) -> None:
        """Serve a bulletin PDF, capped to the pages the classifiers were shown.

        Only bulletins named in metadata.json are reachable: the request carries
        a source URL, never a filesystem path.
        """
        source_url = self._param("url")
        if not source_url:
            self._send_error_json(HTTPStatus.BAD_REQUEST, "url parameter is required")
            return
        with self.server.lock:
            bulletin = self.server.workspace.bulletins.get(source_url)
        if bulletin is None or bulletin.pdf_path is None:
            self._send_error_json(HTTPStatus.NOT_FOUND, "No PDF recorded for this bulletin")
            return
        if not bulletin.pdf_path.exists():
            self._send_error_json(
                HTTPStatus.NOT_FOUND,
                f"PDF not on disk at {bulletin.pdf_path}. Run `pnpm fetch` to download it.",
            )
            return
        try:
            read_path = ensure_truncated_pdf(bulletin.pdf_path)
        except Exception:
            LOGGER.warning("Could not truncate %s; serving in full", bulletin.pdf_path)
            read_path = bulletin.pdf_path
        self._send(HTTPStatus.OK, read_path.read_bytes(), "application/pdf")

    def _serve_static(self, route: str) -> None:
        relative = "index.html" if route in ("", "/") else route.lstrip("/")
        target = (STATIC_DIR / relative).resolve()
        if not target.is_relative_to(STATIC_DIR.resolve()) or not target.is_file():
            self._send_error_json(HTTPStatus.NOT_FOUND, f"Not found: {route}")
            return
        content_type = CONTENT_TYPES.get(target.suffix, "application/octet-stream")
        self._send(HTTPStatus.OK, target.read_bytes(), content_type)


def serve(
    run_names: list[str],
    *,
    host: str = "127.0.0.1",
    port: int = 8765,
    open_browser: bool = True,
) -> None:
    """Run the labeling app until interrupted."""
    workspace = Workspace(run_names)
    httpd = LabelServer((host, port), workspace)
    url = f"http://{host}:{port}/"

    progress = workspace.progress()
    LOGGER.info(
        "Labeling %s bulletins across runs %s — %s complete, %s disagreements to settle",
        progress["bulletins"],
        ", ".join(run_names),
        progress["complete"],
        progress["disputed_undecided"],
    )
    print(f"Bulletin labeling app: {url}")
    print(f"Ground truth: {store.LABELS_PATH}")

    if open_browser:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nStopped.")
    finally:
        httpd.server_close()
