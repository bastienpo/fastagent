import { ScrollArea } from "@/components/ui/scroll-area"
import MessageInput from "@/components/custom/MessageInput"
import { Message } from "@/types/message"
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
            <ScrollArea className="flex-1 md:px-36 md:pt-6 p-6">
                <div className="space-y-4">
                    {messages.map((message) => (
                        <div
                            key={message.id}
                            className={`flex justify-start ${
                                message.sender === "user" ? "" : ""
                            }`}
                        >
                            <div
                                className={`rounded-lg p-3 ${
                                    message.sender === "user"
                                        ? "bg-blue-500 text-white"
                                        : "bg-gray-200 text-gray-900 w-full"
                                }`}
                            >
                                {message.content}
                                <div
                                    className={`text-xs mt-1 ${
                                        message.sender === "user"
                                            ? "text-blue-100"
                                            : "text-gray-500"
                                    }`}
                                ></div>
                            </div>
                        </div>
                    ))}
                </div>
            </ScrollArea>

            <div className="md:px-36 md:py-6 p-6">
                <MessageInput
                    onSendMessage={onSendMessage}
                    onFileUpload={onFileUpload}
                />
            </div>
        </div>
    )
}

export default ChatContainer
