import React, { useState } from "react";
import { Radio, Layers, Compass, Loader2, Play, Check, AlertTriangle, ShieldAlert } from "lucide-react";
import { DisasterConfig, IngestedLog } from "../types";

interface Props {
  currentScenario: DisasterConfig;
}

export default function GisIngestionPanel({ currentScenario }: Props) {
  
  const [ingestionLogs, setIngestionLogs] = useState<IngestedLog[]>([
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
  const [isIngesting, setIsIngesting] = useState(false);
  const [ingestionSource, setIngestionSource] = useState<"SAR" | "IoT" | "SocialMedia">("IoT");
  const [mockSensorInput, setMockSensorInput] = useState("4.85");

  
  const [swipePosition, setSwipePosition] = useState<number>(50);

  
  const [h3Lat, setH3Lat] = useState<string>(currentScenario.coordinates.lat.toFixed(4));
  const [h3Lng, setH3Lng] = useState<string>(currentScenario.coordinates.lng.toFixed(4));
  const [h3Result, setH3Result] = useState<{ index: string; status: string; confidence: string } | null>(null);
  const [isH3Loading, setIsH3Loading] = useState(false);

  
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
          lat_center: parseFloat(h1(currentScenario.coordinates.lat)),
          lng_center: parseFloat(h1(currentScenario.coordinates.lng)),
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

  const h1 = (val: number) => val.toFixed(4);

  
  const computeH3Index = () => {
    setIsH3Loading(true);
    setTimeout(() => {
      const latF = parseFloat(h3Lat) || currentScenario.coordinates.lat;
      const lngF = parseFloat(h3Lng) || currentScenario.coordinates.lng;
      
      
      const hashPr = Math.abs(Math.sin(latF) * Math.cos(lngF) * 1000000);
      const h3Hex = "8" + Math.floor(hashPr).toString(16).padEnd(14, "f");
      
      const distanceToCenter = Math.hypot(latF - currentScenario.coordinates.lat, lngF - currentScenario.coordinates.lng);
      const isDangerous = distanceToCenter < 0.05; // close to active disaster coordinates

      setH3Result({
        index: h3Hex,
        status: isDangerous ? "CRITICAL_HAZARD_ZONE" : "SAFE_BUFFER_ZONE",
        confidence: (99.4 - distanceToCenter * 5).toFixed(1) + "%"
      });
      setIsH3Loading(false);
    }, 800);
  };

  return (
    <div className="space-y-6" id="gis-ingestion-pane">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6" id="gis-ingestion-grid">
        
        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-ingest">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-cyan-400 rounded-sm animate-pulse" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [1]: Multi-Source Data Ingestion
                </h3>
              </div>
              <Radio className="w-4 h-4 text-cyan-400 animate-ping" id="copilot-beacon" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Asynchronously ingest real-time multimodal inputs. Validates coordinate structures through integrated Pydantic classes and writes onto isolated Kafka streams.
            </p>

            <div className="grid grid-cols-3 gap-2 mb-4" id="ingest-channel-selectors">
              {(["IoT", "SAR", "SocialMedia"] as const).map(source => (
                <button
                  key={source}
                  onClick={() => setIngestionSource(source)}
                  className={`py-2 text-[10px] font-mono font-bold rounded-lg border transition-all duration-200 uppercase ${
                    ingestionSource === source 
                      ? "bg-cyan-500/10 border-cyan-500/50 text-cyan-400" 
                      : "bg-slate-950/50 border-slate-800 text-slate-400 hover:text-slate-200"
                  }`}
                  id={`btn-channel-${source}`}
                >
                  {source}
                </button>
              ))}
            </div>

            {ingestionSource === "IoT" && (
              <div className="mb-4" id="iot-input-group">
                <label className="block text-[10px] uppercase font-mono tracking-wider text-slate-500 mb-1.5 font-semibold">
                  Input Float River Gauge Level (Meters):
                </label>
                <input
                  type="number"
                  step="0.05"
                  value={mockSensorInput}
                  onChange={(e) => setMockSensorInput(e.target.value)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-lg py-2 px-3 text-xs text-cyan-400 font-mono focus:border-cyan-500/55 outline-none font-medium"
                />
              </div>
            )}

            <button
              onClick={handlePulseDataFusion}
              disabled={isIngesting}
              className="w-full h-10 bg-cyan-950/40 border border-cyan-500/40 hover:bg-cyan-500/10 text-cyan-400 rounded-lg text-xs font-mono font-bold uppercase transition-all duration-300 flex items-center justify-center gap-2"
              id="btn-pulse-ingest"
            >
              {isIngesting ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Validating Payload...
                </>
              ) : (
                <>
                  <Play className="w-3.5 h-3.5" />
                  Pulse Ingestion Stream
                </>
              )}
            </button>
          </div>

          <div className="mt-5" id="mod1-output-console">
            <div className="flex items-center justify-between text-[10px] uppercase tracking-wider font-mono text-slate-500 font-bold mb-2">
              <span>Kafka Partition Topic Stream Logs</span>
              <span className="text-cyan-500 animate-pulse">● LIVE</span>
            </div>
            <div className="bg-[#04070d] border border-slate-950 rounded-lg p-3 max-h-[140px] overflow-y-auto font-mono text-[10px] space-y-2 select-text" id="stream-logs-box">
              {ingestionLogs.map((log) => (
                <div key={log.id} className="border-b border-slate-900/60 pb-2 last:border-0 last:pb-0">
                  <div className="flex items-center justify-between text-[9px] mb-1">
                    <span className="text-slate-400 font-bold">[{log.timestamp}] {log.source}</span>
                    <span className="text-cyan-400 px-1 bg-cyan-950/20 rounded font-semibold">{log.status}</span>
                  </div>
                  <span className="text-slate-300 font-bold block mb-1">ID: {log.id}</span>
                  <pre className="text-[9px] text-emerald-400 max-w-full overflow-x-auto select-all bg-slate-950/40 p-1 rounded">
                    {JSON.stringify(log.payload, null, 2)}
                  </pre>
                </div>
              ))}
            </div>
          </div>
        </div>

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-satellite">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-amber-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [2/15]: Satellite Image Segmenter
                </h3>
              </div>
              <Layers className="w-4 h-4 text-amber-400" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Swipe the horizontal crossbar below to trigger pixel difference metrics comparing baseline radar vectors against flooded post-event grids.
            </p>

            <div className="relative h-44 w-full bg-slate-950 border border-slate-900 rounded-lg overflow-hidden select-none" id="radar-swipe-simulator">
              
              <div className="absolute inset-0 bg-[#0e1726]/30 flex flex-col justify-between p-3" id="pre-event-basemap">
                <div className="text-[9px] font-mono font-bold bg-slate-900/80 text-slate-300 py-1 px-2 rounded border border-slate-800 self-start">
                  PRE-EVENT RADAR REFLECTANCE
                </div>
                
                <svg className="w-full h-24 self-center text-slate-700/30 opacity-70" viewBox="0 0 200 100">
                  <path d="M 0 80 Q 50 30, 100 80 T 200 80" fill="none" stroke="currentColor" strokeWidth="3" />
                  <rect x="25" y="45" width="20" height="15" fill="none" stroke="currentColor" strokeWidth="2" />
                  <rect x="145" y="55" width="25" height="15" fill="none" stroke="currentColor" strokeWidth="2" />
                  <circle cx="100" cy="50" r="12" fill="none" stroke="currentColor" strokeWidth="1.5" />
                </svg>
              </div>

            
              <div 
                className="absolute inset-y-0 right-0 bg-[#161214] border-l border-cyan-400 overflow-hidden flex flex-col justify-between p-3 transition-all duration-75"
                style={{ left: `${swipePosition}%` }}
                id="post-event-overlay"
              >
                <div 
                  className="text-[9px] font-mono font-bold bg-red-950/80 text-red-400 py-1 px-2 rounded border border-red-900/40 self-start whitespace-nowrap"
                  style={{ transform: `translateX(-${100 - swipePosition}%)` }}
                >
                  POST-EVENT SEGMENTER (SWIN-VIT)
                </div>

                <svg className="w-full h-24 text-red-500/40 self-center" viewBox="0 0 200 100" style={{ transform: `translateX(-${100 - swipePosition}%)` }}>
                  <path d="M 0 80 Q 50 30, 100 80 T 200 80" fill="rgba(6, 182, 212, 0.25)" stroke="#06b6d4" strokeWidth="3" />
                  <rect x="25" y="45" width="20" height="15" fill="rgba(241, 113, 85, 0.4)" stroke="#f97316" strokeWidth="2" />
                  <line x1="25" y1="45" x2="45" y2="60" stroke="#f97316" strokeWidth="1.5" />
                  <circle cx="100" cy="50" r="12" fill="rgba(239, 68, 68, 0.3)" stroke="#ef4444" strokeWidth="2" />
                </svg>
              </div>

              <div className="absolute bottom-2 left-1/3 bg-slate-900/90 border border-slate-800 text-[10px] px-2 py-0.5 rounded text-slate-400 font-mono whitespace-nowrap" id="segmentation-difference">
                Outlier Variance: <span className="text-cyan-400 font-semibold">{(swipePosition * 0.85).toFixed(1)} dB</span>
              </div>
            </div>

            <div className="mt-3" id="swipe-slider">
              <input 
                type="range"
                min="0"
                max="100"
                value={swipePosition}
                onChange={(e) => setSwipePosition(parseInt(e.target.value))}
                className="w-full accent-cyan-500 h-1 cursor-pointer bg-slate-800 rounded-lg outline-none"
              />
              <div className="flex justify-between text-[9px] font-mono text-slate-500 mt-1 uppercase font-semibold">
                <span>Pre-Event</span>
                <span>Move slider to compare</span>
                <span>Post-Event Swin</span>
              </div>
            </div>
          </div>

          <div className="mt-4 bg-[#04070d] border border-slate-950 rounded-lg p-3" id="mod2-stats">
            <div className="grid grid-cols-2 gap-4 text-center font-mono">
              <div className="border-r border-slate-900">
                <span className="text-[10px] text-slate-500 block uppercase font-semibold">Flooded Basin Area</span>
                <span className="text-lg font-bold text-cyan-400">1,482 Hectares</span>
              </div>
              <div>
                <span className="text-[10px] text-slate-500 block uppercase font-semibold">ViT Segmenter F1</span>
                <span className="text-lg font-bold text-emerald-400">0.962 Accuracy</span>
              </div>
            </div>
          </div>
        </div>

      </div>

      
      <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5" id="card-module-h3">
        <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
          <div className="flex items-center gap-2">
            <div className="w-2.5 h-2.5 bg-purple-400 rounded-sm" />
            <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
              [4]: Geospatial AI Risk Engine (H3 Space)
            </h3>
          </div>
          <Compass className="w-4 h-4 text-purple-400" />
        </div>

        <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
          Uber H3 discrete global grid indexing allows O(1) mathematical hazard intersection checks. Enter geographical bounds below to project municipal targets onto hex cells and identify safety indices.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4" id="h3-input-grid">
          <div>
            <label className="block text-[10px] uppercase font-mono tracking-wider text-slate-500 mb-1.5 font-semibold">
              Target Latitude
            </label>
            <input
              type="number"
              step="0.0001"
              value={h3Lat}
              onChange={(e) => setH3Lat(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg py-2 px-3 text-xs text-slate-200 font-mono focus:border-purple-500/55 outline-none"
            />
          </div>
          <div>
            <label className="block text-[10px] uppercase font-mono tracking-wider text-slate-500 mb-1.5 font-semibold">
              Target Longitude
            </label>
            <input
              type="number"
              step="0.0001"
              value={h3Lng}
              onChange={(e) => setH3Lng(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-lg py-2 px-3 text-xs text-slate-200 font-mono focus:border-purple-500/55 outline-none"
            />
          </div>
          <div className="flex items-end">
            <button
              onClick={computeH3Index}
              disabled={isH3Loading}
              className="w-full h-10 bg-purple-950/40 border border-purple-500/40 hover:bg-purple-500/10 text-purple-400 rounded-lg text-xs font-mono font-bold uppercase transition-all flex items-center justify-center gap-2"
              id="btn-resolve-h3"
            >
              {isH3Loading ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Hashing Matrix...
                </>
              ) : (
                <>
                  <Compass className="w-3.5 h-3.5" />
                  Query H3 Index Code
                </>
              )}
            </button>
          </div>
        </div>

        {h3Result && (
          <div className="mt-4 bg-[#04070d] border border-slate-950 rounded-xl p-4 flex flex-col md:flex-row items-center justify-between gap-4 animate-fadeIn" id="h3-result-card">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-full bg-purple-950/40 border border-purple-500/30 flex items-center justify-center">
                <ShieldAlert className="w-4 h-4 text-purple-400" />
              </div>
              <div>
                <span className="text-[9px] uppercase font-mono text-slate-500 block font-semibold">Resolved H3 Hex Space (64-bit Address)</span>
                <span className="text-sm font-bold text-slate-200 font-mono select-all uppercase">{h3Result.index}</span>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4 text-center">
              <div className="px-3 py-1 bg-slate-950 border border-slate-900 rounded-lg">
                <span className="text-[9px] uppercase font-mono text-slate-500 block font-bold">Risk Zone Assessment</span>
                <span className={`text-xs font-bold font-mono ${h3Result.status.includes("CRITICAL") ? "text-red-400 animate-pulse" : "text-emerald-400"}`}>
                  {h3Result.status}
                </span>
              </div>
              <div className="px-3 py-1 bg-slate-950 border border-slate-900 rounded-lg">
                <span className="text-[9px] uppercase font-mono text-slate-500 block font-bold">Intersection Confidence</span>
                <span className="text-xs font-bold font-mono text-slate-300">{h3Result.confidence}</span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
