import react from "@vitejs/plugin-react-swc"
import path from "path"
import { UserConfig } from "vite"

// https://vite.dev/config/
/** @type {import('vite').UserConfig} */
export default {
    plugins: [react()],
    resolve: {
        alias: {
            "@": path.resolve(__dirname, "./src"),
        },
    },
} satisfies UserConfig
