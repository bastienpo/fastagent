import React from "react"
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar"
import AppSidebar from "@/components/custom/AppSidebar"

interface ChatLayoutProps {
    children: React.ReactNode
}

const ChatLayout = ({ children }: ChatLayoutProps) => {
    return (
        <SidebarProvider>
            <AppSidebar />
            <main className="relative w-full">
                <SidebarTrigger />
                <div className="flex h-full bg-gray-100">
                    <div className="flex-1 flex flex-col">{children}</div>
                </div>
            </main>
        </SidebarProvider>
    )
}

export default ChatLayout
