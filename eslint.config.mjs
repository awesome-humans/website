// ESLint for the site's JavaScript in pages/javascripts/: plain browser scripts,
// loaded by zensical.toml's extra_javascript, so no modules and no build step.
import js from "@eslint/js";
import globals from "globals";

export default [
  // uv's environment, with Zensical's own bundled scripts, and the staged site.
  { ignores: [".venv/", "build/"] },
  js.configs.recommended,
  {
    files: ["pages/javascripts/**/*.js"],
    languageOptions: {
      sourceType: "script",
      // __md_scope is the theme's, which its own script defines before these load.
      globals: { ...globals.browser, __md_scope: "readonly" },
    },
  },
];
