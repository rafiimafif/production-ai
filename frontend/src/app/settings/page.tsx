"use client";

import { useState } from "react";

const MODELS = [
  { id: "qwen2.5-14b", tag: "qwen2.5:14b", desc: "Alibaba Qwen 2.5 (14B) — agentic workflows", size: "~9 GB" },
  { id: "qwen2.5-7b", tag: "qwen2.5:7b", desc: "Alibaba Qwen 2.5 (7B) — fast and efficient", size: "~4.5 GB" },
  { id: "qwen2.5-1.5b", tag: "qwen2.5:1.5b", desc: "Small model for embeddings & light tasks", size: "~900 MB" },
];

export default function SettingsPage() {
  const [defaultModel, setDefaultModel] = useState("qwen2.5-7b");
  const [ollamaHost, setOllamaHost] = useState("http://localhost:11434");
  const [saved, setSaved] = useState(false);

  const handleSave = () => {
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-[var(--accent-light)] to-purple-400 bg-clip-text text-transparent">
          Settings
        </h1>
        <p className="text-[var(--text-secondary)] text-sm mt-1">
          Configure your AI system
        </p>
      </div>

      {/* Connection */}
      <div className="glass rounded-2xl p-6 space-y-4">
        <h2 className="text-base font-semibold text-[var(--text-primary)]">
          Ollama Connection
        </h2>
        <div>
          <label
            htmlFor="ollama-host"
            className="block text-xs text-[var(--text-secondary)] mb-1.5"
          >
            Server URL
          </label>
          <input
            id="ollama-host"
            type="text"
            value={ollamaHost}
            onChange={(e) => setOllamaHost(e.target.value)}
            className="w-full glass rounded-xl px-4 py-2.5 text-sm text-[var(--text-primary)] bg-transparent focus:outline-none focus:ring-1 focus:ring-[var(--accent)]"
          />
        </div>
        <div>
          <label
            htmlFor="default-model"
            className="block text-xs text-[var(--text-secondary)] mb-1.5"
          >
            Default Model
          </label>
          <select
            id="default-model"
            value={defaultModel}
            onChange={(e) => setDefaultModel(e.target.value)}
            className="w-full glass rounded-xl px-4 py-2.5 text-sm text-[var(--text-primary)] bg-transparent focus:outline-none focus:ring-1 focus:ring-[var(--accent)] cursor-pointer"
          >
            {MODELS.filter((m) => m.id !== "qwen2.5-1.5b").map((m) => (
              <option key={m.id} value={m.id}>
                {m.tag}
              </option>
            ))}
          </select>
        </div>
        <button
          id="save-settings"
          onClick={handleSave}
          className={`px-5 py-2.5 rounded-xl text-sm font-medium transition-smooth ${
            saved
              ? "bg-[var(--success)] text-white"
              : "bg-[var(--accent)] text-white hover:opacity-90 glow"
          }`}
        >
          {saved ? "✓ Saved" : "Save Settings"}
        </button>
      </div>

      {/* Model Registry */}
      <div className="glass rounded-2xl p-6 space-y-4">
        <h2 className="text-base font-semibold text-[var(--text-primary)]">
          Model Registry
        </h2>
        <div className="space-y-3">
          {MODELS.map((m) => (
            <div
              key={m.id}
              className="flex items-center justify-between p-4 rounded-xl bg-[var(--bg-elevated)] border border-[var(--border)]"
            >
              <div>
                <p className="text-sm font-medium text-[var(--text-primary)]">
                  {m.tag}
                </p>
                <p className="text-xs text-[var(--text-secondary)] mt-0.5">
                  {m.desc}
                </p>
              </div>
              <div className="flex items-center gap-3">
                <span className="text-xs text-[var(--text-muted)]">{m.size}</span>
                <span className="px-2 py-0.5 rounded-md text-[10px] font-medium bg-[var(--accent-glow)] text-[var(--accent-light)] border border-[var(--accent)]">
                  {m.id === defaultModel ? "DEFAULT" : "AVAILABLE"}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* System Info */}
      <div className="glass rounded-2xl p-6 space-y-3">
        <h2 className="text-base font-semibold text-[var(--text-primary)]">
          System Info
        </h2>
        <div className="grid grid-cols-2 gap-3 text-sm">
          {[
            ["Backend", "FastAPI + Uvicorn"],
            ["Orchestration", "LangGraph"],
            ["Vector Store", "ChromaDB"],
            ["Tool Protocol", "MCP (Model Context Protocol)"],
            ["Observability", "Langfuse"],
            ["Infrastructure", "Docker Compose"],
          ].map(([key, value]) => (
            <div key={key} className="flex justify-between py-2 border-b border-[var(--border)]">
              <span className="text-[var(--text-secondary)]">{key}</span>
              <span className="text-[var(--text-primary)] font-medium">{value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
