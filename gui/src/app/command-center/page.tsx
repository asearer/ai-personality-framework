import { Activity, Server, Users, ShieldAlert, CheckCircle2, AlertCircle } from "lucide-react";

export default function CommandCenterPage() {
  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-white tracking-tight">Research Command Center</h1>
          <p className="text-sm text-slate-400 mt-1">Global overview of all active environments and experiments.</p>
        </div>
        <div className="flex space-x-3">
          <button className="bg-slate-800 hover:bg-slate-700 text-sm font-medium px-4 py-2 rounded border border-slate-700 transition-colors">
            Generate Report
          </button>
          <button className="bg-blue-600 hover:bg-blue-500 text-white text-sm font-medium px-4 py-2 rounded transition-colors">
            New Experiment
          </button>
        </div>
      </div>

      {/* Top Metrics Row */}
      <div className="grid grid-cols-4 gap-4">
        {[
          { title: "Active Agents", value: "1,245", trend: "+12%", icon: Users, color: "text-blue-500" },
          { title: "Avg Latency", value: "412ms", trend: "-5ms", icon: Activity, color: "text-emerald-500" },
          { title: "Active Experiments", value: "14", trend: "3 awaiting review", icon: FlaskConicalIcon, color: "text-purple-500" },
          { title: "Safety Events", value: "3", trend: "Needs attention", icon: ShieldAlert, color: "text-rose-500" },
        ].map((metric) => (
          <div key={metric.title} className="bg-slate-900 border border-slate-800 rounded-xl p-5 hover:border-slate-700 transition-colors">
            <div className="flex justify-between items-start">
              <div>
                <p className="text-sm font-medium text-slate-400">{metric.title}</p>
                <h3 className="text-3xl font-bold text-white mt-2">{metric.value}</h3>
              </div>
              <div className={`p-2 bg-slate-800 rounded-lg ${metric.color}`}>
                <metric.icon className="w-5 h-5" />
              </div>
            </div>
            <div className="mt-4 text-xs font-medium text-slate-500 flex items-center">
              {metric.trend}
            </div>
          </div>
        ))}
      </div>

      <div className="grid grid-cols-3 gap-6">
        {/* Systems Health */}
        <div className="col-span-2 bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-white">System Health</h3>
            <button className="text-xs text-blue-400 hover:text-blue-300">View All</button>
          </div>
          <div className="space-y-4">
            {[
              { name: "Personality Engine API", status: "Healthy", latency: "45ms", icon: CheckCircle2, color: "text-emerald-500" },
              { name: "Gemini Model Provider", status: "Healthy", latency: "850ms", icon: CheckCircle2, color: "text-emerald-500" },
              { name: "Vector Memory Store", status: "Warning", latency: "1,200ms", icon: AlertCircle, color: "text-amber-500" },
              { name: "Event Bus Stream", status: "Healthy", latency: "12ms", icon: CheckCircle2, color: "text-emerald-500" },
            ].map((sys) => (
              <div key={sys.name} className="flex items-center justify-between p-3 rounded-lg bg-slate-800/50 border border-slate-700/50">
                <div className="flex items-center space-x-3">
                  <Server className="w-4 h-4 text-slate-400" />
                  <span className="text-sm font-medium text-slate-200">{sys.name}</span>
                </div>
                <div className="flex items-center space-x-6">
                  <span className="text-xs font-mono text-slate-400">{sys.latency}</span>
                  <div className="flex items-center space-x-1.5 w-24">
                    <sys.icon className={`w-3.5 h-3.5 ${sys.color}`} />
                    <span className={`text-xs ${sys.color}`}>{sys.status}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-slate-900 border border-slate-800 rounded-xl p-5">
          <div className="flex justify-between items-center mb-6">
            <h3 className="font-semibold text-white">Live Activity</h3>
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
            </span>
          </div>
          <div className="space-y-4">
            {[
              { time: "Just now", event: "Model evaluation completed", type: "system" },
              { time: "2m ago", event: "Experiment EXP-092 started", type: "user" },
              { time: "15m ago", event: "Safety policy violation flagged", type: "alert" },
              { time: "1h ago", event: "Personality drift detected (Variant B)", type: "alert" },
              { time: "2h ago", event: "Dataset V3.1 snapshot created", type: "system" },
            ].map((activity, i) => (
              <div key={i} className="flex space-x-3">
                <div className="flex flex-col items-center">
                  <div className={`w-2 h-2 rounded-full mt-1.5 ${
                    activity.type === 'alert' ? 'bg-rose-500' :
                    activity.type === 'user' ? 'bg-blue-500' : 'bg-slate-500'
                  }`} />
                  {i !== 4 && <div className="w-px h-full bg-slate-800 mt-2" />}
                </div>
                <div className="pb-4">
                  <p className="text-sm text-slate-200">{activity.event}</p>
                  <p className="text-xs text-slate-500 mt-0.5">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function FlaskConicalIcon(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M10 2v7.31" />
      <path d="M14 9.3V1.99" />
      <path d="M8.5 2h7" />
      <path d="M14 9.3a6.5 6.5 0 1 1-4 0" />
      <line x1="5.52" x2="18.48" y1="16" y2="16" />
    </svg>
  )
}
