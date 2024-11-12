import { useState } from "react"
import ChatLayout from "@/components/custom/ChatLayout"
import ChatContainer from "@/components/custom/ChatContainer"

interface Message {
    id: string
    content: string
    sender: "user" | "bot"
    timestamp: Date
    fileUrl?: string
}

const App = () => {
    const [messages, setMessages] = useState<Message[]>([])

    // Message handling
    const handleSendMessage = (content: string) => {
        const newMessage: Message = {
            id: Date.now().toString(),
            content,
            sender: "user",
            timestamp: new Date(),
        }

        setMessages((prev) => [...prev, newMessage])

        // Simulate bot response
        setTimeout(() => {
            const botMessage: Message = {
                id: (Date.now() + 1).toString(),
                content: "This is a simulated response from the chatbot.",
                sender: "bot",
                timestamp: new Date(),
            }
            setMessages((prev) => [...prev, botMessage])
        }, 1000)
    }

    const handleFileUpload = (file: File) => {
        const fileUrl = URL.createObjectURL(file)
        const newMessage: Message = {
            id: Date.now().toString(),
            content: `Uploaded file: ${file.name}`,
            sender: "user",
            timestamp: new Date(),
            fileUrl,
        }
        setMessages((prev) => [...prev, newMessage])
    }

    return (
        <ChatLayout>
            <ChatContainer
                messages={messages}
                onSendMessage={handleSendMessage}
                onFileUpload={handleFileUpload}
            />
        </ChatLayout>
    )
}

export default App
