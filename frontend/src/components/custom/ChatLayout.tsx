import React from "react"
import { Separator } from "@/components/ui/separator"

interface ChatLayoutProps {
    children: React.ReactNode
}

const ChatLayout = ({ children }: ChatLayoutProps) => {
    return (
        <div className="flex h-screen bg-gray-100">
            <Separator orientation="vertical" />

            <div className="flex-1 flex flex-col">{children}</div>
        </div>
    )
}

export default ChatLayout
