import globals from "globals"
import pluginJs from "@eslint/js"
import tseslint from "typescript-eslint"
import pluginReact from "eslint-plugin-react"
import pluginPrettier from "eslint-config-prettier"
import pluginOxlint from "eslint-plugin-oxlint"

/** @type {import('eslint').Linter.Config[]} */
export default [
    pluginJs.configs.recommended,
    ...tseslint.configs.recommended,
    {
        files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"],
        ignores: ["dist"],
        languageOptions: { globals: globals.browser },
    },
    pluginReact.configs.flat.recommended,
    pluginReact.configs.flat["jsx-runtime"],
    pluginOxlint.configs["flat/recommended"],
    pluginPrettier,
]
