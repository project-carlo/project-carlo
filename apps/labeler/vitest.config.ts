import { defineConfig } from "vitest/config";

// Unit tests cover the pure editing logic (times, weeks, seasons, rows), so
// the Node environment is enough.
export default defineConfig({
  test: {
    environment: "node",
    include: ["src/**/*.test.ts"],
  },
});
