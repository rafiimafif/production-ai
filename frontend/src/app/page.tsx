"use client";

import { useEffect, useState } from "react";

interface ServiceStatus {
  name: string;
  status: "online" | "offline" | "loading";
  description: string;
}

const SERVICES: ServiceStatus[] = [
  { name: "Ollama LLM", status: "loading", description: "Local inference engine" },
  { name: "ChromaDB", status: "loading", description: "Vector store for RAG" },
  { name: "LangGraph", status: "loading", description: "Agent orchestration" },
  { name: "MCP Server", status: "loading", description: "Tool protocol layer" },
];

const STATS = [
  { label: "Models Loaded", value: "3", sub: "Gemma · Llama · Mistral" },
  { label: "Documents Indexed", value: "0", sub: "Upload via Documents page" },
  { label: "Conversations", value: "0", sub: "Start chatting" },
  { label: "Total Cost", value: "$0", sub: "100% local & free" },
];

import { fetchHealth } from "@/lib/api";

export default function DashboardPage() {
  const [services, setServices] = useState<ServiceStatus[]>(SERVICES);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await fetchHealth();
        setServices((prev) =>
          prev.map((s) => {
            if (s.name === "Ollama LLM") return { ...s, status: health.ollama ? "online" : "offline" };
            if (s.name === "LangGraph") return { ...s, status: health.status === "ok" ? "online" : "offline" };
            return { ...s, status: "online" }; // Assume others are online if backend responds
          })
        );
      } catch (error) {
        setServices((prev) => prev.map((s) => ({ ...s, status: "offline" })));
      }
    };
    checkHealth();
  }, []);

  return (
    <div className="max-w-6xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-[var(--accent-light)] to-purple-400 bg-clip-text text-transparent">
          Dashboard
        </h1>
        <p className="text-[var(--text-secondary)] mt-1">
          System overview and health monitoring
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {STATS.map((stat) => (
          <div
            key={stat.label}
            className="glass rounded-2xl p-5 transition-smooth hover:scale-[1.02]"
          >
            <p className="text-xs text-[var(--text-secondary)] uppercase tracking-wider">
              {stat.label}
            </p>
            <p className="text-2xl font-bold mt-1 text-[var(--text-primary)]">
              {stat.value}
            </p>
            <p className="text-xs text-[var(--text-muted)] mt-1">{stat.sub}</p>
          </div>
        ))}
      </div>

      {/* Services */}
      <div>
        <h2 className="text-lg font-semibold mb-4 text-[var(--text-primary)]">
          Services
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {services.map((svc) => (
            <div
              key={svc.name}
              className="glass rounded-2xl p-5 flex items-center justify-between transition-smooth"
            >
              <div>
                <p className="font-medium text-[var(--text-primary)]">{svc.name}</p>
                <p className="text-xs text-[var(--text-secondary)] mt-0.5">
                  {svc.description}
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={`w-2.5 h-2.5 rounded-full ${
                    svc.status === "online"
                      ? "bg-[var(--success)] pulse-dot"
                      : svc.status === "offline"
                      ? "bg-[var(--error)]"
                      : "bg-[var(--warning)] pulse-dot"
                  }`}
                />
                <span
                  className={`text-xs font-medium ${
                    svc.status === "online"
                      ? "text-[var(--success)]"
                      : svc.status === "offline"
                      ? "text-[var(--error)]"
                      : "text-[var(--warning)]"
                  }`}
                >
                  {svc.status}
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Architecture */}
      <div className="glass rounded-2xl p-6">
        <h2 className="text-lg font-semibold mb-4 text-[var(--text-primary)]">
          Architecture
        </h2>
        <div className="flex flex-wrap gap-3 items-center justify-center text-sm">
          {[
            "User → Next.js",
            "→ FastAPI",
            "→ LangGraph Router",
            "→ RAG / Tools / LLM",
            "→ Ollama",
          ].map((step, i) => (
            <div key={i} className="flex items-center gap-2">
              <span className="px-3 py-1.5 rounded-lg bg-[var(--bg-elevated)] text-[var(--text-secondary)] border border-[var(--border)]">
                {step.replace("→ ", "")}
              </span>
              {i < 4 && (
                <span className="text-[var(--accent-light)]">→</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
