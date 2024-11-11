import react from "@vitejs/plugin-react-swc"
import { UserConfig } from "vite"

// https://vite.dev/config/
/** @type {import('vite').UserConfig} */
export default {
    plugins: [react()],
} satisfies UserConfig
