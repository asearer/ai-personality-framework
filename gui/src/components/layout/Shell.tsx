import { Sidebar } from "./Sidebar";
import { TopBar } from "./TopBar";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-screen w-screen overflow-hidden bg-slate-950 text-slate-300 font-sans">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <TopBar />
        <main className="flex-1 overflow-y-auto p-6 relative">
          {children}
        </main>
      </div>
    </div>
  );
}
