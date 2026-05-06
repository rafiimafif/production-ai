const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface HealthStatus {
  status: string;
  ollama: boolean;
}

export interface ModelInfo {
  name: string;
  size: number;
  modified_at: string | null;
}

export interface RAGResult {
  answer: string;
  sources: { text: string; score: number | null; metadata: Record<string, string> }[];
}

export async function fetchHealth(): Promise<HealthStatus> {
  const res = await fetch(`${API_BASE}/api/health`, { cache: "no-store" });
  if (!res.ok) throw new Error("Health check failed");
  return res.json();
}

export async function fetchModels(): Promise<ModelInfo[]> {
  const res = await fetch(`${API_BASE}/api/models`, { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to fetch models");
  const data = await res.json();
  return data.models || data;
}

export async function sendChat(
  messages: ChatMessage[],
  model?: string,
  useAgent = false
): Promise<string> {
  const res = await fetch(`${API_BASE}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages, model, use_agent: useAgent }),
  });
  if (!res.ok) throw new Error("Chat request failed");
  const data = await res.json();
  return data.response;
}

export async function queryRAG(
  question: string,
  collection = "default"
): Promise<RAGResult> {
  const res = await fetch(`${API_BASE}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, collection }),
  });
  if (!res.ok) throw new Error("RAG query failed");
  return res.json();
}

export async function uploadDocuments(files: File[]): Promise<{ indexed: string[] }> {
  const formData = new FormData();
  files.forEach((f) => formData.append("files", f));
  const res = await fetch(`${API_BASE}/api/documents`, {
    method: "POST",
    body: formData,
  });
  if (!res.ok) throw new Error("Upload failed");
  return res.json();
}
