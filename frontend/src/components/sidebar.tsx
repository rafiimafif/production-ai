"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const navItems = [
  { href: "/", label: "Dashboard", icon: "◆" },
  { href: "/chat", label: "Chat", icon: "💬" },
  { href: "/documents", label: "Documents", icon: "📄" },
  { href: "/settings", label: "Settings", icon: "⚙️" },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="fixed left-0 top-0 h-full w-64 glass flex flex-col z-50">
      {/* Logo */}
      <div className="p-6 border-b border-[var(--border)]">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-[var(--accent)] to-purple-600 flex items-center justify-center glow">
            <span className="text-white font-bold text-sm">AI</span>
          </div>
          <div>
            <h1 className="text-sm font-semibold text-[var(--text-primary)]">
              Production AI
            </h1>
            <p className="text-xs text-[var(--text-secondary)]">Local Intelligence</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4 space-y-1">
        {navItems.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.href}
              href={item.href}
              id={`nav-${item.label.toLowerCase()}`}
              className={`flex items-center gap-3 px-4 py-2.5 rounded-xl text-sm transition-smooth ${
                isActive
                  ? "bg-[var(--accent)] text-white glow"
                  : "text-[var(--text-secondary)] hover:text-[var(--text-primary)] hover:bg-[var(--bg-elevated)]"
              }`}
            >
              <span className="text-base">{item.icon}</span>
              <span>{item.label}</span>
            </Link>
          );
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-[var(--border)]">
        <div className="glass rounded-xl p-3">
          <div className="flex items-center gap-2 text-xs">
            <span className="w-2 h-2 rounded-full bg-[var(--success)] pulse-dot" />
            <span className="text-[var(--text-secondary)]">System Active</span>
          </div>
          <p className="text-[10px] text-[var(--text-muted)] mt-1">
            Ollama • ChromaDB • LangGraph
          </p>
        </div>
      </div>
    </aside>
  );
}
