import { ScrollArea } from "@/components/ui/scroll-area"
import MessageInput from "@/components/custom/MessageInput"

interface Message {
    id: string
    content: string
    sender: "user" | "bot"
    timestamp: Date
}

interface ChatContainerProps {
    messages: Message[]
    onSendMessage: (message: string) => void
    onFileUpload: (file: File) => void
}

const ChatContainer = ({
    messages,
    onSendMessage,
    onFileUpload,
}: ChatContainerProps) => {
    return (
        <div className="flex flex-col h-full">
            <ScrollArea className="flex-1 p-4">
                <div className="space-y-4">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex ${
                                message.sender === "user"
                                    ? "justify-end"
                                    : "justify-start"
                            }`}
                        >
                            <div
                                className={`max-w-[70%] rounded-lg p-3 ${
                                    message.sender === "user"
                                        ? "bg-blue-500 text-white"
                                        : "bg-gray-200 text-gray-900"
                                }`}
                            >
                                {message.content}
                                <div
                                    className={`text-xs mt-1 ${
                                        message.sender === "user"
                                            ? "text-blue-100"
                                            : "text-gray-500"
                                    }`}
                                >
                                    {message.timestamp.toLocaleTimeString()}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </ScrollArea>

            <div className="p-4 border-t">
                <MessageInput
                    onSendMessage={onSendMessage}
                    onFileUpload={onFileUpload}
                />
            </div>
        </div>
    )
}

export default ChatContainer
