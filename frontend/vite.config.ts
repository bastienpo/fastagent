import react from "@vitejs/plugin-react"
import path from "path"
import { UserConfig } from "vite"

const ReactCompilerConfig = {
    target: "19",
}

// https://vite.dev/config/
/** @type {import('vite').UserConfig} */
export default {
    plugins: [
        react({
            babel: {
                plugins: [["babel-plugin-react-compiler", ReactCompilerConfig]],
            },
        }),
    ],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
} satisfies UserConfig
