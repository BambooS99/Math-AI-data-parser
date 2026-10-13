import React, { useState } from "react";
import "./chatInputForm.scss";
import type { ChatMessage } from "../../types/chat";
import { ENDPOINTS } from "../../config/api";

export default function ChatInputForm({
  setSubmittedValue,
  isLoading,
  setIsLoading,
}: {
  isLoading: boolean;
  setSubmittedValue: React.Dispatch<React.SetStateAction<ChatMessage[]>>;
  setIsLoading: React.Dispatch<React.SetStateAction<boolean>>;
}) {
  const [input, setInput] = useState("");

  function addAssistantMessage(text: string) {
    const reply: ChatMessage = {
      id: crypto.randomUUID(),
      text,
      sender: "assistant",
      createdAt: new Date().toISOString(),
    };
    setSubmittedValue((prev) => [...prev, reply]);
  }

  async function sendPrompt(message: string) {
    setIsLoading(true);
    try {
      const response = await fetch(ENDPOINTS.chat, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data = await response.json();

      if (data.solver?.success) {
        const steps: string[] = data.solver.steps ?? [];
        addAssistantMessage(
          [`Result: ${data.solver.result}`, ...steps].join("\n"),
        );
      } else {
        addAssistantMessage(
          data.solver?.error_message ??
            "I couldn't solve that. Could you rephrase it?",
        );
      }
    } catch (err) {
      console.error(err);
      addAssistantMessage("Couldn't reach the server. Please try again.");
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
          disabled={isLoading}
        />
        <button
          className="chatform-bar__send"
          onClick={handleSend}
          disabled={input.trim().length === 0 || isLoading}
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
