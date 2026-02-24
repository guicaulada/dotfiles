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

  // Markdown rule overrides
  {
    files: ["**/*.md"],
    rules: {
      // Matches old markdownlint config (MD040 disabled) — not always
      // applicable for config snippets and prompt/skill files
      "markdown/fenced-code-language": "off",
    },
  },
  {
    files: ["home/dot_claude/**/*.md"],
    rules: {
      // False positives from [PLACEHOLDER] template syntax in skill files
      "markdown/no-missing-label-refs": "off",
      // False positives from wildcard patterns in YAML frontmatter
      // (e.g., allowed-tools: Bash(git *))
      "markdown/no-space-in-emphasis": "off",
    },
  },
];
