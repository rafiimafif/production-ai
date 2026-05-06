"use client";

import { useState, useCallback } from "react";

export default function DocumentsPage() {
  const [files, setFiles] = useState<File[]>([]);
  const [indexed, setIndexed] = useState<string[]>([]);
  const [isUploading, setIsUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const dropped = Array.from(e.dataTransfer.files);
    setFiles((prev) => [...prev, ...dropped]);
  }, []);

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles((prev) => [...prev, ...Array.from(e.target.files!)]);
    }
  };

  const removeFile = (index: number) => {
    setFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const handleUpload = async () => {
    if (files.length === 0) return;
    setIsUploading(true);

    try {
      const formData = new FormData();
      files.forEach((f) => formData.append("files", f));

      const res = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"}/api/documents`,
        { method: "POST", body: formData }
      );
      const data = await res.json();
      setIndexed((prev) => [...prev, ...(data.indexed || [])]);
      setFiles([]);
    } catch {
      alert("Upload failed. Ensure the backend is running.");
    } finally {
      setIsUploading(false);
    }
  };

  const formatSize = (bytes: number) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      {/* Header */}
      <div>
        <h1 className="text-3xl font-bold bg-gradient-to-r from-[var(--accent-light)] to-purple-400 bg-clip-text text-transparent">
          Documents
        </h1>
        <p className="text-[var(--text-secondary)] text-sm mt-1">
          Upload files to build your RAG knowledge base
        </p>
      </div>

      {/* Drop zone */}
      <div
        onDragOver={(e) => {
          e.preventDefault();
          setDragOver(true);
        }}
        onDragLeave={() => setDragOver(false)}
        onDrop={handleDrop}
        className={`glass rounded-2xl p-10 text-center transition-smooth cursor-pointer ${
          dragOver ? "border-[var(--accent)] bg-[var(--accent-glow)]" : ""
        }`}
        onClick={() => document.getElementById("file-input")?.click()}
      >
        <input
          id="file-input"
          type="file"
          multiple
          onChange={handleFileSelect}
          className="hidden"
          accept=".pdf,.txt,.md,.docx,.csv,.json"
        />
        <div className="space-y-3">
          <div className="w-14 h-14 rounded-2xl bg-[var(--bg-elevated)] flex items-center justify-center mx-auto">
            <span className="text-2xl">📁</span>
          </div>
          <p className="text-[var(--text-primary)] font-medium">
            Drop files here or click to browse
          </p>
          <p className="text-xs text-[var(--text-muted)]">
            Supports PDF, TXT, MD, DOCX, CSV, JSON
          </p>
        </div>
      </div>

      {/* Staged files */}
      {files.length > 0 && (
        <div className="space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-sm font-medium text-[var(--text-primary)]">
              Ready to index ({files.length} files)
            </h2>
            <button
              id="upload-btn"
              onClick={handleUpload}
              disabled={isUploading}
              className="px-4 py-2 rounded-xl bg-[var(--accent)] text-white text-sm font-medium transition-smooth hover:opacity-90 disabled:opacity-40 glow"
            >
              {isUploading ? "Indexing..." : "Upload & Index"}
            </button>
          </div>
          <div className="space-y-2">
            {files.map((f, i) => (
              <div
                key={`${f.name}-${i}`}
                className="glass rounded-xl px-4 py-3 flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <span className="text-base">📄</span>
                  <div>
                    <p className="text-sm text-[var(--text-primary)]">{f.name}</p>
                    <p className="text-xs text-[var(--text-muted)]">
                      {formatSize(f.size)}
                    </p>
                  </div>
                </div>
                <button
                  onClick={() => removeFile(i)}
                  className="text-[var(--text-muted)] hover:text-[var(--error)] transition-smooth text-sm"
                >
                  ✕
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Indexed documents */}
      {indexed.length > 0 && (
        <div className="space-y-3">
          <h2 className="text-sm font-medium text-[var(--success)]">
            ✓ Indexed Documents ({indexed.length})
          </h2>
          <div className="space-y-2">
            {indexed.map((name, i) => (
              <div
                key={`${name}-${i}`}
                className="glass rounded-xl px-4 py-3 flex items-center gap-3"
              >
                <span className="w-2 h-2 rounded-full bg-[var(--success)]" />
                <p className="text-sm text-[var(--text-primary)]">{name}</p>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
