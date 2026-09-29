import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";
import tailwindcss from "@tailwindcss/vite";

// `pnpm dev:labeler` serves the UI with hot reload and forwards /api to the
// Python server started by `pnpm label` (or `pnpm label --demo`).
const apiPort = process.env.LABELER_API_PORT ?? "8766";

export default defineConfig({
  plugins: [react(), tailwindcss()],
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
