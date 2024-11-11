import { SendIcon, FileIcon } from "./Icons"

const MessageInput = () => {
    return (
        <div className="border-2 border-base-200 rounded-full">
            <div className="flex gap-2 items-center justify-center">
                <label className="btn btn-ghost w-12 rounded-full m-2">
                    <FileIcon />
                    <input type="file" className="hidden" />
                </label>

                <textarea
                    placeholder="Type your message..."
                    rows={1}
                    className="textarea-ghost resize-none focus:outline-none h-full w-full"
                />

                <button className="btn btn-primary h-full w-12 m-2 rounded-full">
                    <SendIcon />
                </button>
            </div>
        </div>
    )
}

export default MessageInput
