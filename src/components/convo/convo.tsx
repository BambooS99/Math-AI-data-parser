import { useEffect, useRef } from "react";
import type { ChatMessage } from "../../types/chat";
import ChatBubble from "../chatBubble/chatBubble";
import "./convo.scss";
import LoadingSpinner from "../loading/loadingSpinner";

export function Convo({
  input,
  isLoading,
}: {
  input: ChatMessage[];
  isLoading: boolean;
}) {
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [input]);

  return (
    <div className="conversation-box" ref={scrollRef}>
      <div className="conversation-box__inner">
        {input.length === 0 ? (
          <div className="conversation-box__empty">
            <div className="conversation-box__empty-title">
              Enter your math equation here!
            </div>
          </div>
        ) : (
          <ul className="chat-list">
            {input.map((message) => (
              <li key={message.id}>
                <ChatBubble message={message} />
              </li>
            ))}
            {isLoading ? <LoadingSpinner /> : null}
          </ul>
        )}
      </div>
    </div>
  );
}
