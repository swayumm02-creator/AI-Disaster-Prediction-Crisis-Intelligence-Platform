import React, { useState } from "react";
import { Radio, Loader2, Sparkles, AlertOctagon, Printer, Check, Clock, TrendingUp } from "lucide-react";

export default function AlertsRecoveryPanel() {
  
  const [broadcastTemplate, setBroadcastTemplate] = useState<"flood" | "wildfire" | "storm">("flood");
  const [isBroadcasting, setIsBroadcasting] = useState(false);
  const [broadcastProgress, setBroadcastProgress] = useState<number | null>(null);

  
  const [isGeneratingReport, setIsGeneratingReport] = useState(false);
  const [generatedReportText, setGeneratedReportText] = useState<string | null>(null);

  
  const [substationRestorationDays, setSubstationRestorationDays] = useState(8);
  const [bridgeClearanceDays, setBridgeClearanceDays] = useState(12);
  const [clinicSetupDays, setClinicSetupDays] = useState(6);

  const isSubstationExpedited = substationRestorationDays < 8;
  const isBridgeExpedited = bridgeClearanceDays < 12;

  
  const totalRecoveryPathHrs = substationRestorationDays + bridgeClearanceDays + clinicSetupDays;

  const handleTriggerBroadcast = () => {
    setIsBroadcasting(true);
    setBroadcastProgress(10);
    
    const interval = setInterval(() => {
      setBroadcastProgress(prev => {
        if (prev === null) return 0;
        if (prev >= 100) {
          clearInterval(interval);
          setIsBroadcasting(false);
          return 100;
        }
        return prev + 15;
      });
    }, 200);
  };

  const generateAegisBriefingMemo = () => {
    setIsGeneratingReport(true);
    setTimeout(() => {
      setGeneratedReportText(`AEGIS-BRIEF-MEMO-91028-VX
CLASSIFICATION: SECRET // CRISIS OPS COMMAND
DATE: ${new Date().toLocaleDateString()}
TARGET SECTOR: GALVESTON HARBOR / SAN FRANCISCO

1. CRISIS TELEMETRY OVERVIEW
- Standing Water Extent: 1,482 Hectares
- Dynamic System Stress Index: V-H Risk Category
- Calculated Inundation Output: VV/VH Segmented anomaly detected at -14.2dB.

2. AUTONOMOUS GRAPH ROUTING DEBUT
- Active Cypher status: Shortest-Path optimized.
- Preferred transit gateway: Road_Beta_Alt (L-9). Estimated transit duration: 18 minutes.
- Constraint parameters: Bypass selected around landslide blockers at Sector-4 intersection block.

3. STRATEGIC RESOURCES CONVERGENCE (MILP SOLVED)
- Helicopters: 4 Dispatched
- Ground EMS Units: 12 Active
- Fast Marine Responders: 2 Deployed
- Total allocation coverage: 95.8% index matching.

OFFICIAL AUTHORIZATION ENCRYPTED SIGNATURE:
[ AEGIS_CORE_ORCHESTRATOR_APPROVED_KEY_90918-X-F ]`);
      setIsGeneratingReport(false);
    }, 900);
  };

  return (
    <div className="space-y-6" id="alerts-recovery-pane">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6" id="alerts-recovery-grid">

  
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-broadcast">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-red-500 rounded-sm animate-pulse" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [12]: Early Warning Cell Broadcast
                </h3>
              </div>
              <Radio className="w-4 h-4 text-red-500 animate-pulse" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Triggers localized geo-fenced Cell Broadcast notifications to LTE/5G cellular structures within active H3 indices in sub-second intervals.
            </p>

            <div className="space-y-3 font-mono text-[10px]" id="broadcast-selectors">
              <div>
                <label className="block text-[9px] uppercase font-mono tracking-wider text-slate-500 mb-1 font-bold">Alert Broadcaster Template</label>
                <select
                  value={broadcastTemplate}
                  onChange={(e) => setBroadcastTemplate(e.target.value as any)}
                  className="w-full bg-slate-950 border border-slate-900 text-slate-200 py-2 px-3 rounded-lg text-xs font-mono outline-none focus:border-red-500"
                >
                  <option value="flood">⚠️ Extreme Flood Inundation - Immediate evacuation</option>
                  <option value="wildfire">🔥 Forest Wildfire Approaching - Gated evacuation routes</option>
                  <option value="storm">🌀 Storm Surge Warning - Seek elevated shelters</option>
                </select>
              </div>

              <div className="bg-slate-950 p-2 border border-slate-900 rounded font-mono text-[9px] text-red-400">
                {broadcastTemplate === "flood" && "BROADCAST_MSG: Crisis Ops alerts residents of Valley Basin region. Standing flood depth exceeds critical limits. Move to designated Shelters. Alt path routes selected."}
                {broadcastTemplate === "wildfire" && "BROADCAST_MSG: Extreme wind fires active in Sector Foothills. Evacuate via Road Beta Alt immediately. Follow automated UAV flashing lights."}
                {broadcastTemplate === "storm" && "BROADCAST_MSG: Hurricane surge locked on coastal boundaries. Power Grid scheduled shut down in 15 minutes. High-vantage evacuation corridors designated."}
              </div>

              <button
                onClick={handleTriggerBroadcast}
                disabled={isBroadcasting}
                className="w-full h-10 bg-red-950/40 border border-red-500/40 hover:bg-red-500/10 text-red-400 rounded-lg text-xs font-bold uppercase transition-all flex items-center justify-center gap-2"
                id="btn-broadcast"
              >
                {isBroadcasting ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    Broadcasting Alerts...
                  </>
                ) : (
                  <>
                    <Radio className="w-3.5 h-3.5" />
                    Broadcast Local Warnings
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="mt-4" id="mod12-output">
            {broadcastProgress !== null && (
              <div className="bg-[#04070d] border border-slate-950 rounded-xl p-3 space-y-2 font-mono text-[10px] animate-fadeIn">
                <div className="flex justify-between items-center text-[9px]">
                  <span className="text-slate-500 font-bold">FCC Signaling Queue dispatch status</span>
                  <span className="text-red-400 font-bold">{broadcastProgress >= 100 ? "BROADCAST_SUCCESS" : "DISPATCHING"}</span>
                </div>
                
                <div className="w-full bg-slate-950 h-2 rounded overflow-hidden">
                  <div className="bg-red-500 h-full transition-all duration-150" style={{ width: `${broadcastProgress}%` }} />
                </div>
                
                <div className="flex justify-between text-[8.5px] text-slate-400 pt-1">
                  <span>H3 indexes: 64-bit Hexes</span>
                  <span className="font-bold text-slate-200">Subscribers notified: {Math.round(broadcastProgress * 148)} / 14,800</span>
                </div>
              </div>
            )}
          </div>
        </div>

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-reporting">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-cyan-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [17]: Generative AI Reporting Engine
                </h3>
              </div>
              <Sparkles className="w-4 h-4 text-cyan-400 animate-pulse" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Assembles active telemetry vectors, routing states, and computed variables into beautiful structured crisis reports for command teams signatures.
            </p>

            <button
              onClick={generateAegisBriefingMemo}
              disabled={isGeneratingReport}
              className="w-full h-10 bg-cyan-950/40 border border-cyan-500/40 hover:bg-cyan-500/10 text-cyan-400 rounded-lg text-xs font-bold uppercase transition-all flex items-center justify-center gap-2"
              id="btn-generate-report"
            >
              {isGeneratingReport ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Compiling Active Logs...
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  Generate Briefing Report
                </>
              )}
            </button>
          </div>

          <div className="mt-4" id="mod17-output">
            {generatedReportText ? (
              <div className="space-y-3 animate-fadeIn">
                <div className="p-3 bg-[#04070d] border border-slate-950 rounded-xl max-h-[140px] overflow-y-auto font-mono text-[9px] text-zinc-300 leading-relaxed scrollbar-thin select-all">
                  <pre>{generatedReportText}</pre>
                </div>
                
                <button
                  onClick={() => window.print()}
                  className="w-full py-1.5 px-3 border border-slate-800 bg-slate-950 text-[10px] rounded hover:bg-slate-900 text-slate-300 hover:text-slate-100 uppercase font-mono font-bold flex items-center justify-center gap-1.5"
                >
                  <Printer className="w-3.5 h-3.5" />
                  Print Briefing Memo
                </button>
              </div>
            ) : (
              <div className="bg-[#04070d] border border-slate-950 rounded-xl p-6 text-center text-slate-600 font-mono text-[10px] italic">
                Click button above to compile active system-wide stats.
              </div>
            )}
          </div>
        </div>

      </div>

  
      <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5" id="card-module-recovery-planner">
        <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 bg-yellow-400 rounded-sm animate-pulse" />
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
              [18]: Predictive Recovery Planner (Critical Path Timeline)
            </h3>
          </div>
          <Clock className="w-4 h-4 text-yellow-400" />
        </div>

        <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
          Schedules public helper entities restoration programs using Critical Path Method (CPM) networks. Dependent child projects (like setting up medical field clinics) can only start once structural constraints (like clearing landslides) are achieved.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-5" id="recovery-planner-layout">
          
          <div className="space-y-3 font-mono text-[10px]" id="cpm-levers">
            <div className="border-b border-slate-900 pb-2 mb-2 font-bold text-slate-500 uppercase tracking-tight">Active Operation Durations</div>
            
            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Task A: substation electric boot:</span>
                <span className="text-yellow-400">{substationRestorationDays} hrs</span>
              </div>
              <input
                type="range"
                min="4"
                max="12"
                value={substationRestorationDays}
                onChange={(e) => setSubstationRestorationDays(parseInt(e.target.value))}
                className="w-full accent-yellow-500 h-1 cursor-pointer bg-slate-800 rounded outline-none"
              />
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Task B: clear bridge landslide (Requires Task A):</span>
                <span className="text-yellow-400">{bridgeClearanceDays} hrs</span>
              </div>
              <input
                type="range"
                min="6"
                max="18"
                value={bridgeClearanceDays}
                onChange={(e) => setBridgeClearanceDays(parseInt(e.target.value))}
                className="w-full accent-yellow-500 h-1 cursor-pointer bg-slate-800 rounded outline-none"
              />
            </div>

            <div className="space-y-1">
              <div className="flex justify-between text-slate-400">
                <span>Task C: setup trauma clinical clinic (Requires Task B):</span>
                <span className="text-yellow-400">{clinicSetupDays} hrs</span>
              </div>
              <input
                type="range"
                min="3"
                max="9"
                value={clinicSetupDays}
                onChange={(e) => setClinicSetupDays(parseInt(e.target.value))}
                className="w-full accent-yellow-500 h-1 cursor-pointer bg-slate-800 rounded outline-none"
              />
            </div>
          </div>

          <div className="flex flex-col justify-center bg-[#04070d] border border-slate-950 p-4 rounded-xl font-mono text-[10px] space-y-3" id="cpm-cpm-schedule">
            <div className="flex justify-between border-b border-slate-900 pb-1.5 font-bold text-slate-500 uppercase">
              <span>CPM Network Solved Path</span>
              <span className="text-yellow-400 font-semibold flex items-center gap-0.5"><Clock className="w-3" /> RESTORING</span>
            </div>

            <div className="space-y-2 text-[9.5px]">
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded bg-cyan-400 animate-pulse"></span>
                <span className="text-slate-300">Phase 1: sub boot-up: <strong className="text-slate-100">{substationRestorationDays} hours</strong> [Critical]</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded bg-amber-500 animate-pulse"></span>
                <span className="text-slate-300">Phase 2: debris clearing: <strong className="text-slate-100">{bridgeClearanceDays} hours</strong> [Critical Delay]</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded bg-purple-400 animate-pulse"></span>
                <span className="text-slate-300">Phase 3: shelter clinical aid: <strong className="text-slate-100">{clinicSetupDays} hours</strong> [Critical]</span>
              </div>
            </div>

            <div className="pt-2 border-t border-slate-900/60 leading-relaxed text-slate-400">
              Computed Critical Path Duration: <strong className="text-yellow-400 font-bold text-xs">{totalRecoveryPathHrs} Hours</strong>
              <div className="text-[8px] text-slate-500 mt-1 uppercase font-bold">Constraint formula: T_recovery = Task_A + Task_B + Task_C</div>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
}
