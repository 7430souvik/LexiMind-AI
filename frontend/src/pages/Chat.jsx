import { useState } from "react";

import MainLayout from "../layouts/MainLayout";
import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";

import { uploadDocument } from "../services/documentService";
import {
  analyzeDocument,
  waitForAnalysis,
} from "../services/analysisService";
import { askQuestion } from "../services/chatService";

export default function Chat() {
  const [messages, setMessages] = useState([]);
  const [documentId, setDocumentId] = useState(null);

  // Send normal chat message (backend integration later)
  const handleSend = async (text) => {
  // Show user's message
  setMessages((prev) => [
    ...prev,
    {
      id: Date.now(),
      role: "user",
      content: text,
    },
  ]);

  // No document uploaded
  if (!documentId) {
    setMessages((prev) => [
      ...prev,
      {
        id: Date.now() + 1,
        role: "assistant",
        content: "Please upload a PDF first.",
      },
    ]);
    return;
  }

  try {
    const response = await askQuestion(documentId, text);

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now() + 2,
        role: "assistant",
        content: response.answer,
      },
    ]);
  } catch (error) {
    console.error(error);

    setMessages((prev) => [
      ...prev,
      {
        id: Date.now() + 3,
        role: "assistant",
        content: "Sorry, I couldn't answer your question.",
      },
    ]);
  }
};

  // Upload PDF
  const handleFileSelect = async (file) => {
    try {
      // Show selected PDF in chat immediately
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "user",
          type: "file",
          fileName: file.name,
          fileSize: file.size,
        },
      ]);

      // Upload PDF
      const result = await uploadDocument(file);

      setDocumentId(result.id);

      // Notify upload success
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "assistant",
          content: "✅ Document uploaded successfully.",
        },
        {
          id: Date.now() + 2,
          role: "assistant",
          content: "🔍 Analyzing your document...",
        },
      ]);

      // Start analysis
      await analyzeDocument(result.id);

      // Wait until analysis is complete
      const analysis = await waitForAnalysis(result.id);

      // Show AI results
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 3,
          role: "assistant",
          content: `📄 Summary\n\n${analysis.summary}`,
        },
        {
          id: Date.now() + 4,
          role: "assistant",
          content: `⚠️ Risks\n\n${analysis.risks}`,
        },
        {
          id: Date.now() + 5,
          role: "assistant",
          content: `📌 Key Clauses\n\n${analysis.key_clauses}`,
        },
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          id: Date.now(),
          role: "assistant",
          content: "❌ Failed to upload or analyze the document.",
        },
      ]);
    }
  };

  return (
    <MainLayout>
      <div className="flex flex-col h-full">
        <ChatWindow messages={messages} />

        <ChatInput
          onSend={handleSend}
          onFileSelect={handleFileSelect}
        />
      </div>
    </MainLayout>
  );
}