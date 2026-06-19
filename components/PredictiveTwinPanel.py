import React, { useState } from "react";
import { Sliders, Activity, Flame, CloudRain, ShieldAlert, DollarSign, Loader2, ArrowRight } from "lucide-react";
import { SimulationState } from "../types";

interface Props {
  simulationState: SimulationState;
  setSimulationState: React.Dispatch<React.SetStateAction<SimulationState>>;
  projectedLossMillions: string;
  systemStressPct: number;
  evacuationFlowRate: number;
}

export default function PredictiveTwinPanel({
  simulationState,
  setSimulationState,
  projectedLossMillions,
  systemStressPct,
  evacuationFlowRate
}: Props) {
  
  const [selectedForecastHazard, setSelectedForecastHazard] = useState<"flood" | "wildfire" | "landslide">("flood");
  const [isForecasting, setIsForecasting] = useState(false);
  const [forecastResult, setForecastResult] = useState<{
    hazardThreatPct: number;
    empiricalLossVal: string;
    physicsLossVal: string;
    cascadingProbabilityPct: number;
  } | null>(null);

  
  const runForecastingEngine = () => {
    setIsForecasting(true);
    setTimeout(() => {
      let threat = 45;
      let cascading = 30;
      if (selectedForecastHazard === "flood") {
        threat = Math.min(Math.round(simulationState.precipitation * 0.9 + 15), 100);
        cascading = Math.min(Math.round(simulationState.precipitation * 0.6 + (100 - simulationState.powerGridCapacity) * 0.4), 100);
      } else if (selectedForecastHazard === "wildfire") {
        threat = Math.min(Math.round(simulationState.roadCongestion * 0.8 + 20), 100);
        cascading = Math.min(Math.round(simulationState.roadCongestion * 0.5 + 10), 100);
      } else {
        threat = Math.min(Math.round(simulationState.precipitation * 1.1 + 10), 100);
        cascading = Math.min(Math.round(simulationState.precipitation * 0.9 + 5), 100);
      }

      setForecastResult({
        hazardThreatPct: threat,
        empiricalLossVal: (0.124 + threat * 0.0035).toFixed(4),
        physicsLossVal: (0.045 + (100 - simulationState.powerGridCapacity) * 0.0015).toFixed(4),
        cascadingProbabilityPct: cascading
      });
      setIsForecasting(false);
    }, 1000);
  };

  return (
    <div className="space-y-6" id="predictive-twin-pane">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6" id="twin-main-grid">
        
        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-sandbox">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-red-400 rounded-sm animate-pulse" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [5/14]: Digital Twin Dynamics & Economics
                </h3>
              </div>
              <Sliders className="w-4 h-4 text-red-400" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Modify active environmental levers. Compute economic assets degradation and traffic routing degradation coefficients dynamically.
            </p>

            <div className="space-y-4 font-mono text-[10px]" id="sandbox-levers">
              <div id="lever-precipitation">
                <div className="flex justify-between text-slate-400 font-semibold mb-1 uppercase">
                  <span>Precipitation Rainfall</span>
                  <span className="text-cyan-400">{simulationState.precipitation} mm/hr</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="120"
                  value={simulationState.precipitation}
                  onChange={(e) => setSimulationState(prev => ({ ...prev, precipitation: parseInt(e.target.value) }))}
                  className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
                />
              </div>

              <div id="lever-congestion">
                <div className="flex justify-between text-slate-400 font-semibold mb-1 uppercase">
                  <span>Background Road Gridlock</span>
                  <span className="text-amber-500">{simulationState.roadCongestion}% Density</span>
                </div>
                <input
                  type="range"
                  min="10"
                  max="100"
                  value={simulationState.roadCongestion}
                  onChange={(e) => setSimulationState(prev => ({ ...prev, roadCongestion: parseInt(e.target.value) }))}
                  className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
                />
              </div>

              <div id="lever-power">
                <div className="flex justify-between text-slate-400 font-semibold mb-1 uppercase">
                  <span>Electric Grid Capacity</span>
                  <span className="text-emerald-500">{simulationState.powerGridCapacity}% Online</span>
                </div>
                <input
                  type="range"
                  min="20"
                  max="100"
                  value={simulationState.powerGridCapacity}
                  onChange={(e) => setSimulationState(prev => ({ ...prev, powerGridCapacity: parseInt(e.target.value) }))}
                  className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
                />
              </div>
            </div>
          </div>

          <div className="mt-5 bg-[#04070d] border border-slate-950 rounded-lg p-3.5 space-y-3 font-mono text-[10px]">
            <div className="flex items-center justify-between text-[11px] border-b border-slate-900 pb-2 mb-2 font-bold text-slate-400">
              <span>DYNAMIC FAILURE MATRIX</span>
              <span className="text-red-400">STATE_MUTABLE</span>
            </div>
            
            <div className="grid grid-cols-2 gap-3">
              <div className="bg-slate-950 p-2 border border-slate-900/60 rounded flex items-center justify-between" id="metric-stress">
                <div>
                  <span className="text-[9px] text-slate-500 block uppercase font-semibold">Total System Stress</span>
                  <span className="text-xs font-bold text-slate-100">{systemStressPct}%</span>
                </div>
                <Activity className={`w-4 h-4 ${systemStressPct > 70 ? "text-red-500 animate-bounce" : "text-cyan-400 animate-pulse"}`} />
              </div>

              <button 
                onClick={() => setSimulationState({ precipitation: 90, roadCongestion: 85, powerGridCapacity: 30, hazardSpreadRadius: 850 })}
                className="bg-red-950/20 hover:bg-red-950/40 border border-red-900/30 text-red-400 rounded p-2 text-center text-[10px] uppercase font-bold transition-colors"
              >
                Trigger CAT-5 Storm
              </button>
            </div>

            <div className="grid grid-cols-2 gap-3 pt-1 border-t border-slate-900">
              <div>
                <span className="text-[9px] text-slate-500 block uppercase font-semibold">Projected Damage</span>
                <span className="text-sm font-bold text-amber-500 flex items-center gap-0.5">
                  <DollarSign className="w-3.5 h-3.5 text-slate-500" />
                  {projectedLossMillions}M
                </span>
              </div>
              <div>
                <span className="text-[9px] text-slate-500 block uppercase font-semibold">Transit Flow Rate</span>
                <span className="text-sm font-bold text-cyan-400">
                  {evacuationFlowRate} units / min
                </span>
              </div>
            </div>
          </div>
        </div>

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-prediction">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-yellow-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [3]: Disaster Risk Forecasting AI
                </h3>
              </div>
              <Activity className="w-4 h-4 text-yellow-400 animate-pulse" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Combines spatiotemporal datasets across forest thresholds and hydrologic structures using localized Graph Neural Networks (GNNs).
            </p>

            <div className="grid grid-cols-3 gap-2 mb-4" id="prediction-hazard-selectors">
              {(["flood", "wildfire", "landslide"] as const).map(haz => (
                <button
                  key={haz}
                  onClick={() => setSelectedForecastHazard(haz)}
                  className={`py-2 text-[10px] font-mono font-bold rounded-lg border transition-all duration-200 uppercase ${
                    selectedForecastHazard === haz 
                      ? "bg-yellow-500/10 border-yellow-500/50 text-yellow-400" 
                      : "bg-slate-950/50 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                >
                  {haz}
                </button>
              ))}
            </div>

            <button
              onClick={runForecastingEngine}
              disabled={isForecasting}
              className="w-full h-10 bg-yellow-950/40 border border-yellow-500/40 hover:bg-yellow-500/10 text-yellow-400 rounded-lg text-xs font-mono font-bold uppercase transition-all flex items-center justify-center gap-2"
              id="btn-run-forecast"
            >
              {isForecasting ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Solving TFT Constraints...
                </>
              ) : (
                <>
                  <ArrowRight className="w-3.5 h-3.5" />
                  Predict Cascading Damage
                </>
              )}
            </button>
          </div>

          <div className="mt-4" id="mod3-output">
            {forecastResult ? (
              <div className="bg-[#04070d] border border-slate-950 rounded-lg p-3 space-y-2 font-mono text-[10px] animate-fadeIn">
                <div className="flex justify-between border-b border-slate-900 pb-1 font-bold text-slate-500">
                  <span>SPATIOTEMPORAL GRAPH FORECAST</span>
                  <span className="text-yellow-400">SOLVED</span>
                </div>
                <div className="grid grid-cols-2 gap-2">
                  <div>
                    <span className="text-slate-500 text-[9px] block">Hazard Index Peak</span>
                    <span className="text-xs font-bold text-slate-200">{forecastResult.hazardThreatPct}%</span>
                  </div>
                  <div>
                    <span className="text-slate-500 text-[9px] block">Causal Cascade Probability</span>
                    <span className="text-xs font-bold text-red-400">{forecastResult.cascadingProbabilityPct}%</span>
                  </div>
                </div>
                <div className="pt-1.5 border-t border-slate-900/60 flex justify-between text-[9px]">
                  <span className="text-slate-400">Empirical loss: {forecastResult.empiricalLossVal}</span>
                  <span className="text-slate-400">Physics constraints: {forecastResult.physicsLossVal}</span>
                </div>
              </div>
            ) : (
              <div className="bg-[#04070d] border border-slate-950 rounded-lg p-4 text-center text-slate-600 font-mono text-[10px] italic">
                Set environmental sliders and click predicton trigger.
              </div>
            )}
          </div>
        </div>

      </div>

      
      <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5" id="card-module-xai">
        <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 bg-sky-400 rounded-sm" />
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
              [13]: Explainable AI (XAI) Center
            </h3>
          </div>
          <Activity className="w-4 h-4 text-sky-400" />
        </div>

        <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
          Provides human-comprehensible descriptions for model predictions. Displays SHAP (SHapley Additive exPlanations) values representing feature attributions to the peak hazard threat.
        </p>

        <div className="bg-[#04070d] border border-slate-950 rounded-xl p-4 space-y-3 font-mono text-[10px]" id="xai-bars-container">
          <div className="flex justify-between text-slate-500 font-bold border-b border-slate-900 pb-1 text-[9px]">
            <span>FEATURE CONTRIBUTION INDEX</span>
            <span>SHAP ATTRIBUTION VALUE</span>
          </div>

    
          <div className="space-y-1">
            <div className="flex justify-between text-slate-300 font-semibold">
              <span>Rainfall Intesity (Precipitation Volume)</span>
              <span className="text-[#38bdf8]">+{(simulationState.precipitation * 0.006).toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 rounded h-1.5 overflow-hidden">
              <div className="bg-sky-400 h-full transition-all duration-300" style={{ width: `${Math.min((simulationState.precipitation / 120) * 100, 100)}%` }} />
            </div>
          </div>

          
          <div className="space-y-1">
            <div className="flex justify-between text-slate-300 font-semibold">
              <span>Grid Degradation (Blackout Susceptibility)</span>
              <span className="text-[#38bdf8]">+{((100 - simulationState.powerGridCapacity) * 0.004).toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 rounded h-1.5 overflow-hidden">
              <div className="bg-sky-400 h-full transition-all duration-300" style={{ width: `${100 - simulationState.powerGridCapacity}%` }} />
            </div>
          </div>

          
          <div className="space-y-1">
            <div className="flex justify-between text-slate-300 font-semibold">
              <span>Road Gridlock Density Factor</span>
              <span className="text-[#38bdf8]">+{(simulationState.roadCongestion * 0.003).toFixed(3)}</span>
            </div>
            <div className="w-full bg-slate-950 rounded h-1.5 overflow-hidden">
              <div className="bg-sky-400 h-full transition-all duration-300" style={{ width: `${simulationState.roadCongestion}%` }} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
