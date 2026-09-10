// Minimal static file server for the built app (apps/web/dist).
//
// The e2e suite runs against `wrangler dev` because it needs the production
// Worker semantics; the benchmark deliberately does not. A plain Node server
// starts in milliseconds, adds no proxy/miniflare layer between the browser and
// the bytes, and keeps run-to-run timing noise down — which is what a
// measurement harness needs. SPA fallback mirrors wrangler's
// `not_found_handling: "single-page-application"`.
import { createReadStream, existsSync, statSync } from "node:fs";
import { createServer } from "node:http";
import { extname, join, normalize, resolve, sep } from "node:path";

const MIME = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".wasm": "application/wasm",
  ".webmanifest": "application/manifest+json",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".xml": "application/xml",
};

/** Resolve a request path to a file inside `root`, or null when it escapes. */
function resolveFile(root, urlPath) {
  let decoded;
  try {
    decoded = decodeURIComponent(urlPath.split("?")[0]);
  } catch {
    // Malformed percent-encoding: treat as not-found rather than letting the
    // URIError take the whole server down mid-run.
    return null;
  }
  const candidate = resolve(join(root, normalize(decoded)));
  // Compare against `root + sep`, not a bare prefix: `startsWith(root)` also
  // admits a sibling directory whose name merely begins with root's ("dist"
  // would match "dist-other").
  if (candidate !== root && !candidate.startsWith(root + sep)) return null;
  if (existsSync(candidate) && statSync(candidate).isDirectory()) {
    const index = join(candidate, "index.html");
    return existsSync(index) ? index : null;
  }
  return existsSync(candidate) ? candidate : null;
}

/**
 * @param {{ root: string, port?: number }} options
 * @returns {Promise<{ origin: string, close: () => Promise<void> }>}
 */
export function startStaticServer({ root, port = 0 }) {
  const absoluteRoot = resolve(root);
  if (!existsSync(join(absoluteRoot, "index.html"))) {
    throw new Error(
      `No index.html in ${absoluteRoot}. Run \`pnpm --filter web build\` first.`,
    );
  }

  const server = createServer((req, res) => {
    const file =
      resolveFile(absoluteRoot, req.url ?? "/") ??
      join(absoluteRoot, "index.html");
    res.writeHead(200, {
      "content-type": MIME[extname(file)] ?? "application/octet-stream",
      // The benchmark controls caching itself (each run uses a fresh context),
      // so serve without validators to keep every run byte-identical.
      "cache-control": "no-store",
    });
    createReadStream(file).pipe(res);
  });

  return new Promise((resolvePromise) => {
    server.listen(port, "127.0.0.1", () => {
      const address = server.address();
      const boundPort = typeof address === "object" && address ? address.port : port;
      resolvePromise({
        origin: `http://127.0.0.1:${boundPort}`,
        close: () =>
          new Promise((done) => {
            server.closeAllConnections?.();
            server.close(() => done());
          }),
      });
    });
  });
}
