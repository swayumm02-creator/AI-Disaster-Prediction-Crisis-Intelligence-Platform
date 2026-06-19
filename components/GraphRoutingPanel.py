import React, { useState } from "react";
import { Network, MapPin, Sliders, RefreshCw, AlertTriangle, ShieldCheck } from "lucide-react";

export default function GraphRoutingPanel() {
  const [roadAlphaBlocked, setRoadAlphaBlocked] = useState(false);
  const [alphaWeight, setAlphaWeight] = useState(50); // Travel time percentage
  const [betaWeight, setBetaWeight] = useState(50);  // Hazard proximity
  const [gammaWeight, setGammaWeight] = useState(50); // Congestion multiplier

  
  const routeAlphaSpeedMultiplier = Math.max(10 - Math.round(gammaWeight / 10), 2);
  const safetyIndex = Math.min(100 - Math.round((betaWeight * 0.8) + (roadAlphaBlocked ? 0 : 35)), 100);
  const estimatedTimeMins = roadAlphaBlocked 
    ? Math.round(18 + (gammaWeight * 0.12)) 
    : Math.round(11 + (gammaWeight * 0.08) + (100 - alphaWeight) * 0.06);

  return (
    <div className="space-y-6" id="graph-routing-pane">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-neo4j">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-indigo-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [11]: Disaster Knowledge Graph System
                </h3>
              </div>
              <Network className="w-4 h-4 text-indigo-400" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Provides millisecond lookup queries across interconnected infrastructure elements in Neo4j. Simulates dynamic road blockages below.
            </p>

            <div className="border border-slate-950 bg-[#04070d] p-4 rounded-xl flex flex-col justify-center min-h-[140px]" id="routing-graph-diagram">
              <div className="flex items-center justify-between text-[10px] font-mono mb-4 text-slate-500 font-bold border-b border-slate-900/60 pb-1.5">
                <span>Core Node Hierarchy</span>
                <span className="text-emerald-400 animate-pulse">Graph connection: Online</span>
              </div>

              <div className="flex items-center justify-between gap-2 max-w-[340px] mx-auto w-full select-none" id="graph-topology-viewport">
                <div className="p-2 border border-slate-800 bg-slate-950 rounded text-center text-[10px] font-mono font-bold" id="node-origin">
                  <MapPin className="w-3.5 h-3.5 text-cyan-400 mx-auto mb-1" />
                  <div>Triage-A</div>
                  <span className="text-[7.5px] text-slate-500 uppercase block mt-0.5">Origin</span>
                </div>

                <div className="flex-1 flex flex-col items-center relative" id="graph-paths-intersections">
                  
                  <div className={`h-0.5 w-full transition-all duration-300 ${roadAlphaBlocked ? "bg-red-500/40 border-dashed border-red-500/20" : "bg-cyan-500"}`}></div>
                  <span className={`text-[8px] font-mono font-semibold py-0.5 px-1.5 rounded my-1 transition-colors ${roadAlphaBlocked ? "text-red-400 bg-red-950/20" : "text-cyan-400 bg-cyan-950/10"}`}>
                    Road Alpha (H-35)
                  </span>

                  
                  <div className={`h-0.5 w-full transition-all duration-300 ${roadAlphaBlocked ? "bg-emerald-500" : "bg-slate-800"}`}></div>
                  <span className={`text-[8px] font-mono font-semibold py-0.5 px-1.5 rounded transition-colors my-1 ${roadAlphaBlocked ? "text-emerald-400 bg-emerald-950/20" : "text-slate-500 bg-slate-950/10"}`}>
                    Road Beta Alt (L-9)
                  </span>
                </div>

                <div className="p-2 border border-slate-800 bg-slate-950 rounded text-center text-[10px] font-mono font-bold" id="node-destination">
                  <MapPin className="w-3.5 h-3.5 text-red-500 mx-auto mb-1" />
                  <div>Central Base</div>
                  <span className="text-[7.5px] text-slate-500 uppercase block mt-0.5">Hospital</span>
                </div>
              </div>
            </div>

            <div className="mt-3 flex items-center justify-between text-xs" id="neo4j-trigger">
              <span className="text-slate-400 font-sans text-xs">Simulate dynamic obstruction:</span>
              <button
                onClick={() => setRoadAlphaBlocked(!roadAlphaBlocked)}
                className={`py-1.5 px-3 rounded-lg font-mono font-bold text-[10px] uppercase transition-all border ${
                  roadAlphaBlocked 
                    ? "bg-red-950/30 border-red-500/40 text-red-400 hover:bg-red-900/10" 
                    : "bg-slate-950 border-slate-800 text-slate-400 hover:text-slate-200"
                }`}
              >
                {roadAlphaBlocked ? "Obstruction Active (Alpha Blocked)" : "Trigger Alpha Landslide"}
              </button>
            </div>
          </div>

          <div className="mt-4 bg-[#04070d] border border-slate-950 rounded-lg p-3 font-mono text-[9.5px]">
            <div className="flex justify-between text-slate-500 uppercase font-bold mb-1.5">
              <span>Cypher Solver Shortest-Path Stream</span>
              <span className="text-indigo-400 font-semibold">SUCCESS</span>
            </div>
            <div className="text-slate-300 space-y-1">
              <div>Selected Corridor: <span className={`font-bold ${roadAlphaBlocked ? "text-emerald-400" : "text-cyan-400"}`}>{roadAlphaBlocked ? "Road_Beta_Alt" : "Road_Alpha"}</span></div>
              <div>Projected EMS Transit Time: <span className="font-bold text-slate-100">{estimatedTimeMins} mins</span></div>
              <div className="text-slate-500 text-[8px]">Query optimized: NONE(road IN relationships(path) WHERE road.status = "BLOCKED")</div>
            </div>
          </div>
        </div>

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-evacuation-planner">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-cyan-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [7]: Autonomous Evacuation Planner
                </h3>
              </div>
              <Sliders className="w-4 h-4 text-cyan-400" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Calculates dynamic getaway routes using Reinforcement Learning (PPO). Adjust algorithm weights below to simulate mathematical escape detours in real-time.
            </p>

            <div className="space-y-4 font-mono text-[10px]">
              <div>
                <div className="flex justify-between text-slate-400 font-semibold mb-1 uppercase">
                  <span>Travel Time Importance (alpha)</span>
                  <span className="text-cyan-400">{alphaWeight}% Weight</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="100"
                  value={alphaWeight}
                  onChange={(e) => setAlphaWeight(parseInt(e.target.value))}
                  className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-400 font-semibold mb-1 uppercase">
                  <span>Hazard Proximity Avoidance (beta)</span>
                  <span className="text-amber-500">{betaWeight}% Weight</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="100"
                  value={betaWeight}
                  onChange={(e) => setBetaWeight(parseInt(e.target.value))}
                  className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
                />
              </div>

              <div>
                <div className="flex justify-between text-slate-400 font-semibold mb-1 uppercase">
                  <span>Road Congestion Penalty (gamma)</span>
                  <span className="text-purple-400">{gammaWeight}% Weight</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="100"
                  value={gammaWeight}
                  onChange={(e) => setGammaWeight(parseInt(e.target.value))}
                  className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
                />
              </div>
            </div>
          </div>

          <div className="mt-4 bg-[#04070d] border border-slate-950 rounded-lg p-3 space-y-2 font-mono text-[10px]" id="evac-calculated-rewards">
            <div className="flex items-center justify-between text-[11px] border-b border-slate-900 pb-1.5 font-bold text-slate-500">
              <span>PPO AGENT OPTIMIZATION METRIC</span>
              <span className="text-cyan-400">STATE_RESOLVED</span>
            </div>
            
            <div className="grid grid-cols-2 gap-2 text-center pb-1">
              <div className="bg-slate-950/60 p-2 border border-slate-900 rounded">
                <span className="text-slate-500 text-[8.5px] block font-bold">ROUTE SAFETY INDEX</span>
                <span className={`text-xs font-bold font-mono ${safetyIndex < 50 ? "text-red-400 animate-pulse" : "text-emerald-400"}`}>
                  {safetyIndex}% Safe
                </span>
              </div>
              <div className="bg-slate-950/60 p-2 border border-slate-900 rounded">
                <span className="text-slate-500 text-[8.5px] block font-bold">ESTIMATED EMS TRANSIT</span>
                <span className="text-xs font-bold font-mono text-cyan-400">
                  {estimatedTimeMins} Minutes
                </span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
}
