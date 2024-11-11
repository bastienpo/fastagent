import MessageInput from "./MessageInput"

const ChatInterface: React.FC = () => {
    return (
        <div className="flex flex-col w-full items-center">
            <div className="w-1/2">
                <MessageInput />
            </div>
        </div>
    )
}

export default ChatInterface
