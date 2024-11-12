import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Message } from "@/types/message"

export const messageKeys = {
    all: ['messages'] as const,
    list: () => [...messageKeys.all, 'list'] as const,
}

export const messageService = {
    // Fetch messages
    async getMessages(): Promise<Message[]> {
        const response = await fetch('/v1/messages')
        if (!response.ok) throw new Error('Failed to fetch messages')
        return response.json()
    },

    // Send message
    async sendMessage(message: Omit<Message, 'id'>): Promise<Message> {
        const response = await fetch('/v1/messages', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(message),
        })
        if (!response.ok) throw new Error('Failed to send message')
        return response.json()
    },
}

// Custom hooks for React Query
export function useMessages() {
    return useQuery({
        queryKey: messageKeys.list(),
        queryFn: messageService.getMessages,
    })
}

export function useSendMessage() {
    const queryClient = useQueryClient()
    
    return useMutation({
        mutationFn: messageService.sendMessage,
        onMutate: async (newMessage) => {
            // Cancel outgoing refetches
            await queryClient.cancelQueries({ queryKey: messageKeys.list() })

            // Snapshot the previous value
            const previousMessages = queryClient.getQueryData(messageKeys.list())

            // Optimistically update
            queryClient.setQueryData(messageKeys.list(), (old: Message[] = []) => [
                ...old,
                { ...newMessage, id: `temp-${Date.now()}` },
            ])

            return { previousMessages }
        },
        onError: (err, newMessage, context) => {
            // Rollback on error
            queryClient.setQueryData(messageKeys.list(), context?.previousMessages)
        },
        onSettled: () => {
            // Refetch after error or success
            queryClient.invalidateQueries({ queryKey: messageKeys.list() })
        },
    })
}