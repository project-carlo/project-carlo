import js from "@eslint/js";
import tseslint from "typescript-eslint";

// No browser globals: this package must run in React Native as well as the web.
export default tseslint.config(
  { ignores: ["dist"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: { ecmaVersion: 2022 },
  },
);
