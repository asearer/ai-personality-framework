import { Bell, Search, Settings } from "lucide-react";

export function TopBar() {
  return (
    <div className="h-14 bg-slate-900 border-b border-slate-800 flex items-center justify-between px-4 text-slate-300 shrink-0">
      <div className="flex items-center space-x-4 flex-1">
        <div className="flex items-center space-x-2">
          <span className="px-2 py-1 text-xs font-bold bg-blue-900/50 text-blue-400 border border-blue-800 rounded">
            RESEARCH
          </span>
          <span className="px-2 py-1 text-xs font-bold bg-emerald-900/50 text-emerald-400 border border-emerald-800 rounded">
            GENERAL
          </span>
        </div>
        <div className="h-4 w-px bg-slate-700" />
        <div className="text-sm font-medium">Project: Baseline Perturbation Study</div>
      </div>
      
      <div className="flex-1 flex justify-center">
        <div className="relative w-96">
          <Search className="w-4 h-4 absolute left-3 top-2 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search experiments, sessions, traits..." 
            className="w-full bg-slate-800 border border-slate-700 rounded-md py-1.5 pl-9 pr-4 text-sm focus:outline-none focus:border-blue-500 text-slate-200 placeholder-slate-500"
          />
        </div>
      </div>

      <div className="flex-1 flex justify-end items-center space-x-4">
        <div className="flex items-center space-x-2 text-xs">
          <span className="relative flex h-2 w-2">
            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
            <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
          </span>
          <span className="text-emerald-500 font-medium">System Online</span>
        </div>
        <button className="p-1.5 hover:bg-slate-800 rounded-md text-slate-400 transition-colors">
          <Bell className="w-5 h-5" />
        </button>
        <button className="p-1.5 hover:bg-slate-800 rounded-md text-slate-400 transition-colors">
          <Settings className="w-5 h-5" />
        </button>
        <div className="h-8 w-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500 flex items-center justify-center text-white text-xs font-bold shadow-inner border border-slate-700">
          AR
        </div>
      </div>
    </div>
  );
}
