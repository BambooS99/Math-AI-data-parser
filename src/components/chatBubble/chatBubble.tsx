import type { ChatMessage } from "../../types/chat";
import "./chatBubble.scss";

export default function ChatBubble({ message }: { message: ChatMessage }) {
  const isUser = message.sender === "user";

  return (
    <div
      className={`chat-bubble-row ${isUser ? "chat-bubble-row--user" : "chat-bubble-row--assistant"}`}
    >
      <div
        className={`chat-bubble ${isUser ? "chat-bubble--user" : "chat-bubble--assistant"}`}
      >
        {message.text}
      </div>
    </div>
  );
}
