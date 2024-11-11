import { createRoot } from "react-dom/client"
import { StrictMode } from "react"

function App() {
    return (
        <StrictMode>
            <div>Hello World</div>
        </StrictMode>
    )
}

const container = document.getElementById("root")
if (container) {
    const root = createRoot(container)
    root.render(<App />)
}
