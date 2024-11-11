import daisyui from "daisyui"

/** @type {import('tailwindcss').Config} */
export default {
    content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
    theme: {
        colors: {
            "azure-radiance": {
                50: "#f0f8fe",
                100: "#dceffd",
                200: "#c2e3fb",
                300: "#97d3f9",
                400: "#66baf4",
                500: "#439cee",
                600: "#3584e4",
                700: "#256ad0",
                800: "#2455a9",
                900: "#224a86",
                950: "#192e52",
            },
        },
        extend: {},
    },
    plugins: [daisyui],
    daisyui: {
        themes: ["bumblebee"],
    },
}
