import React, { useState, useEffect, useRef } from "react";
import { 
  ShieldAlert, Radio, Clock, Activity, CloudRain, Flame, Wind, 
  MapPin, Play, RefreshCw, Send, Sliders, ChevronRight, Check, 
  Layers, Terminal, BookOpen, AlertTriangle, Cpu, Network, Compass, 
  Search, FileText, UserCheck, ShieldCheck, DollarSign,
  TrendingDown, Map, Loader2, Copy
} from "lucide-react";
import CommandHeader from "./components/CommandHeader";
import { MODULE_BLUEPRINTS } from "./data/blueprints";
import { 
  DisasterConfig, IngestedLog, AgentStep, DroneNode, 
  SimulationState, OptimizationResult 
} from "./types";


import GisIngestionPanel from "./components/GisIngestionPanel";
import PredictiveTwinPanel from "./components/PredictiveTwinPanel";
import AgentAutonomyPanel from "./components/AgentAutonomyPanel";
import GraphRoutingPanel from "./components/GraphRoutingPanel";
import NlpCopilotPanel from "./components/NlpCopilotPanel";
import AlertsRecoveryPanel from "./components/AlertsRecoveryPanel";


const SCENARIOS: DisasterConfig[] = [
  {
    id: "scen-valleypoint",
    name: "Valley Point Basin Flash Flood",
    type: "flood",
    severity: "CAT-4",
    coordinates: { lat: 37.7749, lng: -122.4194 },
    activeThreatCount: 14,
    sheltersOpen: 6,
  },
  {
    id: "scen-sierra",
    name: "Sierra Foothills Wildfire",
    type: "wildfire",
    severity: "V-H",
    coordinates: { lat: 34.0522, lng: -118.2437 },
    activeThreatCount: 22,
    sheltersOpen: 9,
  },
  {
    id: "scen-galveston",
    name: "Galveston Harbor Storm Surge",
    type: "hurricane",
    severity: "CAT-5",
    coordinates: { lat: 29.3013, lng: -94.7977 },
    activeThreatCount: 31,
    sheltersOpen: 15,
  }
];

export default function App() {
  
  const [currentScenario, setCurrentScenario] = useState<DisasterConfig>(SCENARIOS[0]);

  
  const [activeTab, setActiveTab] = useState<"cockpit" | "blueprints">("cockpit");
  const [cockpitSubTab, setCockpitSubTab] = useState<
    "ingestion-gis" | "predictive-twin" | "agent-autonomy" | "graph-routing" | "nlp-copilot" | "alerts-recovery"
  >("ingestion-gis");

  
  const [selectedBlueprintId, setSelectedBlueprintId] = useState<number>(1);
  const [searchQuery, setSearchQuery] = useState("");
  const [copyFeedback, setCopyFeedback] = useState<string | null>(null);

  
  const [ingestionLogs, setIngestionLogs] = useState<IngestedLog[]>([]);
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestionSource, setIngestionSource] = useState<"SAR" | "IoT" | "SocialMedia">("IoT");
  const [mockSensorInput, setMockSensorInput] = useState("4.85");

  
  const [swipePosition, setSwipePosition] = useState<number>(50);

  
  const [simulationState, setSimulationState] = useState<SimulationState>({
    precipitation: 45, 
    powerGridCapacity: 88, 
    roadCongestion: 35, 
    hazardSpreadRadius: 420, 
  });

  
  const structuralDamageFactor = Math.min((simulationState.precipitation * 1.5) + (simulationState.hazardSpreadRadius * 0.05), 100);
  const projectedLossMillions = ((structuralDamageFactor * 2.4) + ((100 - simulationState.powerGridCapacity) * 1.8)).toFixed(2);
  const systemStressPct = Math.min(Math.round((simulationState.precipitation * 0.8) + (simulationState.roadCongestion * 0.6) + (100 - simulationState.powerGridCapacity)), 100);
  const evacuationFlowRate = Math.max(Math.round(800 - (simulationState.roadCongestion * 6) - (simulationState.precipitation * 3)), 50);

  
  const [activeAgentIndex, setActiveAgentIndex] = useState<number>(-1);
  const [agentStepHistory, setAgentStepHistory] = useState<AgentStep[]>([]);
  const [isAgentRunning, setIsAgentRunning] = useState(false);


  const [isSwarmActive, setIsSwarmActive] = useState(true);
  const [roadAlphaBlocked, setRoadAlphaBlocked] = useState(false);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const droneNodes = useRef<DroneNode[]>([]);

  
  const [chatMessages, setChatMessages] = useState<{ role: "user" | "model"; content: string; mode?: string }[]>([
    {
      role: "model",
      content: `### 🚨 Aegis Strategic Copilot Active\n\nI am the central crisis analysis co-ordinator. Ask me to formulate alternate evacuation routes, evaluate H3 spatial threat zones, detail the current multi-agent mesh planning state, or design responsive disaster operations.\n\n*Select a conversation preset below or type a custom command.*`
    }
  ]);
  const [chatInput, setChatInput] = useState("");
  const [isChatLoading, setIsChatLoading] = useState(false);
  const chatBottomRef = useRef<HTMLDivElement | null>(null);

  
  useEffect(() => {
    const nodes: DroneNode[] = [];
    for (let i = 0; i < 6; i++) {
      nodes.push({
        id: i + 1,
        x: 40 + Math.random() * 220,
        y: 40 + Math.random() * 120,
        vx: (Math.random() - 0.5) * 1.2,
        vy: (Math.random() - 0.5) * 1.2,
        status: i === 2 ? "SCANNING" : i === 4 ? "SIGNAL_LOCKED" : "SEARCHING",
        meshStrength: 85 + Math.floor(Math.random() * 15),
        targetsFound: i === 4 ? 2 : 0,
      });
    }
    droneNodes.current = nodes;

    setIngestionLogs([
      {
        timestamp: new Date(Date.now() - 3600000).toLocaleTimeString(),
        source: "Sentinel SAR Image",
        id: "IGN-009827",
        type: "Raster Data",
        status: "SUCCESS",
        payload: { bands: ["VV", "VH"], resolution: "10m", raw_url: "s3://sentinel-1/tile_1982a.tiff" }
      },
      {
        timestamp: new Date(Date.now() - 1800000).toLocaleTimeString(),
        source: "River Gauge IoT",
        id: "IGN-009828",
        type: "Sensor Float",
        status: "INGESTED",
        payload: { station_id: "RVG-12", flood_tide_meters: 3.82, battery_charging_voltage: "12.4V" }
      }
    ]);
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
        // Update positions and bounce off boundaries
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
        ctx.arc(node.x, node.y, 14, 0, Math.PI * 2);
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
        ctx.lineWidth = 1.5;
        ctx.fill();
        ctx.stroke();

        // Core Drone Dot
        ctx.beginPath();
        ctx.arc(node.x, node.y, 4, 0, Math.PI * 2);
        ctx.fillStyle = node.status === "SIGNAL_LOCKED" ? "#ef4444" : node.status === "SCANNING" ? "#f59e0b" : "#06b6d4";
        ctx.fill();

        // Print Node Identifier labels
        ctx.fillStyle = "#94a3b8";
        ctx.font = "8px monospace";
        ctx.fillText(`UAV-${node.id}`, node.x + 10, node.y - 6);
        ctx.fillStyle = node.status === "SIGNAL_LOCKED" ? "#fca5a5" : "#64748b";
        ctx.fillText(node.status, node.x + 10, node.y + 4);
      });

      // Render thermal anomaly coordinate targets inside search zone
      ctx.beginPath();
      ctx.arc(180, 85, 8, 0, Math.PI * 2);
      ctx.strokeStyle = "rgba(239, 68, 68, 0.6)";
      ctx.lineWidth = 2;
      ctx.stroke();
      
      ctx.fillStyle = "rgba(239, 68, 68, 0.8)";
      ctx.font = "bold 8px system-ui";
      ctx.fillText("THERMAL_HIT", 155, 105);

      animId = requestAnimationFrame(runSimulation);
    };

    runSimulation();
    return () => cancelAnimationFrame(animId);
  }, [isSwarmActive]);

  // Autoscroll chat terminal to bottom
  useEffect(() => {
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, isChatLoading]);

  // Handler 1: Trigger Multi-Source Ingestion telemetry pulse simulation
  const handlePulseDataFusion = () => {
    setIsIngesting(true);
    const mockId = `IGN-00${Math.floor(Math.random() * 900000) + 100000}`;
    const timestamp = new Date().toLocaleTimeString();

    setTimeout(() => {
      let createdPayload: any;
      if (ingestionSource === "SAR") {
        createdPayload = {
          satellite: "Sentinel-2B",
          spatial_resolution_meters: 10,
          lat_center: currentScenario.coordinates.lat.toFixed(4),
          lng_center: currentScenario.coordinates.lng.toFixed(4),
          bands: ["Red-Edge", "NIR", "VV_POL"]
        };
      } else if (ingestionSource === "IoT") {
        createdPayload = {
          station_id: "FLG-B-S4",
          river_level_meters: parseFloat(mockSensorInput) || 3.12,
          sensor_voltage: "3.28V",
          telemetry_freq_seconds: 60,
          status: parseFloat(mockSensorInput) > 4.5 ? "ABOVE_FLOOD_STAGE" : "OPERATIONAL"
        };
      } else {
        createdPayload = {
          user_handle: "@emergency_alert_net",
          timestamp_epoch: Date.now(),
          parsed_geolocation: [currentScenario.coordinates.lat, currentScenario.coordinates.lng],
          extracted_text: "Bridge at Sector-4 totally submerged. Water is rushing, roads isolated!",
          confidence: 0.94,
          pydantic_classification: "DISTRESS_URGENT"
        };
      }

      const freshLog: IngestedLog = {
        timestamp,
        source: ingestionSource === "SAR" ? "Sentinel SAR" : ingestionSource === "IoT" ? "IoT River Gauge" : "Social Feed",
        id: mockId,
        type: ingestionSource === "SAR" ? "Raster Stack Image" : ingestionSource === "IoT" ? "Sensor Float Metric" : "NLP Distress Stream",
        status: "SUCCESS",
        payload: createdPayload
      };

      setIngestionLogs(prev => [freshLog, ...prev].slice(0, 5));
      setIsIngesting(false);
    }, 1200);
  };

  // Handler 6: Autonomous LangGraph multi-agent simulation step machine
  const runLangGraphSimulation = () => {
    if (isAgentRunning) return;
    setIsAgentRunning(true);
    setAgentStepHistory([]);
    setActiveAgentIndex(0);

    const steps = [
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
    }, 1800);
  };

  // Handler 10: RAG Copilot message processing
  const handleSendMessage = async (customMessage?: string) => {
    const textToSend = customMessage || chatInput;
    if (!textToSend.trim() || isChatLoading) return;

    setChatInput("");
    setChatMessages(prev => [...prev, { role: "user", content: textToSend }]);
    setIsChatLoading(true);

    try {
      const response = await fetch("/api/copilot", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: textToSend,
          context: `Target: ${currentScenario.name}, Type: ${currentScenario.type}, Severity: ${currentScenario.severity}, SystemStress: ${systemStressPct}%, Congestion: ${simulationState.roadCongestion}%, FloodGauge: ${simulationState.precipitation}mm/hr`,
          history: chatMessages.slice(-6).map(m => ({ role: m.role, content: m.content }))
        })
      });

      const data = await response.json();
      if (response.ok) {
        setChatMessages(prev => [...prev, { role: "model", content: data.reply, mode: data.mode }]);
      } else {
        setChatMessages(prev => [...prev, { role: "model", content: `### Copy Command Error\n\nCould not fetch response: ${data.error || "Unknown server failure"}` }]);
      }
    } catch (err: any) {
      console.error(err);
      setChatMessages(prev => [...prev, { role: "model", content: `### Server Communication Failure\n\nFailed to dispatch prompt. Ensure your Express/Vite full-stack environment has compiled correctly.` }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  // Helper copy blueprint snippet to clipboard
  const handleCopyCode = (code: string, id: number) => {
    navigator.clipboard.writeText(code);
    setCopyFeedback(id.toString());
    setTimeout(() => setCopyFeedback(null), 2000);
  };

  // Handle preset clicks in Chat interface
  const handlePresetClick = (presetText: string) => {
    handleSendMessage(presetText);
  };

  // Query filter blueprint matches
  const filteredBlueprints = MODULE_BLUEPRINTS.filter(b => 
    b.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    b.category.toLowerCase().includes(searchQuery.toLowerCase()) ||
    b.techStack.some(t => t.toLowerCase().includes(searchQuery.toLowerCase()))
  );

  const selectedBlueprint = MODULE_BLUEPRINTS.find(b => b.id === selectedBlueprintId) || MODULE_BLUEPRINTS[0];

  return (
    <div className="min-h-screen bg-[#03070d] text-slate-100 flex flex-col font-sans" id="aegis-command-root">
      
      {/* Platform Header Navigation Integration */}
      <CommandHeader 
        currentScenario={currentScenario} 
        onScenarioChange={setCurrentScenario} 
        scenarios={SCENARIOS} 
      />

      {/* Main Command Workspace */}
      <main className="flex-1 max-w-[1920px] mx-auto w-full grid grid-cols-1 lg:grid-cols-12 overflow-hidden" id="workspace-grid">
        
        {/* Left/Middle Action Sandbox Frame Panel */}
        <section className="lg:col-span-8 p-6 flex flex-col gap-6 overflow-y-auto max-h-[calc(100vh-80px)] border-r border-slate-900" id="sandbox-pane">
          
          {/* Main Top Navigation Tabs Selector */}
          <div className="flex border-b border-slate-900 bg-slate-950/60 p-1.5 rounded-xl gap-2 select-none" id="dashboard-navbar">
            <button
              onClick={() => setActiveTab("cockpit")}
              className={`flex-1 py-3 text-xs uppercase tracking-wider font-semibold font-mono rounded-lg transition-all duration-300 flex items-center justify-center gap-2 ${
                activeTab === "cockpit" 
                  ? "bg-cyan-500/10 border border-cyan-500/30 text-cyan-400" 
                  : "text-slate-400 hover:text-slate-100 border border-transparent"
              }`}
              id="nav-cockpit-tab"
            >
              <Compass className="w-4 h-4" />
              Crisis Command Cockpit
            </button>
            <button
              onClick={() => setActiveTab("blueprints")}
              className={`flex-1 py-3 text-xs uppercase tracking-wider font-semibold font-mono rounded-lg transition-all duration-300 flex items-center justify-center gap-2 ${
                activeTab === "blueprints" 
                  ? "bg-cyan-500/10 border border-cyan-500/30 text-cyan-400" 
                  : "text-slate-400 hover:text-slate-100 border border-transparent"
              }`}
              id="nav-blueprints-tab"
            >
              <BookOpen className="w-4 h-4" />
              Architecture Blueprints ({MODULE_BLUEPRINTS.length})
            </button>
          </div>

          {/* TAB 1 CONTENT: Live Tactical Response Command Cockpit */}
          {activeTab === "cockpit" && (
            <div className="flex flex-col gap-6 animate-fadeIn" id="cockpit-container">
              
              {/* Category selector for all 18 System Capabilities */}
              <div className="grid grid-cols-2 md:grid-cols-6 gap-2 bg-slate-950/40 p-2 rounded-xl border border-slate-900 animate-fadeIn" id="cockpit-sub-navbar">
                <button
                  onClick={() => setCockpitSubTab("ingestion-gis")}
                  className={`p-3 rounded-lg border text-center transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                    cockpitSubTab === "ingestion-gis"
                      ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-400 font-bold"
                      : "bg-slate-900/40 border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                  id="subtab-ingest-gis"
                >
                  <span className="text-[10px] font-mono uppercase">1. Ingestion & GIS</span>
                  <span className="text-[8px] text-slate-500 block uppercase font-semibold">Systems 1, 2, 4, 15</span>
                </button>
                <button
                  onClick={() => setCockpitSubTab("predictive-twin")}
                  className={`p-3 rounded-lg border text-center transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                    cockpitSubTab === "predictive-twin"
                      ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-400 font-bold"
                      : "bg-slate-900/40 border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                  id="subtab-pred-twin"
                >
                  <span className="text-[10px] font-mono uppercase">2. AI & Twin</span>
                  <span className="text-[8px] text-slate-500 block uppercase font-semibold">Systems 3, 5, 13, 14</span>
                </button>
                <button
                  onClick={() => setCockpitSubTab("agent-autonomy")}
                  className={`p-3 rounded-lg border text-center transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                    cockpitSubTab === "agent-autonomy"
                      ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-400"
                      : "bg-slate-900/40 border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                  id="subtab-autonomy"
                >
                  <span className="text-[10px] font-mono uppercase">3. Multi-Agents</span>
                  <span className="text-[8px] text-slate-500 block uppercase font-semibold">Systems 6, 8, 16</span>
                </button>
                <button
                  onClick={() => setCockpitSubTab("graph-routing")}
                  className={`p-3 rounded-lg border text-center transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                    cockpitSubTab === "graph-routing"
                      ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-400 font-bold"
                      : "bg-slate-900/40 border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                  id="subtab-graphs"
                >
                  <span className="text-[10px] font-mono uppercase">4. Graphs & Routes</span>
                  <span className="text-[8px] text-slate-500 block uppercase font-semibold">Systems 7, 11</span>
                </button>
                <button
                  onClick={() => setCockpitSubTab("nlp-copilot")}
                  className={`p-3 rounded-lg border text-center transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                    cockpitSubTab === "nlp-copilot"
                      ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-400 font-bold"
                      : "bg-slate-900/40 border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                  id="subtab-nlp"
                >
                  <span className="text-[10px] font-mono uppercase font-bold">5. NLP Copilot</span>
                  <span className="text-[8px] text-slate-500 block uppercase font-semibold">Systems 9, 10</span>
                </button>
                <button
                  onClick={() => setCockpitSubTab("alerts-recovery")}
                  className={`p-3 rounded-lg border text-center transition-all duration-200 flex flex-col items-center justify-center gap-1.5 ${
                    cockpitSubTab === "alerts-recovery"
                      ? "bg-cyan-500/10 border-cyan-500/40 text-cyan-400 font-bold"
                      : "bg-slate-900/40 border-transparent text-slate-400 hover:text-slate-200"
                  }`}
                  id="subtab-recovery"
                >
                  <span className="text-[10px] font-mono uppercase">6. Alerts & CPM</span>
                  <span className="text-[8px] text-slate-500 block uppercase font-semibold">Systems 12, 17, 18</span>
                </button>
              </div>

              {/* Conditional Renders for Cockpit Sub-categories */}
              <div className="flex-1" id="subcockpit-panel-container">
                {cockpitSubTab === "ingestion-gis" && (
                  <GisIngestionPanel currentScenario={currentScenario} />
                )}
                {cockpitSubTab === "predictive-twin" && (
                  <PredictiveTwinPanel
                    simulationState={simulationState}
                    setSimulationState={setSimulationState}
                    projectedLossMillions={projectedLossMillions}
                    systemStressPct={systemStressPct}
                    evacuationFlowRate={evacuationFlowRate}
                  />
                )}
                {cockpitSubTab === "agent-autonomy" && (
                  <AgentAutonomyPanel currentScenario={currentScenario} />
                )}
                {cockpitSubTab === "graph-routing" && (
                  <GraphRoutingPanel />
                )}
                {cockpitSubTab === "nlp-copilot" && (
                  <NlpCopilotPanel currentScenario={currentScenario} />
                )}
                {cockpitSubTab === "alerts-recovery" && (
                  <AlertsRecoveryPanel />
                )}
              </div>

            </div>
          )}

          {/* TAB 2 CONTENT: Technical blueprint Search Engine */}
          {activeTab === "blueprints" && (
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 animate-fadeIn" id="blueprints-view">
              
              {/* Search sidebar columns */}
              <div className="md:col-span-4 flex flex-col gap-4 border-r border-[#090e18] pr-4 max-h-[calc(100vh-200px)] overflow-y-auto" id="blueprints-sidebar">
                <div className="relative" id="blueprints-search-field">
                  <span className="absolute inset-y-0 left-0 flex items-center pl-3 text-slate-500">
                    <Search className="w-4 h-4" />
                  </span>
                  <input
                    type="text"
                    placeholder="Search engineering spec..."
                    value={searchQuery}
                    onChange={(e) => setSearchQuery(e.target.value)}
                    className="w-full bg-[#090e18] border border-slate-900 rounded-xl py-2 px-9 text-xs text-slate-200 focus:border-cyan-500 outline-none font-mono"
                    id="input-blueprint-search"
                  />
                </div>

                {/* Vertical scrollable card instances */}
                <div className="space-y-2 flex-1" id="blueprints-links-stack">
                  {filteredBlueprints.map((blueprint) => (
                    <button
                      key={blueprint.id}
                      onClick={() => setSelectedBlueprintId(blueprint.id)}
                      className={`w-full text-left p-3.5 rounded-lg border transition-all duration-200 flex flex-col gap-1.5 ${
                        selectedBlueprintId === blueprint.id
                          ? "bg-cyan-500/10 border-cyan-500/35 text-cyan-400"
                          : "bg-[#090e18] border-slate-950 text-slate-400 hover:text-slate-200"
                      }`}
                      id={`btn-blueprint-card-${blueprint.id}`}
                    >
                      <div className="flex items-center justify-between text-[8px] font-mono uppercase font-bold" id="blueprint-metadata">
                        <span>Component {blueprint.id}</span>
                        <span className="px-1.5 py-0.2 bg-slate-950 text-slate-400 rounded">
                          {blueprint.category}
                        </span>
                      </div>
                      <div className="text-[11.5px] font-bold font-sans tracking-wide leading-snug" id="blueprint-title">
                        {blueprint.title}
                      </div>
                    </button>
                  ))}
                  {filteredBlueprints.length === 0 && (
                    <div className="text-slate-600 italic text-center py-8 text-xs font-mono" id="blueprint-empty-prompt">
                      No engineering component matches search constraints.
                    </div>
                  )}
                </div>
              </div>

              {/* Central Technical Code View Panel columns */}
              <div className="md:col-span-8 flex flex-col gap-5 p-2" id="blueprint-detail-content">
                
                {/* Specification Headers */}
                <div className="border-b border-slate-900 pb-4" id="blueprint-details-header">
                  <div className="flex items-center justify-between text-[10px] font-mono uppercase text-slate-500 font-bold mb-1">
                    <span>Enterprise System Specification</span>
                    <span>Component identifier: {selectedBlueprint.id}</span>
                  </div>
                  <h2 className="text-xl font-sans font-bold text-slate-100 tracking-wide">
                    {selectedBlueprint.title}
                  </h2>
                </div>

                {/* Architecture Narrative Block */}
                <div className="space-y-2" id="blueprint-narrative-summary">
                  <div className="text-[10px] font-mono text-slate-500 uppercase tracking-wider font-bold">
                    Architectural Blueprint Summary:
                  </div>
                  <p className="text-xs text-slate-300 font-sans leading-relaxed bg-[#090e18]/60 p-4 border border-slate-900 rounded-xl select-text">
                    {selectedBlueprint.architectureSummary}
                  </p>
                </div>

                {/* Techstack attributes */}
                <div className="space-y-1.5" id="blueprint-tech-stack-container">
                  <div className="text-[10px] font-mono text-slate-500 uppercase tracking-wider font-bold">
                    Target Tech Stack Integrators:
                  </div>
                  <div className="flex flex-wrap gap-2" id="blueprint-tech-tags">
                    {selectedBlueprint.techStack.map((tech, idx) => (
                      <span key={idx} className="bg-slate-950 border border-slate-900 text-slate-300 text-[10px] font-mono px-2.5 py-1 rounded" id={`tag-${tech}`}>
                        {tech}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Conditional Math Formula section */}
                {selectedBlueprint.equation && (
                  <div className="bg-cyan-950/10 border border-cyan-500/10 rounded-xl p-4 space-y-2 font-mono text-center" id="blueprint-math-panel">
                    <div className="text-[9px] uppercase tracking-wider text-slate-500 font-semibold" id="math-header">
                      Deterministic Mathematical Objective Minimizer Function
                    </div>
                    <div className="text-sm font-bold text-cyan-400 select-all py-1" id="math-formula-text">
                      {selectedBlueprint.equation}
                    </div>
                    {selectedBlueprint.equationDescription && (
                      <div className="text-[9.5px] text-slate-400 font-sans max-w-xl mx-auto leading-relaxed" id="math-description-text">
                        {selectedBlueprint.equationDescription}
                      </div>
                    )}
                  </div>
                )}

                {/* Dynamic Architectural Code Code terminal block */}
                {selectedBlueprint.codeBlock && (
                  <div className="flex flex-col flex-1" id="blueprint-terminal-editor">
                    <div className="bg-[#0b0f17] border border-slate-950 rounded-t-xl py-2 px-4 flex items-center justify-between text-[10px] font-mono text-slate-500 font-bold" id="terminal-bar">
                      <div className="flex items-center gap-1.5">
                        <Terminal className="w-3.5 h-3.5 text-cyan-400" id="icon-terminal-indicator" />
                        <span className="uppercase text-slate-400">{selectedBlueprint.codeBlock.language} FILE COMPOSITION</span>
                      </div>
                      <button
                        onClick={() => handleCopyCode(selectedBlueprint.codeBlock!.code, selectedBlueprint.id)}
                        className="flex items-center gap-1 hover:text-slate-200 transition-colors cursor-pointer py-1 px-2 rounded hover:bg-slate-950 border border-transparent hover:border-slate-900"
                        id="btn-copy-blueprint-code"
                      >
                        {copyFeedback === selectedBlueprint.id.toString() ? (
                          <>
                            <Check className="w-3 h-3 text-emerald-400" />
                            Copied to Console!
                          </>
                        ) : (
                          <>
                            <Copy className="w-3 h-3" />
                            Copy File
                          </>
                        )}
                      </button>
                    </div>
                    <div className="bg-[#04070d] border-x border-b border-slate-950 p-4 max-h-[350px] overflow-y-auto font-mono text-xs rounded-b-xl text-emerald-400 select-text" id="terminal-pane-view">
                      <pre className="whitespace-pre select-all font-mono leading-relaxed">{selectedBlueprint.codeBlock.code}</pre>
                    </div>
                  </div>
                )}

              </div>
            </div>
          )}



        </section>

        {/* Right Pane: Aegis AI Copilot Console */}
        <section className="lg:col-span-4 p-6 flex flex-col h-[calc(100vh-80px)]" id="copilot-panel">
          <div className="flex-1 bg-[#090e18] border border-slate-900 rounded-xl flex flex-col overflow-hidden max-h-full" id="copilot-terminal-container">
            
            {/* Copilot Header */}
            <div className="bg-[#0b101d] border-b border-slate-950 py-3.5 px-4 flex items-center justify-between font-mono" id="copilot-inner-header">
              <div className="flex items-center gap-2">
                <div className="relative">
                  <span className="absolute -top-0.5 -right-0.5 w-2 h-2 bg-green-500 rounded-full animate-ping"></span>
                  <div className="w-5 h-5 bg-cyan-950 border border-cyan-500/40 rounded-full flex items-center justify-center">
                    <Terminal className="w-3 h-3 text-cyan-400 animate-pulse" />
                  </div>
                </div>
                <div className="text-xs">
                  <div className="font-bold text-slate-200 uppercase tracking-tight">Aegis Operations Copilot</div>
                  <span className="text-[9px] text-slate-500 block uppercase font-semibold">Cognitive Agent Support</span>
                </div>
              </div>
              <span className="text-[10px] bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 px-2 py-0.5 rounded font-bold">
                v2.4.0
              </span>
            </div>

            {/* Chat message streams */}
            <div className="flex-1 p-4 overflow-y-auto space-y-4 select-text" id="chat-messages-scroller">
              {chatMessages.map((msg, idx) => (
                <div 
                  key={idx} 
                  className={`flex flex-col max-w-[88%] rounded-xl px-4 py-3 text-xs leading-relaxed font-sans ${
                    msg.role === "user" 
                      ? "bg-slate-900 border border-slate-800 text-slate-100 self-end rounded-br-none" 
                      : "bg-[#04070c] border border-slate-950 text-slate-300 self-start rounded-bl-none font-mono text-[10.5px]"
                  }`}
                  id={`chat-msg-${idx}`}
                >
                  <div className="flex items-center justify-between text-[8px] font-mono uppercase text-slate-500 mb-1.5 font-semibold">
                    <span>{msg.role === "user" ? "Command Ops" : "Aegis AI System"}</span>
                    {msg.mode === "simulated" && (
                      <span className="text-amber-500 bg-amber-500/10 border border-amber-500/20 px-1.5 py-0.2 rounded font-bold">LOCAL_SIMULATOR</span>
                    )}
                    {msg.mode === "live" && (
                      <span className="text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.2 rounded font-bold font-mono">LIVE_GEMINI</span>
                    )}
                  </div>
                  
                  {msg.role === "model" ? (
                    <div className="space-y-2 whitespace-pre-wrap select-all prose-invert text-slate-200">
                      {msg.content}
                    </div>
                  ) : (
                    <span className="select-all block text-slate-200 font-sans text-xs">{msg.content}</span>
                  )}
                </div>
              ))}
              
              {isChatLoading && (
                <div className="bg-[#04070c] border border-slate-950 rounded-xl px-4 py-3.5 self-start max-w-[88%] flex items-center gap-2 text-xs font-mono text-cyan-400" id="chat-loading-bubble">
                  <Loader2 className="w-4 h-4 animate-spin text-cyan-400" />
                  Generating Operations briefing...
                </div>
              )}
              
              <div ref={chatBottomRef} id="chat-scroller-bottom" />
            </div>

            {/* Conversation presets query helpers */}
            <div className="p-3 border-t border-slate-950 bg-[#050911]/60" id="copilot-chat-presets">
              <span className="text-[9px] uppercase tracking-wider font-mono text-slate-500 block mb-1.5 font-bold">
                Operational Command Presets:
              </span>
              <div className="flex flex-col gap-1.5" id="presets-container">
                <button
                  onClick={() => handlePresetClick("Calculate dynamic structural loss from pre and post disaster satellite SAR imagery.")}
                  className="w-full text-left bg-[#04070d]/60 hover:bg-[#04070d]/100 border border-slate-900 rounded-lg p-2 text-[9.5px] font-mono text-slate-400 hover:text-cyan-400 transition-colors uppercase leading-tight font-bold"
                  id="preset-satellite-diff"
                >
                  🛰️ Analyze SAR Satellite Images
                </button>
                <button
                  onClick={() => handlePresetClick("Detail how LangGraph agents conditionally route and coordinate crisis resources.")}
                  className="w-full text-left bg-[#04070d]/60 hover:bg-[#04070d]/100 border border-slate-900 rounded-lg p-2 text-[9.5px] font-mono text-slate-400 hover:text-cyan-400 transition-colors uppercase leading-tight font-bold"
                  id="preset-langgraph"
                >
                  🤖 Scan Autonomous Agent Mesh
                </button>
                <button
                  onClick={() => handlePresetClick("Find the optimal alternative path to Central Base when principal route gets Blocked.")}
                  className="w-full text-left bg-[#04070d]/60 hover:bg-[#04070d]/100 border border-slate-900 rounded-lg p-2 text-[9.5px] font-mono text-slate-400 hover:text-cyan-400 transition-colors uppercase leading-tight font-bold"
                  id="preset-routed-neo5j"
                >
                  🗺️ Query Alternate Graph Paths
                </button>
              </div>
            </div>

            {/* In-app terminal input box bar */}
            <div className="p-3 border-t border-slate-950 bg-[#0b101d]" id="copilot-input-bar">
              <form 
                onSubmit={(e) => { e.preventDefault(); handleSendMessage(); }} 
                className="flex items-center gap-2" 
                id="form-copilot-chat"
              >
                <input
                  type="text"
                  placeholder="Formulate query to Aegis Copilot..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  className="flex-1 bg-slate-950 border border-slate-900 hover:border-slate-800 focus:border-cyan-500/60 rounded-xl py-2 px-3 text-xs text-slate-200 outline-none font-mono"
                  id="input-copilot-text"
                />
                <button
                  type="submit"
                  disabled={isChatLoading || !chatInput.trim()}
                  className="bg-cyan-950/40 border border-cyan-500/40 text-cyan-400 hover:text-cyan-300 rounded-xl p-2.5 hover:bg-cyan-500/10 transition-colors cursor-pointer flex items-center justify-center disabled:opacity-40"
                  id="btn-copilot-send"
                >
                  <Send className="w-4 h-4" />
                </button>
              </form>
            </div>

          </div>
        </section>

      </main>

      {/* Persistent global platform footer */}
      <footer className="border-t border-slate-900 bg-[#04070d] px-6 py-3.5 flex flex-col md:flex-row items-center justify-between text-[11px] font-mono select-none" id="command-footer-bar">
        <div className="text-slate-500 uppercase font-semibold" id="footer-branding-label">
          Aegis Prime Platform Core v2.4.0 // Dual-Path Graph Encryption Active
        </div>
        <div className="flex items-center gap-4 text-slate-400 mt-2 md:mt-0" id="footer-status-pills">
          <div className="flex items-center gap-1.5 font-bold" id="status-fastapi">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            FASTAPI_INGEST
          </div>
          <div className="flex items-center gap-1.5 font-bold" id="status-ml">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            PYTORCH_SWIN
          </div>
          <div className="flex items-center gap-1.5 font-bold" id="status-neo4j">
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            NEO4J_GRAPH
          </div>
        </div>
      </footer>

    </div>
  );
}
