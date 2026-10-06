import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { createReadStream, statSync } from "node:fs";
import { resolve } from "node:path";
import type { Plugin } from "vite";

import { cloudflare } from "@cloudflare/vite-plugin";

import { SITE_ORIGIN, serializeJsonLd, websiteJsonLd } from "./src/lib/seo";
import { SNAPSHOT_FILE } from "./src/lib/snapshot";

/** Injects the site-level WebSite/Organization JSON-LD into index.html so the
 *  markup has a single source of truth in src/lib/seo.ts. */
function injectSiteJsonLd(): Plugin {
  return {
    name: "inject-site-jsonld",
    transformIndexHtml() {
      return [
        {
          tag: "script",
          attrs: { type: "application/ld+json" },
          children: serializeJsonLd(websiteJsonLd(SITE_ORIGIN)),
          injectTo: "head",
        },
      ];
    },
  };
}

/** Serves the snapshot in dev as the opaque gzip file production serves (see
 *  public/_headers). Vite's static server labels every `.gz` file
 *  `Content-Encoding: gzip`, so the browser would unzip it before api.ts does,
 *  and api.ts's own gunzip would then fail on plain JSON. */
function serveSnapshotOpaque(): Plugin {
  return {
    name: "serve-snapshot-opaque",
    configureServer(server) {
      server.middlewares.use(`/${SNAPSHOT_FILE}`, (req, res, next) => {
        const path = resolve(server.config.publicDir, SNAPSHOT_FILE);
        let size: number;
        try {
          size = statSync(path).size;
        } catch {
          return next();
        }
        res.writeHead(200, {
          "Content-Type": "application/octet-stream",
          "Content-Length": size,
          "Cache-Control": "no-cache",
          "X-Content-Type-Options": "nosniff",
        });
        if (req.method === "HEAD") return res.end();
        createReadStream(path).pipe(res);
      });
    },
  };
}

export default defineConfig({
  plugins: [
    serveSnapshotOpaque(),
    react(),
    tailwindcss(),
    cloudflare(),
    injectSiteJsonLd(),
  ],
  resolve: {
    alias: {
      "@": resolve(__dirname, "./src"),
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          map: ["leaflet", "react-leaflet"],
          vendor: ["react", "react-dom", "react-router-dom"],
        },
      },
    },
  },
  server: {
    host: true,
    port: 5173,
  },
});