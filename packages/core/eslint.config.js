import js from "@eslint/js";
import tseslint from "typescript-eslint";

// No browser globals here; the real guard is the type check (tsconfig.json has
// no DOM lib), since typescript-eslint turns off no-undef for TypeScript.
export default tseslint.config(
  { ignores: ["dist"] },
  {
    extends: [js.configs.recommended, ...tseslint.configs.recommended],
    files: ["**/*.{ts,tsx}"],
    languageOptions: { ecmaVersion: 2022 },
  },
);
