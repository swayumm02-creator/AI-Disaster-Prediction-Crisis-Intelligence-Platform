import React, { useState, useEffect } from "react";
import { ShieldAlert, Radio, Clock, Activity, CloudRain, Flame, Activity as Wave, Wind } from "lucide-react";
import { DisasterConfig } from "../types";

interface CommandHeaderProps {
  currentScenario: DisasterConfig;
  onScenarioChange: (scenario: DisasterConfig) => void;
  scenarios: DisasterConfig[];
}

export default function CommandHeader({ currentScenario, onScenarioChange, scenarios }: CommandHeaderProps) {
  const [utcTime, setUtcTime] = useState("");
  const [estTime, setEstTime] = useState("");
  const [pingState, setPingState] = useState(14);

  useEffect(() => {
    const updateTimes = () => {
      const now = new Date();
      setUtcTime(now.toUTCString().replace("GMT", "UTC"));
      setEstTime(
        now.toLocaleTimeString("en-US", {
          timeZone: "America/New_York",
          hour12: false,
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
        }) + " EST"
      );
    };

    updateTimes();
    const interval = setInterval(updateTimes, 1000);

    const pingInterval = setInterval(() => {
      setPingState(Math.floor(Math.random() * 8) + 12);
    }, 4000);

    return () => {
      clearInterval(interval);
      clearInterval(pingInterval);
    };
  }, []);

  const getScenarioIcon = (type: string) => {
    switch (type) {
      case "flood":
        return <CloudRain className="w-4 h-4 text-cyan-400" id="icon-scenario-flood" />;
      case "wildfire":
        return <Flame className="w-4 h-4 text-amber-500" id="icon-scenario-fire" />;
      case "hurricane":
        return <Wind className="w-4 h-4 text-teal-400" id="icon-scenario-cane" />;
      default:
        return <Wave className="w-4 h-4 text-emerald-400" id="icon-scenario-default" />;
    }
  };

  return (
    <header className="border-b border-slate-800 bg-[#070b13] px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-4 select-none" id="command-header">
      <div className="flex items-center gap-3" id="header-branding">
        <div className="p-2.5 bg-red-950/40 border border-red-500/40 rounded-lg animate-pulse" id="branding-badge-outer">
          <ShieldAlert className="w-6 h-6 text-red-500 animate-pulse" id="branding-badge-icon" />
        </div>
        <div>
          <div className="flex items-center gap-2" id="title-wrapper">
            <h1 className="text-xl font-sans font-bold tracking-tight text-white uppercase" id="core-platform-title">
              Aegis Prime
            </h1>
            <span className="text-[10px] bg-red-500/10 border border-red-500/30 text-red-400 font-mono px-2 py-0.5 rounded uppercase tracking-widest font-semibold" id="operation-badge">
              Tactical Ops Center
            </span>
          </div>
          <p className="text-xs text-slate-400 font-sans tracking-wide mt-0.5" id="engine-subheading">
            AI Disaster Prediction, Spatial Intelligence & Autonomous Rescue Infrastructure
          </p>
        </div>
      </div>

      <div className="flex flex-wrap items-center gap-4 text-xs font-mono" id="header-metrics-bar">
        
        <div className="flex items-center gap-2 bg-slate-900/80 border border-slate-800 px-3 py-1.5 rounded-lg" id="scenario-selector-container">
          <span className="text-[10px] text-slate-500 font-semibold uppercase tracking-wider" id="scenario-label">
            Target Grid:
          </span>
          <select
            value={currentScenario.id}
            onChange={(e) => {
              const target = scenarios.find((s) => s.id === e.target.value);
              if (target) onScenarioChange(target);
            }}
            className="bg-transparent text-slate-200 outline-none cursor-pointer pr-1 font-mono font-medium focus:text-cyan-400 max-w-[180px]"
            id="scenario-native-select"
          >
            {scenarios.map((scen) => (
              <option key={scen.id} value={scen.id} className="bg-[#0b0f19] text-slate-200">
                {scen.name} ({scen.severity})
              </option>
            ))}
          </select>
          {getScenarioIcon(currentScenario.type)}
        </div>

        
        <div className="flex items-center gap-4 bg-slate-900/40 border border-slate-800 px-3 py-1.5 rounded-lg text-slate-400" id="timekeepers-panel">
          <div className="flex items-center gap-1.5" id="utc-clock-container">
            <Clock className="w-3.5 h-3.5 text-slate-500" id="icon-utc" />
            <span className="text-slate-300 font-semibold tracking-wider" id="utc-display-text">{utcTime || "SYNCING..."}</span>
          </div>
          <div className="hidden sm:block text-slate-600 font-bold" id="clock-divider">|</div>
          <div className="hidden sm:block text-slate-300 font-medium" id="est-display-text">
            {estTime}
          </div>
        </div>

        
        <div className="flex items-center gap-2 bg-slate-900/40 border border-slate-800 px-3 py-1.5 rounded-lg text-emerald-400 font-semibold" id="telemetry-ping-box">
          <Activity className="w-3.5 h-3.5 text-green-500 animate-pulse" id="ping-pulse-icon" />
          <span className="tracking-wide" id="ping-text">{pingState}ms</span>
          <span className="text-[9px] bg-green-500/10 border border-green-500/20 text-green-400 px-1.5 py-0.2 rounded font-semibold" id="ping-status-pill">
            NODE_SECURE
          </span>
        </div>
      </div>
    </header>
  );
}
