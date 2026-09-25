import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";
import { resolve } from "node:path";
import type { Plugin } from "vite";

import { cloudflare } from "@cloudflare/vite-plugin";

import { SITE_ORIGIN, serializeJsonLd, websiteJsonLd } from "./src/lib/seo";

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

export default defineConfig({
  plugins: [react(), tailwindcss(), cloudflare(), injectSiteJsonLd()],
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