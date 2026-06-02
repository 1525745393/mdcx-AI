import globals from "globals";
import pluginJs from "@eslint/js";
import pluginJsdoc from "eslint-plugin-jsdoc";
import eslintConfigPrettier from "eslint-config-prettier";

export default [
  {
    languageOptions: {
      globals: {
        ...globals.browser,
        ...globals.node,
        ...globals.es2021
      },
      ecmaVersion: "latest",
      sourceType: "module"
    },
    rules: {
      "no-unused-vars": ["error", { "argsIgnorePattern": "^_" }],
      "no-console": "warn",
      "no-debugger": "error",
      "semi": ["error", "always"],
      "quotes": ["error", "single"],
      "indent": ["error", 4],
      "linebreak-style": ["error", "unix"],
      "no-trailing-spaces": "error",
      "eol-last": "error",
      "comma-dangle": ["error", "never"],
      "object-curly-spacing": ["error", "always"],
      "array-bracket-spacing": ["error", "always"],
      "jsdoc/require-description": "warn",
      "jsdoc/require-param": "warn",
      "jsdoc/require-returns": "warn",
      "jsdoc/require-returns-check": "warn",
      "jsdoc/valid-types": "error",
      "jsdoc/no-undefined-types": "warn",
      "jsdoc/check-tag-names": "warn",
      "jsdoc/check-types": "warn"
    }
  },
  pluginJs.configs.recommended,
  pluginJsdoc.configs["flat/recommended"],
  eslintConfigPrettier
];
