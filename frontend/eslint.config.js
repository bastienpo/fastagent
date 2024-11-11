import globals from "globals"
import pluginJs from "@eslint/js"
import tseslint from "typescript-eslint"
import pluginReact from "eslint-plugin-react"
import pluginReactHooks from "eslint-plugin-react-hooks"
import pluginPrettier from "eslint-config-prettier"
import pluginOxlint from "eslint-plugin-oxlint"

/** @type {import('eslint').Linter.Config[]} */
export default [
    { ignores: ["dist", "pnpm-lock.yaml", "coverage"] }, // global ignores
    pluginJs.configs.recommended, // javascript predefined config
    ...tseslint.configs.recommended, // typescript predefined config
    {
        files: ["**/*.{js,mjs,cjs,ts,jsx,tsx}"],
        languageOptions: {
            globals: {
                ...globals.browser,
            },
        },
        settings: {
            react: {
                version: "detect",
            },
        },
        plugins: {
            reactHooks: pluginReactHooks,
        },
    },
    pluginReact.configs.flat["jsx-runtime"],
    pluginPrettier, // prettier shareable config
    pluginOxlint.configs["flat/recommended"], // oxlint shareable config
]
