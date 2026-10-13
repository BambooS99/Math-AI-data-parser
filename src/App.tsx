import { useState } from "react";
import Header from "./components/header/header";
import SidePanel from "./components/sidePanel/sidePanel";
import { Convo } from "./components/convo/convo";
import ChatInputForm from "./components/chatInputForm/chatInputForm";
import type { ChatMessage } from "./types/chat";
import "./styles/tokens.css";
import "./App.css";

export default function App() {
  const [submittedValue, setSubmittedValue] = useState<ChatMessage[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  return (
    <div className="app-shell">
      <Header />
      <div className="app-body">
        <SidePanel side="left" />
        <main className="app-main">
          <Convo isLoading={isLoading} input={submittedValue} />
          <ChatInputForm
            isLoading={isLoading}
            setIsLoading={setIsLoading}
            setSubmittedValue={setSubmittedValue}
          />
        </main>
        <SidePanel side="right" />
      </div>
    </div>
  );
}
