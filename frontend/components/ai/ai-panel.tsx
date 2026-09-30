"use client";

import React, { useState } from "react";
import { Bot, Send, ShieldCheck, Sparkles, CheckCircle, ArrowRight, CornerDownLeft, AlertCircle } from "lucide-react";

interface AiPanelProps {
  riskData: any;
  onAdvisoryReview?: () => void;
  onGenerateReport?: () => void;
}

export default function AiPanel({ riskData, onAdvisoryReview, onGenerateReport }: AiPanelProps) {
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState<any[]>([
    {
      role: "assistant",
      content: (
        "**SUPERVISOR AGENT READY** • *Zero-LLM Arithmetic Active*\n\n" +
        "Cyclone DEMO-01 is currently 65km offshore tracking NW at 18 km/h. " +
        "Deterministic models estimate **HIGH RISK (0.76)** driven by 2.5m storm surge and 180mm surface runoff. " +
        "3 coastal hospitals and 14 road segments show elevated inundation exposure."
      ),
      toolsCalled: ["get_current_cyclone_state", "get_risk_map", "get_infrastructure_exposure"],
    },
  ]);
  const [isLoading, setIsLoading] = useState(false);

  const sampleQuestions = [
    "Which hospitals could become inaccessible?",
    "Show roads likely to flood.",
    "What happens if rainfall increases by 30%?",
    "Which shelters have insufficient capacity?",
  ];

  const handleSend = async (textToSend?: string) => {
    const prompt = textToSend || query;
    if (!prompt.trim() || isLoading) return;

    const userMsg = { role: "user", content: prompt };
    setMessages((prev) => [...prev, userMsg]);
    setQuery("");
    setIsLoading(true);

    try {
      const res = await fetch("/api/v1/agent/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: prompt, cyclone_id: "CYCLONE-DEMO-01" }),
      });
      const data = await res.json();

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: data.response || "No response received.",
          toolsCalled: data.tools_called || [],
          validation: data.output_validation,
        },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Backend API offline or unreachable. Ensure FastAPI backend is running on port 8000.",
          toolsCalled: [],
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  const contributions = [
    { label: "Storm surge", pct: 28, color: "bg-cyan-500" },
    { label: "Heavy rainfall", pct: 23, color: "bg-blue-500" },
    { label: "Low elevation", pct: 18, color: "bg-amber-500" },
    { label: "Road exposure", pct: 16, color: "bg-red-500" },
    { label: "Power grid exposure", pct: 15, color: "bg-purple-500" },
  ];

  return (
    <div className="flex flex-col h-full bg-[#0b101c] border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
      {/* Top Assessment Header */}
      <div className="p-4 border-b border-slate-800 bg-[#0d1424]">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Bot className="w-5 h-5 text-cyan-400" />
            <span className="font-bold text-sm text-slate-100 font-mono tracking-wide">
              SUPERVISOR AGENT
            </span>
          </div>
          <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-amber-950/80 text-amber-400 border border-amber-800 font-bold">
            HIGH RISK — 0.76
          </span>
        </div>

        {/* Explainable AI Contribution Bars */}
        <div className="mt-3 space-y-1.5 font-mono text-[11px]">
          <div className="text-slate-400 text-[10px] uppercase font-bold flex justify-between">
            <span>Primary Contributing Risk Drivers</span>
            <span>Zero-LLM Weights</span>
          </div>
          {contributions.map((c) => (
            <div key={c.label}>
              <div className="flex justify-between text-slate-300 text-[10px] mb-0.5">
                <span>{c.label}</span>
                <span>{c.pct}%</span>
              </div>
              <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                <div className={`h-full rounded-full ${c.color}`} style={{ width: `${c.pct}%` }} />
              </div>
            </div>
          ))}
        </div>

        {/* One-Click Action Buttons */}
        <div className="mt-3 pt-3 border-t border-slate-800/80 flex items-center space-x-2">
          <button
            onClick={onAdvisoryReview}
            className="flex-1 bg-amber-600 hover:bg-amber-500 text-slate-950 font-bold py-1.5 px-2 rounded text-xs font-mono transition flex items-center justify-center space-x-1 shadow"
          >
            <span>REVIEW DRAFT ADVISORY</span>
          </button>
          <button
            onClick={onGenerateReport}
            className="flex-1 bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium py-1.5 px-2 rounded text-xs font-mono transition flex items-center justify-center space-x-1 border border-slate-700"
          >
            <span>SITUATION REPORT</span>
          </button>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-3 font-sans text-xs">
        {messages.map((m, idx) => (
          <div
            key={idx}
            className={`p-3 rounded-lg leading-relaxed ${
              m.role === "user"
                ? "bg-cyan-950/40 border border-cyan-800/60 text-cyan-100 ml-6"
                : "bg-slate-900 border border-slate-800 text-slate-200 mr-2"
            }`}
          >
            {m.role === "assistant" && m.toolsCalled && m.toolsCalled.length > 0 && (
              <div className="mb-2 pb-1.5 border-b border-slate-800 flex flex-wrap gap-1 items-center">
                <span className="text-[10px] font-mono text-cyan-400">TOOLS:</span>
                {m.toolsCalled.map((t: string) => (
                  <span
                    key={t}
                    className="text-[9px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300 border border-slate-700"
                  >
                    {t}()
                  </span>
                ))}
              </div>
            )}
            <div className="whitespace-pre-wrap">{m.content}</div>
          </div>
        ))}
        {isLoading && (
          <div className="p-3 bg-slate-900 border border-slate-800 rounded-lg text-slate-400 animate-pulse font-mono text-xs flex items-center space-x-2">
            <span className="w-2 h-2 rounded-full bg-cyan-400 animate-ping" />
            <span>Agent executing bounded deterministic tool loop...</span>
          </div>
        )}
      </div>

      {/* Pre-set questions chips */}
      <div className="p-2 border-t border-slate-800/80 bg-slate-950/60 overflow-x-auto flex space-x-1.5">
        {sampleQuestions.map((q, i) => (
          <button
            key={i}
            onClick={() => handleSend(q)}
            className="whitespace-nowrap px-2 py-1 rounded-full bg-slate-900 hover:bg-slate-800 text-[10px] text-slate-300 border border-slate-800 font-mono transition"
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input box */}
      <div className="p-3 border-t border-slate-800 bg-[#0d1424] flex items-center space-x-2">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleSend()}
          placeholder="Ask AI Supervisor (e.g. 'Which hospitals could flood?')"
          className="flex-1 bg-slate-900 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500 font-mono"
        />
        <button
          onClick={() => handleSend()}
          disabled={isLoading || !query.trim()}
          className="p-2 bg-cyan-600 hover:bg-cyan-500 disabled:opacity-40 text-slate-950 font-bold rounded-lg transition"
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
}
