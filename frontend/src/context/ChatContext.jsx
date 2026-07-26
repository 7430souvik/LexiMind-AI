import { createContext, useContext, useState } from "react";

const ChatContext = createContext();

export function ChatProvider({ children }) {
  const [messages, setMessages] = useState([]);
  const [currentDocument, setCurrentDocument] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);

  return (
    <ChatContext.Provider
      value={{
        messages,
        setMessages,
        currentDocument,
        setCurrentDocument,
        loading,
        setLoading,
        uploading,
        setUploading,
      }}
    >
      {children}
    </ChatContext.Provider>
  );
}

export function useChat() {
  return useContext(ChatContext);
}