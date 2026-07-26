export default function TypingIndicator() {
  return (
    <div className="flex justify-start mb-6">
      <div className="rounded-2xl bg-white border px-4 py-3 shadow-sm">
        <span className="animate-pulse">LexiMind is thinking...</span>
      </div>
    </div>
  );
}