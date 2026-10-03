import { createReadStream, existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import type { IncomingMessage, ServerResponse } from "node:http";
import { createRequire } from "node:module";
import path from "node:path";
import { defineConfig, type Plugin } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// `pnpm dev:labeler` serves the UI with hot reload and forwards /api to the
// Python server started by `pnpm label` (or `pnpm label --demo`).
const apiPort = process.env.LABELER_API_PORT ?? "8766";

function pdfjsWasmDir(): string {
  const require = createRequire(import.meta.url);
  return path.join(path.dirname(require.resolve("pdfjs-dist/package.json")), "wasm");
}

/** Serve pdf.js's wasm decoders at /pdfjs/wasm/ in dev, and emit them into dist. */
function pdfjsWasm(): Plugin {
  const wasmDir = path.resolve(pdfjsWasmDir());
  const serve = (req: IncomingMessage, res: ServerResponse, next: (err?: unknown) => void) => {
    const rel = decodeURIComponent((req.url ?? "/").split("?")[0] ?? "/").replace(/^\/+/, "");
    if (!rel || rel.split("/").some((part) => part === ".." || part === "")) {
      next();
      return;
    }
    const file = path.resolve(wasmDir, rel);
    if (!file.startsWith(`${wasmDir}${path.sep}`) || !existsSync(file) || !statSync(file).isFile()) {
      next();
      return;
    }
    const contentType = file.endsWith(".wasm")
      ? "application/wasm"
      : file.endsWith(".js")
        ? "text/javascript"
        : "application/octet-stream";
    res.setHeader("Content-Type", contentType);
    createReadStream(file).pipe(res);
  };
  return {
    name: "pdfjs-wasm",
    configureServer(server) {
      server.middlewares.use("/pdfjs/wasm", serve);
    },
    configurePreviewServer(server) {
      server.middlewares.use("/pdfjs/wasm", serve);
    },
    generateBundle() {
      for (const name of readdirSync(wasmDir)) {
        const full = path.join(wasmDir, name);
        if (!statSync(full).isFile()) continue;
        this.emitFile({
          type: "asset",
          fileName: `pdfjs/wasm/${name}`,
          source: readFileSync(full),
        });
      }
    },
  };
}

export default defineConfig({
  plugins: [react(), tailwindcss(), pdfjsWasm()],
  server: {
    host: "127.0.0.1",
    port: 5174,
    proxy: {
      "/api": { target: `http://127.0.0.1:${apiPort}` },
    },
  },
  build: {
    chunkSizeWarningLimit: 1500,
  },
});
