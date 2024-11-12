import { useState } from "react"
import ChatLayout from "@/components/custom/ChatLayout"
import ChatContainer from "@/components/custom/ChatContainer"
import { Message } from "@/types/message"

const App = () => {
    const [messages, setMessages] = useState<Message[]>([])

    // Message handling
    const handleSendMessage = (content: string) => {
        const newMessage: Message = {
            id: 1,
            content,
            sender: "user",
            timestamp: new Date(),
            conversation_id: 1,
        }

        setMessages((prev) => [...prev, newMessage])

        // Simulate bot response
        setTimeout(() => {
            const botMessage: Message = {
                id: 2,
                content: "Hello world!.",
                sender: "assistant",
                timestamp: new Date(),
                conversation_id: 1,
            }
            setMessages((prev) => [...prev, botMessage])
        }, 5)
    }

    return (
        <ChatLayout>
            <ChatContainer
                messages={messages}
                onSendMessage={handleSendMessage}
                onFileUpload={() => {}}
            />
        </ChatLayout>
    )
}

export default App
