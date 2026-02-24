import json from "@eslint/json";
import markdown from "@eslint/markdown";
import yml from "eslint-plugin-yml";

export default [
  // Global ignores — files handled by other tools
  {
    ignores: [
      "**/*.py",
      "**/*.lua",
      "**/*.sh",
      "**/*.toml",
      "**/*.tmpl",
      ".pytest_cache/",
      "node_modules/",
      "home/dot_config/nvim/lazy-lock.json",
    ],
  },

  // YAML — recommended rules, formatting disabled (Prettier handles it)
  ...yml.configs["flat/prettier"],

  // JSON — duplicate key detection
  {
    files: ["**/*.json"],
    plugins: { json },
    language: "json/json",
    rules: {
      "json/no-duplicate-keys": "error",
    },
  },

  // Markdown — recommended semantic rules
  ...markdown.configs.recommended,
];
