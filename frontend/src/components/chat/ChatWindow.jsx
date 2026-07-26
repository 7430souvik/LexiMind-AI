import MessageList from "./MessageList";
import WelcomeScreen from "./WelcomeScreen";

export default function ChatWindow({ messages }) {
  return (
    <div className="flex-1 overflow-y-auto bg-gray-50">
      <div className="flex-1 overflow-y-auto">
        {messages.length === 0 ? (
          <WelcomeScreen />
        ) : (
          <MessageList messages={messages} />
        )}
      </div>
    </div>
  );
}