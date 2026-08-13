"use client";

import { useState, useEffect } from "react";
import { Zap, Brain, Cpu } from "lucide-react";

type LogEvent = {
  id: string;
  timestamp: string;
  type: string;
  source: string;
  details: string;
  color: string;
};

export default function LiveMonitorPage() {
  const [events, setEvents] = useState<LogEvent[]>([]);
  const [isLive, setIsLive] = useState(true);

  // Mock telemetry stream
  useEffect(() => {
    if (!isLive) return;

    const eventTypes = [
      { type: "USER_ACTION", source: "PerceptionManager", color: "text-blue-400" },
      { type: "APPRAISAL_COMPLETED", source: "AppraisalEngine", color: "text-emerald-400" },
      { type: "EMOTION_UPDATED", source: "EmotionEngine", color: "text-amber-400" },
      { type: "STATE_UPDATED", source: "StateManager", color: "text-purple-400" },
      { type: "MOTIVATION_UPDATED", source: "MotivationEngine", color: "text-rose-400" },
      { type: "BEHAVIOR_SELECTED", source: "BehaviorEngine", color: "text-cyan-400" },
      { type: "AGENT_RESPONSE", source: "LanguageModelProvider", color: "text-slate-200" },
    ];

    let counter = 0;
    const interval = setInterval(() => {
      const typeDef = eventTypes[counter % eventTypes.length];
      
      const newEvent: LogEvent = {
        id: Math.random().toString(36).substr(2, 9),
        timestamp: new Date().toISOString().split("T")[1].substring(0, 12),
        type: typeDef.type,
        source: typeDef.source,
        details: typeDef.type === "AGENT_RESPONSE" 
          ? "Generated 24 tokens in 312ms" 
          : "Processed successfully",
        color: typeDef.color,
      };

      setEvents((prev) => [newEvent, ...prev].slice(0, 50));
      counter++;
    }, 1500);

    return () => clearInterval(interval);
  }, [isLive]);

  return (
    <div className="h-full flex flex-col space-y-4">
      <div className="flex justify-between items-center shrink-0">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Live System Monitor</h1>
          <p className="text-sm text-slate-400 mt-1">Real-time telemetry and interaction trace stream.</p>
        </div>
        <div className="flex space-x-3 items-center">
          <div className="flex items-center space-x-2 mr-4">
            <span className="text-sm font-medium text-slate-400">Stream Status:</span>
            {isLive ? (
              <span className="flex items-center text-emerald-500 text-sm font-bold">
                <span className="animate-pulse mr-2 h-2 w-2 bg-emerald-500 rounded-full"></span>
                LIVE
              </span>
            ) : (
              <span className="flex items-center text-amber-500 text-sm font-bold">
                <span className="mr-2 h-2 w-2 bg-amber-500 rounded-full"></span>
                PAUSED
              </span>
            )}
          </div>
          <button 
            onClick={() => setIsLive(!isLive)}
            className="bg-slate-800 hover:bg-slate-700 text-sm font-medium px-4 py-2 rounded border border-slate-700 transition-colors"
          >
            {isLive ? "Pause Stream" : "Resume Stream"}
          </button>
        </div>
      </div>

      <div className="flex-1 grid grid-cols-3 gap-6 min-h-0">
        {/* Left pane: Active agents / stats */}
        <div className="col-span-1 space-y-6 overflow-y-auto pr-2">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="font-semibold text-white mb-4 flex items-center">
              <Brain className="w-5 h-5 mr-2 text-purple-400" /> Active Session State
            </h3>
            
            <div className="space-y-4">
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Stress Level</span>
                  <span className="text-amber-400 font-mono">0.68</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5">
                  <div className="bg-amber-500 h-1.5 rounded-full" style={{ width: '68%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Arousal</span>
                  <span className="text-rose-400 font-mono">0.82</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5">
                  <div className="bg-rose-500 h-1.5 rounded-full" style={{ width: '82%' }}></div>
                </div>
              </div>
              <div>
                <div className="flex justify-between text-xs mb-1">
                  <span className="text-slate-400">Valence</span>
                  <span className="text-emerald-400 font-mono">0.15</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-1.5">
                  <div className="bg-emerald-500 h-1.5 rounded-full" style={{ width: '15%' }}></div>
                </div>
              </div>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 grid grid-cols-2 gap-4">
              <div>
                <span className="text-xs text-slate-500 block">Active Motivation</span>
                <span className="text-sm font-semibold text-slate-200">Self-Protection</span>
              </div>
              <div>
                <span className="text-xs text-slate-500 block">Behavioral Intent</span>
                <span className="text-sm font-semibold text-slate-200">Defensive</span>
              </div>
            </div>
          </div>

          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
            <h3 className="font-semibold text-white mb-4 flex items-center">
              <Cpu className="w-5 h-5 mr-2 text-blue-400" /> Pipeline Metrics
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                <span className="text-sm text-slate-400">Appraisal Latency</span>
                <span className="text-sm font-mono text-slate-200">12ms</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                <span className="text-sm text-slate-400">Emotion Mapping</span>
                <span className="text-sm font-mono text-slate-200">4ms</span>
              </div>
              <div className="flex justify-between items-center py-2 border-b border-slate-800/50">
                <span className="text-sm text-slate-400">LLM Generation</span>
                <span className="text-sm font-mono text-emerald-400">312ms</span>
              </div>
            </div>
          </div>
        </div>

        {/* Right pane: Event Trace Stream */}
        <div className="col-span-2 bg-slate-900 border border-slate-800 rounded-xl flex flex-col overflow-hidden">
          <div className="bg-slate-800/50 px-4 py-3 border-b border-slate-800 flex justify-between items-center shrink-0">
            <div className="flex items-center space-x-2">
              <Zap className="w-4 h-4 text-amber-400" />
              <span className="font-medium text-sm text-slate-200">Event Trace Stream</span>
            </div>
            <div className="flex space-x-2 text-xs">
              <button className="px-2 py-1 bg-slate-800 hover:bg-slate-700 rounded border border-slate-700 text-slate-300">Filter</button>
              <button className="px-2 py-1 bg-slate-800 hover:bg-slate-700 rounded border border-slate-700 text-slate-300">Clear</button>
            </div>
          </div>
          
          <div className="flex-1 overflow-y-auto p-4 font-mono text-xs">
            {events.length === 0 ? (
              <div className="h-full flex items-center justify-center text-slate-500">
                Waiting for events...
              </div>
            ) : (
              <div className="space-y-1">
                {events.map((evt) => (
                  <div key={evt.id} className="flex group hover:bg-slate-800/50 p-1.5 rounded transition-colors cursor-pointer border border-transparent hover:border-slate-700">
                    <span className="text-slate-500 w-24 shrink-0">{evt.timestamp}</span>
                    <span className={`w-48 shrink-0 font-semibold ${evt.color}`}>
                      {evt.type}
                    </span>
                    <span className="text-slate-400 w-40 shrink-0">[{evt.source}]</span>
                    <span className="text-slate-300 truncate flex-1">{evt.details}</span>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
