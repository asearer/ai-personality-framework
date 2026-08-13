import Link from "next/link";
import {
  Microscope,
  LayoutDashboard,
  FlaskConical,
  TestTube,
  Users,
  Database,
  BookOpen,
  Brain,
  Wand2,
  ListTree,
  GitCompare,
  Activity,
  History,
  ShieldAlert,
  Shield,
  ActivitySquare
} from "lucide-react";

export function Sidebar() {
  const sections = [
    {
      title: "Research",
      items: [
        { name: "Command Center", href: "/command-center", icon: LayoutDashboard },
        { name: "Experiments", href: "/experiments", icon: FlaskConical },
        { name: "Simulations", href: "/simulations", icon: TestTube },
        { name: "Cohorts", href: "/cohorts", icon: Users },
        { name: "Datasets", href: "/datasets", icon: Database },
        { name: "Notebook", href: "/notebook", icon: BookOpen },
      ]
    },
    {
      title: "Personality",
      items: [
        { name: "Explorer", href: "/personality/explorer", icon: Brain },
        { name: "Builder", href: "/personality/builder", icon: Wand2 },
        { name: "Traits", href: "/personality/traits", icon: ListTree },
        { name: "Comparison", href: "/personality/comparison", icon: GitCompare },
      ]
    },
    {
      title: "Behavior",
      items: [
        { name: "Live Monitor", href: "/interactions/live", icon: Activity },
        { name: "Interactions", href: "/interactions", icon: History },
        { name: "State Monitor", href: "/interactions/state", icon: ActivitySquare },
        { name: "Memory", href: "/interactions/memory", icon: Database },
      ]
    },
    {
      title: "Safety",
      items: [
        { name: "Safety Monitor", href: "/safety", icon: ShieldAlert },
        { name: "Bias/Fairness", href: "/safety/bias", icon: Shield },
      ]
    }
  ];

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 h-full flex flex-col flex-shrink-0 text-slate-300">
      <div className="p-4 flex items-center space-x-3 text-slate-100 border-b border-slate-800">
        <Microscope className="w-6 h-6 text-blue-500" />
        <span className="font-semibold text-sm tracking-wide">RESEARCH GUI</span>
      </div>
      <div className="flex-1 overflow-y-auto p-4 space-y-6">
        {sections.map((sec) => (
          <div key={sec.title}>
            <div className="text-xs font-semibold text-slate-500 uppercase tracking-wider mb-2">
              {sec.title}
            </div>
            <div className="space-y-1">
              {sec.items.map((item) => {
                const Icon = item.icon;
                return (
                  <Link
                    key={item.name}
                    href={item.href}
                    className="flex items-center space-x-3 px-3 py-2 rounded-md hover:bg-slate-800 hover:text-slate-100 transition-colors text-sm"
                  >
                    <Icon className="w-4 h-4 text-slate-400" />
                    <span>{item.name}</span>
                  </Link>
                );
              })}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
