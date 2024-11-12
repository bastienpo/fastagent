import React, { useState, useRef } from "react"
import { Button } from "@/components/ui/button"
import { Textarea } from "@/components/ui/textarea"
import { Paperclip, Send } from "lucide-react"

interface MessageInputProps {
    onSendMessage: (message: string) => void
    onFileUpload: (file: File) => void
}

const MessageInput = ({ onSendMessage }: MessageInputProps) => {
    const [message, setMessage] = useState("")
    const fileInputRef = useRef<HTMLInputElement>(null)

    const handleSend = () => {
        if (message.trim()) {
            onSendMessage(message.trim())
            setMessage("")
        }
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    return (
        <div className="flex gap-2">
            <div className="flex-1">
                <Textarea
                    placeholder="Type your message..."
                    value={message}
                    onChange={(e) => setMessage(e.target.value)}
                    onKeyDown={handleKeyPress}
                    className="min-h-[80px] max-h-[200px] resize-none"
                />
            </div>

            <div className="flex flex-col gap-2">
                <Button
                    size="icon"
                    variant="outline"
                    onClick={() => fileInputRef.current?.click()}
                >
                    <Paperclip className="h-4 w-4" />
                </Button>

                <Button size="icon" onClick={handleSend}>
                    <Send className="h-4 w-4" />
                </Button>
            </div>

            <input
                type="file"
                ref={fileInputRef}
                onChange={() => {}}
                accept=".png,.pdf,.jpg,.jpeg,.csv"
                className="hidden"
            />
        </div>
    )
}

export default MessageInput
