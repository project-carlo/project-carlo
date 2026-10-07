import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { createReadStream, statSync } from "node:fs";
import { resolve } from "node:path";
import type { Plugin } from "vite";

import { cloudflare } from "@cloudflare/vite-plugin";

import { SITE_ORIGIN, serializeJsonLd, websiteJsonLd } from "./src/lib/seo";
import { SNAPSHOT_FILE } from "./src/lib/snapshot";
import { CITY_MAP_ENTRY } from "./src/lib/cityMapEntry";

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

/** Serves the app shell for every page load in dev, as production did before
 *  it served real 404s. The Cloudflare plugin serves dev requests by
 *  wrangler.jsonc's not_found_handling ("404-page"), but dev has no
 *  prerendered pages, 404.html or landing.html, so without this every route
 *  but `/` would be an empty 404. Must come before cloudflare(). */
function serveShellInDev(): Plugin {
  return {
    name: "serve-shell-in-dev",
    apply: "serve",
    configureServer(server) {
      server.middlewares.use((req, _res, next) => {
        const path = req.url?.split("?")[0] ?? "";
        const isPageLoad =
          req.method === "GET" &&
          (req.headers.accept ?? "").includes("text/html") &&
          !path.startsWith("/api/") &&
          !path.startsWith("/@") &&
          !/\.[a-z0-9]+$/i.test(path);
        // The plugin's handler reads originalUrl, so rewrite both.
        if (isPageLoad) req.url = req.originalUrl = "/";
        next();
      });
    },
  };
}

export default defineConfig({
  plugins: [
    serveShellInDev(),
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
  environments: {
    client: {
      build: {
        // scripts/prerender.ts reads it to link the built stylesheet, fonts
        // and the city map's script.
        manifest: true,
        rollupOptions: {
          input: {
            index: resolve(__dirname, "index.html"),
            // Loaded by the prerendered city pages (see StaticCityPage).
            cityMap: resolve(__dirname, CITY_MAP_ENTRY),
          },
        },
      },
    },
  },
  build: {
    rollupOptions: {
      output: {
        manualChunks: {
          map: ["leaflet", "react-leaflet"],
          vendor: ["react", "react-dom", "react-dom/client", "react-router-dom"],
        },
      },
    },
  },
  server: {
    host: true,
    port: 5173,
  },
});