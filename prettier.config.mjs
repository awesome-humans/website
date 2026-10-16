// Prettier settings beyond its defaults. The command line in package.json sets
// --prose-wrap preserve; this file holds what varies by file type.
export default {
  overrides: [
    {
      // JSONC allows comments but not trailing commas, and VS Code's JSONC checker
      // flags them. Prettier would add them, as it does in JavaScript.
      files: "*.jsonc",
      options: { trailingComma: "none" },
    },
  ],
};
