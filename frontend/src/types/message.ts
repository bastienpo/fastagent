interface Message {
    id: number
    content: string
    sender: "user" | "assistant"
    timestamp: Date
    fileUrl?: string
    conversation_id: number
}

export type { Message }
