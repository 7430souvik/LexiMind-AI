import MessageBubble from "./MessageBubble";

export default function MessageList({ messages }) {
  return (
    <>
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          role={message.role}
          content={message.content}
        />
      ))}
    </>
  );
}