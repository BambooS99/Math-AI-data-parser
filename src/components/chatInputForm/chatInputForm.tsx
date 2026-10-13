import React, { useState } from "react";
import "./chatInputForm.scss";
import type { ChatMessage } from "../../types/chat";

export default function ChatInputForm({
  submittedValue,
  setSubmittedValue,
  isLoading,
  setIsLoading,
}: {
  isLoading: boolean;
  submittedValue: ChatMessage[];
  setSubmittedValue: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  setIsLoading: any;
}) {
  const [input, setInput] = useState("");
  const API_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

  async function sendPrompt(message: string) {
    const url = `${API_URL}/chat`;
    setIsLoading(true);
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();

      const replyText = data.solver.success
        ? String(data.solver.result)
        : (data.solver.error_message ?? "Sorry I couldn't solve that");

      const assistantMessage: ChatMessage = {
        id: crypto.randomUUID(),
        text: replyText,
        sender: "assistant",
        createdAt: new Date().toISOString(),
      };

      setSubmittedValue((prev) => [...prev, assistantMessage]);
    } catch {
      const errorMessage: ChatMessage = {
        id: crypto.randomUUID(),
        text: "I couldnt get a valid response from the API. Please try again later",
        sender: "assistant",
        createdAt: new Date().toISOString(),
      };
      setSubmittedValue((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  function handleSend() {
    const message = input.trim();
    if (message.length === 0) return;

    const nextMessage: ChatMessage = {
      id: crypto.randomUUID(),
      text: message,
      sender: "user",
      createdAt: new Date().toISOString(),
    };

    setSubmittedValue((prev) => [...prev, nextMessage]);
    setInput("");
    sendPrompt(message);
  }

  // understand this section deeply

  function handleKeyDown(e: React.KeyboardEvent<HTMLTextAreaElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="chatform-container">
      <div className="chatform-bar">
        <textarea
          className="chatform-bar__input"
          placeholder="Message Math GPT..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          rows={1}
        />
        <button
          className="chatform-bar__send"
          onClick={handleSend}
          disabled={input.trim().length === 0}
          aria-label="Send message"
        >
          <svg
            width="16"
            height="16"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            strokeWidth="1.75"
            strokeLinecap="round"
            strokeLinejoin="round"
          >
            <path d="M12 19V5" />
            <path d="M5 12l7-7 7 7" />
          </svg>
        </button>
      </div>
    </div>
  );
}
