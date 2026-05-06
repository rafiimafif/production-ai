import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/sidebar";

const inter = Inter({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Production AI — Local Intelligence Platform",
  description:
    "Production-grade AI system with local LLMs, RAG, agent orchestration, and full observability. Total cost: $0.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className={`${inter.variable} h-full antialiased`}>
      <body className="min-h-full flex gradient-bg">
        <Sidebar />
        <main className="flex-1 ml-64 p-6 overflow-auto">{children}</main>
      </body>
    </html>
  );
}
