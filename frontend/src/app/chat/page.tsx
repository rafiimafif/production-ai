"use client";

import { useState, useRef, useEffect } from "react";
import type { ChatMessage } from "@/lib/api";

export default function ChatPage() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [model, setModel] = useState("gemma3");
  const [useAgent, setUseAgent] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    const text = input.trim();
    if (!text || isLoading) return;

    const userMsg: ChatMessage = { role: "user", content: text };
    const newMessages = [...messages, userMsg];
    setMessages(newMessages);
    setInput("");
    setIsLoading(true);

    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/chat`,
        {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            messages: newMessages,
            model,
            use_agent: useAgent,
          }),
        }
      );
      const data = await res.json();
      setMessages([
        ...newMessages,
        { role: "assistant", content: data.response || "No response received." },
      ]);
    } catch {
      setMessages([
        ...newMessages,
        {
          role: "assistant",
          content:
            "⚠️ Could not connect to the backend. Make sure `uvicorn backend.main:app` is running on port 8000.",
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto flex flex-col h-[calc(100vh-3rem)]">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-3xl font-bold bg-gradient-to-r from-[var(--accent-light)] to-purple-400 bg-clip-text text-transparent">
            Chat
          </h1>
          <p className="text-[var(--text-secondary)] text-sm mt-1">
            Talk to your local AI — powered by Ollama
          </p>
        </div>
        <div className="flex items-center gap-3">
          {/* Model selector */}
          <select
            id="model-selector"
            value={model}
            onChange={(e) => setModel(e.target.value)}
            className="glass rounded-xl px-3 py-2 text-xs text-[var(--text-secondary)] bg-transparent border-none focus:outline-none focus:ring-1 focus:ring-[var(--accent)] cursor-pointer"
          >
            <option value="gemma3">Gemma 3</option>
            <option value="llama3">Llama 3.3</option>
            <option value="mistral">Mistral Small</option>
          </select>
          {/* Agent toggle */}
          <button
            id="agent-toggle"
            onClick={() => setUseAgent(!useAgent)}
            className={`px-3 py-2 rounded-xl text-xs font-medium transition-smooth ${
              useAgent
                ? "bg-[var(--accent)] text-white glow"
                : "glass text-[var(--text-secondary)] hover:text-[var(--text-primary)]"
            }`}
          >
            {useAgent ? "Agent ON" : "Agent OFF"}
          </button>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto space-y-4 pr-2">
        {messages.length === 0 && (
          <div className="flex items-center justify-center h-full">
            <div className="text-center space-y-4">
              <div className="w-16 h-16 rounded-2xl bg-gradient-to-br from-[var(--accent)] to-purple-600 flex items-center justify-center mx-auto glow">
                <span className="text-2xl">🤖</span>
              </div>
              <p className="text-[var(--text-secondary)] text-sm">
                Send a message to start the conversation
              </p>
              <div className="flex flex-wrap gap-2 justify-center">
                {[
                  "Explain LangGraph",
                  "Search my documents",
                  "What models are available?",
                ].map((suggestion) => (
                  <button
                    key={suggestion}
                    onClick={() => setInput(suggestion)}
                    className="glass px-3 py-1.5 rounded-xl text-xs text-[var(--text-secondary)] hover:text-[var(--text-primary)] transition-smooth hover:scale-105"
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[75%] px-4 py-3 text-sm whitespace-pre-wrap ${
                msg.role === "user" ? "message-user text-white" : "message-ai"
              }`}
            >
              {msg.content}
            </div>
          </div>
        ))}

        {isLoading && (
          <div className="flex justify-start">
            <div className="message-ai px-4 py-3 flex gap-1.5">
              <span className="w-2 h-2 rounded-full bg-[var(--text-secondary)] typing-dot" />
              <span className="w-2 h-2 rounded-full bg-[var(--text-secondary)] typing-dot" />
              <span className="w-2 h-2 rounded-full bg-[var(--text-secondary)] typing-dot" />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="mt-4 glass rounded-2xl p-3 flex items-center gap-3">
        <input
          id="chat-input"
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && !e.shiftKey && handleSend()}
          placeholder="Type your message..."
          className="flex-1 bg-transparent text-sm text-[var(--text-primary)] placeholder:text-[var(--text-muted)] focus:outline-none"
        />
        <button
          id="chat-send"
          onClick={handleSend}
          disabled={isLoading || !input.trim()}
          className="px-4 py-2 rounded-xl bg-[var(--accent)] text-white text-sm font-medium transition-smooth hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed glow"
        >
          Send
        </button>
      </div>
    </div>
  );
}
