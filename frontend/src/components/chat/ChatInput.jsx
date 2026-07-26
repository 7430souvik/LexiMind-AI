import { SendHorizontal } from "lucide-react";
import UploadButton from "./UploadButton";
import { useState } from "react";

export default function ChatInput ({
  onSend,
  onFileSelect,
}){
  const [text, setText] = useState("");

  const handleSend = () => {
    if (!text.trim()) return;

    onSend(text);
    setText("");
  };

  return (
    <div className="border-t bg-white p-5">

      <div className="max-w-4xl mx-auto">

        <div className="flex items-center rounded-2xl border bg-white px-4 py-3 shadow-sm">

          <UploadButton onFileSelect={onFileSelect} />

          <input
            className="flex-1 outline-none"
            placeholder="Ask anything..."
            value={text}
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                handleSend();
              }
            }}
          />

          <button
            onClick={handleSend}
            className="ml-3 rounded-full bg-black p-2 text-white hover:bg-gray-800"
          >
            <SendHorizontal size={18} />
          </button>

        </div>

      </div>

    </div>
  );
}