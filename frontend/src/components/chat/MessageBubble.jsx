export default function MessageBubble({ role, content }) {
  const isUser = role === "user";

  return (
    <div
      className={`flex w-full mb-6 ${
        isUser ? "justify-end" : "justify-start"
      }`}
    >
      <div className="max-w-3xl">

        <div className="text-sm text-gray-500 mb-1">
          {isUser ? "You" : "LexiMind"}
        </div>

        <div
          className={`rounded-2xl px-5 py-4 whitespace-pre-wrap ${
            isUser
              ? "bg-blue-600 text-white"
              : "bg-white border border-gray-200 shadow-sm"
          }`}
        >
          {content}
        </div>

      </div>
    </div>
  );
}