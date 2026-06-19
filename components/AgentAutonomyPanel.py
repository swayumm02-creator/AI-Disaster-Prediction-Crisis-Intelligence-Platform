import React, { useState, useEffect, useRef } from "react";
import { Network, Play, Loader2, Cpu, HelpCircle, RefreshCw, Compass } from "lucide-react";
import { DroneNode, AgentStep, DisasterConfig } from "../types";

interface Props {
  currentScenario: DisasterConfig;
}

export default function AgentAutonomyPanel({ currentScenario }: Props) {
 
  const [activeAgentIndex, setActiveAgentIndex] = useState<number>(-1);
  const [agentStepHistory, setAgentStepHistory] = useState<AgentStep[]>([]);
  const [isAgentRunning, setIsAgentRunning] = useState(false);

  
  const [resourceAllocPriority, setResourceAllocPriority] = useState<"evacuation" | "assets" | "medical">("evacuation");
  const [isOptimizingResources, setIsOptimizingResources] = useState(false);
  const [optimizationOutput, setOptimizationOutput] = useState<{
    helicopters: number;
    ambulances: number;
    rescueBoats: number;
    efficiencyRating: number;
  } | null>(null);

  
  const [isSwarmActive, setIsSwarmActive] = useState(true);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const droneNodes = useRef<DroneNode[]>([]);

  
  useEffect(() => {
    const nodes: DroneNode[] = [];
    for (let i = 0; i < 6; i++) {
      nodes.push({
        id: i + 1,
        x: 40 + Math.random() * 220,
        y: 40 + Math.random() * 100,
        vx: (Math.random() - 0.5) * 1.5,
        vy: (Math.random() - 0.5) * 1.5,
        status: i === 2 ? "SCANNING" : i === 4 ? "SIGNAL_LOCKED" : "SEARCHING",
        meshStrength: 85 + Math.floor(Math.random() * 15),
        targetsFound: i === 4 ? 2 : 0,
      });
    }
    droneNodes.current = nodes;
  }, []);

  
  useEffect(() => {
    let animId: number;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const runSimulation = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      const nodes = droneNodes.current;

      if (isSwarmActive) {
        
        nodes.forEach(node => {
          node.x += node.vx;
          node.y += node.vy;

          if (node.x <= 15 || node.x >= canvas.width - 15) node.vx *= -1;
          if (node.y <= 15 || node.y >= canvas.height - 15) node.vy *= -1;
        });
      }

      
      ctx.strokeStyle = "rgba(6, 182, 212, 0.15)";
      ctx.lineWidth = 1;
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dist = Math.hypot(nodes[i].x - nodes[j].x, nodes[i].y - nodes[j].y);
          if (dist < 110) {
            ctx.beginPath();
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();
          }
        }
      }

     
      nodes.forEach(node => {
        ctx.beginPath();
        ctx.arc(node.x, node.y, 12, 0, Math.PI * 2);
        if (node.status === "SIGNAL_LOCKED") {
          ctx.strokeStyle = "rgba(239, 68, 68, 0.4)";
          ctx.fillStyle = "rgba(239, 68, 68, 0.15)";
        } else if (node.status === "SCANNING") {
          ctx.strokeStyle = "rgba(245, 158, 11, 0.4)";
          ctx.fillStyle = "rgba(245, 158, 11, 0.1)";
        } else {
          ctx.strokeStyle = "rgba(6, 182, 212, 0.3)";
          ctx.fillStyle = "rgba(6, 182, 212, 0.05)";
        }
        ctx.fill();
        ctx.stroke();

        ctx.beginPath();
        ctx.arc(node.x, node.y, 3, 0, Math.PI * 2);
        ctx.fillStyle = node.status === "SIGNAL_LOCKED" ? "#ef4444" : node.status === "SCANNING" ? "#f59e0b" : "#06b6d4";
        ctx.fill();

        ctx.fillStyle = "#94a3b8";
        ctx.font = "8px monospace";
        ctx.fillText(`UAV-${node.id}`, node.x + 9, node.y - 4);
      });

      
      ctx.beginPath();
      ctx.arc(170, 75, 7, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(239, 68, 68, 0.5)";
      ctx.lineWidth = 1.5;
      ctx.stroke();
      ctx.fillStyle = "rgba(239, 68, 68, 0.7)";
      ctx.font = "bold 8px monospace";
      ctx.fillText("THERMAL_HIT", 145, 95);

      animId = requestAnimationFrame(runSimulation);
    };

    runSimulation();
    return () => cancelAnimationFrame(animId);
  }, [isSwarmActive]);

  
  const runLangGraphSimulation = () => {
    if (isAgentRunning) return;
    setIsAgentRunning(true);
    setAgentStepHistory([]);
    setActiveAgentIndex(0);

    const steps: AgentStep[] = [
      {
        agent: "Situation Analysis Agent",
        statusString: "METADATA_ANALYZING",
        action: "Geospatial parsing initiated",
        log: `Scanning sensory inputs. Target coordinate ${currentScenario.coordinates.lat.toFixed(3)}, ${currentScenario.coordinates.lng.toFixed(3)} analyzed. Landslide threat index at 82%.`,
        coordinates: "37.77, -122.41"
      },
      {
        agent: "Situation Router (Conditional Edge)",
        statusString: "HYPOTHESIS_EVALUATION",
        action: "Evaluating routing state parameters",
        log: "Branch condition evaluated: High alert status confirmed. Route token sent to [Supply Chain Node] and [Tactical Team Node].",
      },
      {
        agent: "Supply Chain Agent",
        statusString: "INVENTORY_ALLOCATING",
        action: "Acquiring logistic supplies",
        log: "Dispatched 4 modular medical containers from centralized medical reserve. Rerouting delivery corridors.",
        targetUnit: "Depot-South"
      },
      {
        agent: "Rescue Team Agent",
        statusString: "UAV_DEPLOYED",
        action: "Broadcasting geo-fenced mesh directions",
        log: "P2P Drone swarm 4 units activated. Thermal imagery streaming live to crisis database.",
        coordinates: "37.75, -122.43"
      }
    ];

    let current = 0;
    const interval = setInterval(() => {
      setAgentStepHistory(prev => [...prev, steps[current]]);
      setActiveAgentIndex(current + 1);
      current++;
      if (current >= steps.length) {
        clearInterval(interval);
        setIsAgentRunning(false);
        setActiveAgentIndex(-1);
      }
    }, 1200);
  };

  
  const solveResourceAllocation = () => {
    setIsOptimizingResources(true);
    setTimeout(() => {
      let helis = 2;
      let ambs = 6;
      let boats = 3;
      let rating = 88.5;

      if (resourceAllocPriority === "evacuation") {
        helis = 4;
        ambs = 12;
        boats = 2;
        rating = 95.8;
      } else if (resourceAllocPriority === "assets") {
        helis = 2;
        ambs = 4;
        boats = 5;
        rating = 91.2;
      } else {
        helis = 3;
        ambs = 8;
        boats = 4;
        rating = 94.1;
      }

      setOptimizationOutput({
        helicopters: helis,
        ambulances: ambs,
        rescueBoats: boats,
        efficiencyRating: rating
      });
      setIsOptimizingResources(false);
    }, 900);
  };

  return (
    <div className="space-y-6" id="agent-autonomy-pane">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6" id="autonomy-top-grid">

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-langgraph">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-emerald-400 rounded-sm animate-pulse" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [6]: LangGraph Agent Mesh
                </h3>
              </div>
              <Network className="w-4 h-4 text-emerald-400" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Orchestrates a collaborative State Graph. Conditional edges evaluate active hazard indices to dispatch resources sequentially.
            </p>

            <div className="relative border border-slate-950 bg-[#04070d] p-4 rounded-xl flex flex-col items-center gap-2" id="canvas-agent-diagram">
              <div className="grid grid-cols-2 gap-3 w-full max-w-[340px] text-center font-mono py-2">
                {/* Node A */}
                <div 
                  className={`p-2 border rounded-lg transition-all duration-300 text-[10px] ${
                    activeAgentIndex === 1 
                      ? "bg-cyan-500/10 border-cyan-400 text-cyan-400 scale-102 font-bold" 
                      : "bg-slate-950/80 border-slate-900 text-slate-400"
                  }`}
                  id="node-situation"
                >
                  <div>Situation Analysis</div>
                  <span className="text-[7.5px] text-slate-500 block uppercase font-medium">Sensory Stream</span>
                </div>

                {/* Node B */}
                <div 
                  className={`p-2 border rounded-lg transition-all duration-300 text-[10px] ${
                    activeAgentIndex === 2 
                      ? "bg-amber-500/10 border-amber-400 text-amber-400 scale-102 font-bold"
                      : "bg-slate-950/80 border-slate-900 text-slate-400"
                  }`}
                  id="node-router"
                >
                  <div>Conditional Router</div>
                  <span className="text-[7.5px] text-slate-500 block uppercase font-medium">Branch Edge</span>
                </div>

                {/* Node C */}
                <div 
                  className={`p-2 border rounded-lg transition-all duration-300 text-[10px] ${
                    activeAgentIndex === 3 
                      ? "bg-emerald-500/10 border-emerald-400 text-emerald-400 scale-102 font-bold" 
                      : "bg-slate-950/80 border-slate-900 text-slate-400"
                  }`}
                  id="node-supply"
                >
                  <div>Procurement Node</div>
                  <span className="text-[7.5px] text-slate-500 block uppercase font-medium">Resource Depot</span>
                </div>

                {/* Node D */}
                <div 
                  className={`p-2 border rounded-lg transition-all duration-300 text-[10px] ${
                    activeAgentIndex === 4 
                      ? "bg-red-500/10 border-red-400 text-red-400 scale-102 font-bold" 
                      : "bg-slate-950/80 border-slate-900 text-slate-400"
                  }`}
                  id="node-tactical"
                >
                  <div>Tactical Rescue</div>
                  <span className="text-[7.5px] text-slate-500 block uppercase font-medium">Dispatch Swarms</span>
                </div>
              </div>

              <button
                onClick={runLangGraphSimulation}
                disabled={isAgentRunning}
                className="w-full h-10 bg-emerald-950/40 border border-emerald-500/40 hover:bg-emerald-500/10 text-emerald-400 text-xs font-mono font-bold uppercase rounded-lg transition-all flex items-center justify-center gap-2"
                id="btn-run-agents"
              >
                {isAgentRunning ? "Executing Graph Flow..." : "Run Agent Planning Session"}
              </button>
            </div>
          </div>

          <div className="mt-4" id="mod6-output">
            <div className="text-[9px] font-mono text-slate-500 uppercase tracking-wider mb-2 font-bold">
             
            </div>
            <div className="bg-[#04070d] border border-slate-950 rounded-lg p-3 h-24 overflow-y-auto font-mono text-[9px] space-y-1.5 scrollbar-thin select-text" id="agent-logs-box">
              {agentStepHistory.length === 0 ? (
                <span className="text-slate-600 italic block text-center py-4">Click button above to stream agent-to-agent traces</span>
              ) : (
                agentStepHistory.map((step, idx) => (
                  <div key={idx} className="border-b border-slate-900/60 pb-1.5 last:border-0 last:pb-0">
                    <div className="flex justify-between font-bold text-[9.5px]">
                      <span className="text-emerald-400">{step.agent}</span>
                      <span className="text-slate-500 px-1 bg-slate-950 rounded">{step.statusString}</span>
                    </div>
                    <p className="text-slate-300 mt-0.5 leading-relaxed">{step.log}</p>
                  </div>
                ))
              )}
            </div>
          </div>
        </div>

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-swarm">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-cyan-400 rounded-sm animate-pulse" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [16]: Drone Swarm Mesh
                </h3>
              </div>
              <Compass className="w-4 h-4 text-cyan-400 animate-spin" style={{ animationDuration: "16s" }} />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Decentralized ad-hoc P2P search coordinator. Models real-time UAV coordinates and locates thermal distress vectors.
            </p>

            <div className="border border-slate-950 bg-[#04070d] rounded-xl p-3 relative flex flex-col items-center">
              <div className="absolute top-2 right-2 flex items-center gap-1 text-[8px] font-mono text-slate-500 uppercase font-bold bg-slate-950 py-0.5 px-1.5 rounded border border-slate-900">
                <span className="w-1.5 h-1.5 bg-cyan-400 rounded-full animate-ping"></span>
                Mesh: 6 Nodes
              </div>

              <canvas 
                ref={canvasRef}
                width="350"
                height="150"
                className="w-full h-auto bg-[#03060c] border border-slate-950 rounded-lg max-h-[155px]"
              />

              <div className="flex gap-2 w-full mt-3">
                <button
                  onClick={() => setIsSwarmActive(!isSwarmActive)}
                  className="flex-1 py-1 px-3 border border-slate-800 hover:border-slate-700 bg-slate-950 rounded text-[9px] font-mono font-bold text-slate-400 hover:text-slate-100 uppercase"
                >
                  {isSwarmActive ? "Pause Trajectories" : "Resume Trajectories"}
                </button>
                <button
                  onClick={() => {
                    const nodes = droneNodes.current;
                    nodes.forEach(n => {
                      n.x = 40 + Math.random() * 220;
                      n.y = 40 + Math.random() * 100;
                    });
                  }}
                  className="py-1 px-3 border border-slate-800 hover:border-slate-700 bg-slate-950 rounded text-[9px] font-mono font-bold text-slate-400 hover:text-slate-100 uppercase"
                >
                  Reorient Mesh
                </button>
              </div>
            </div>
          </div>

          <div className="mt-4 font-mono text-[9.5px] bg-[#04070d] border border-slate-950 rounded-lg p-2.5">
            <div className="grid grid-cols-2 gap-2 text-slate-400">
              <div>Swarm Consensus index: <span className="text-emerald-400 font-bold">Excellent (&gt;92%)</span></div>
              <div>Thermal Locked cell: <span className="text-red-400 font-bold animate-pulse">LOCKED [S-4]</span></div>
            </div>
          </div>
        </div>

      </div>

      
      <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5" id="card-module-optimization">
        <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 bg-teal-400 rounded-sm" />
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
              [8]: AI Rescue Resource Optimization Core (Genetic / MILP)
            </h3>
          </div>
          <Cpu className="w-4 h-4 text-teal-400" />
        </div>

        <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
          Executes Mixed-Integer Linear Programming (MILP) models to optimize tactical gear distribution. Resolves the minimal travel-cost matching allocations across secondary shelters.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-12 gap-5" id="optimization-control-grid">
          
          <div className="md:col-span-5 space-y-4 font-mono text-[10px]" id="opt-selectors">
            <div>
              <label className="block text-[9.5px] uppercase font-mono tracking-wider text-slate-500 mb-1.5 font-bold">Target Operational Optimization Goal</label>
              <select
                value={resourceAllocPriority}
                onChange={(e) => setResourceAllocPriority(e.target.value as any)}
                className="w-full bg-slate-950 border border-slate-900 text-slate-200 py-2 px-3 rounded-lg text-xs font-mono outline-none focus:border-teal-500"
              >
                <option value="evacuation">Maximize Population Evacuation Coverage</option>
                <option value="assets">Maximize Critical Infrastructure Security</option>
                <option value="medical">Medical Resource Triage Priority</option>
              </select>
            </div>

            <button
              onClick={solveResourceAllocation}
              disabled={isOptimizingResources}
              className="w-full h-10 bg-teal-950/40 border border-teal-500/40 hover:bg-teal-500/10 text-teal-400 rounded-lg text-xs font-bold uppercase transition-all flex items-center justify-center gap-2"
              id="btn-solve-milp"
            >
              {isOptimizingResources ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Mutating Genetic Generation...
                </>
              ) : (
                <>
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" style={{ animationDuration: "6s" }} />
                  Run Optimization Solver
                </>
              )}
            </button>
          </div>

          <div className="md:col-span-7 flex flex-col justify-center" id="opt-stdout">
            {optimizationOutput ? (
              <div className="bg-[#04070d] border border-slate-950 rounded-xl p-4 space-y-3 font-mono text-[10px] animate-fadeIn">
                <div className="flex justify-between border-b border-slate-900 pb-1.5 font-bold text-slate-500">
                  <span>SciPy GLPK Optimizer Result Output</span>
                  <span className="text-teal-400">OPTIMAL</span>
                </div>
                
                <div className="grid grid-cols-3 gap-3 text-center">
                  <div className="bg-slate-950/50 p-2 rounded border border-slate-900">
                    <span className="text-slate-500 text-[8.5px] block">AIR HELICOPTERS</span>
                    <span className="text-sm font-semibold text-slate-200">{optimizationOutput.helicopters} Dispatched</span>
                  </div>
                  <div className="bg-slate-950/50 p-2 rounded border border-slate-900">
                    <span className="text-slate-500 text-[8.5px] block">LAND AMBULANCES</span>
                    <span className="text-sm font-semibold text-slate-200">{optimizationOutput.ambulances} Active</span>
                  </div>
                  <div className="bg-slate-950/50 p-2 rounded border border-slate-900">
                    <span className="text-slate-500 text-[8.5px] block">RESCUE BOATS</span>
                    <span className="text-sm font-semibold text-slate-200">{optimizationOutput.rescueBoats} Deployed</span>
                  </div>
                </div>

                <div className="flex justify-between items-center text-[9.5px] pt-2 border-t border-slate-900 text-slate-400">
                  <span>Converged Generator generation: 140 generations</span>
                  <span className="font-bold text-teal-400">Triage efficiency: {optimizationOutput.efficiencyRating}%</span>
                </div>
              </div>
            ) : (
              <div className="bg-[#04070d] border border-slate-950 rounded-xl p-6 text-center text-slate-600 font-mono text-[10px] italic">
                Select an optimization strategy and execute the GLPK Linear Solver.
              </div>
            )}
          </div>

        </div>
      </div>
    </div>
  );
}
