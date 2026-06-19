import React, { useState, useRef, useEffect } from "react";
import { Terminal, Send, Loader2, Search, Check, Copy, MessageCircle } from "lucide-react";
import { DisasterConfig } from "../types";

interface Props {
  currentScenario: DisasterConfig;
}

const SOCIAL_PRESETS = [
  {
    text: "Bridge at Sector-4 totally submerged. Water is rushing, roads isolated!",
    classification: "URGENT_EVACUATION",
    confidence: 97.4,
    coords: "37.7749, -122.4194"
  },
  {
    text: "Heavy wildfire smoke approaching Foothills. Visibilty below 10 meters.",
    classification: "HAZARD_OBSERVATION",
    confidence: 89.2,
    coords: "37.7512, -122.4312"
  },
  {
    text: "Water level is rising slowly in the backyard, but roads are still open for now.",
    classification: "ROUTINE_MONITOR",
    confidence: 76.5,
    coords: "37.7922, -122.4011"
  }
];

export default function NlpCopilotPanel({ currentScenario }: Props) {
  
  const [inputText, setInputText] = useState(SOCIAL_PRESETS[0].text);
  const [isParsing, setIsParsing] = useState(false);
  const [parsedOutput, setParsedOutput] = useState<{
    classification: string;
    confidence: number;
    coords: string;
  } | null>(null);

  const handleParseDistress = () => {
    setIsParsing(true);
    setTimeout(() => {
      const match = SOCIAL_PRESETS.find(p => p.text === inputText) || {
        classification: "DISTRESS_IDENTIFIED",
        confidence: 84.8,
        coords: `${currentScenario.coordinates.lat.toFixed(4)}, ${currentScenario.coordinates.lng.toFixed(4)}`
      };
      setParsedOutput({
        classification: match.classification,
        confidence: match.confidence,
        coords: match.coords
      });
      setIsParsing(false);
    }, 850);
  };

  
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
    chatBottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [chatMessages, isChatLoading]);

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
          context: `Target: ${currentScenario.name}, Type: ${currentScenario.type}, Severity: ${currentScenario.severity}`,
          history: chatMessages.slice(-6).map(m => ({ role: m.role, content: m.content }))
        })
      });

      const data = await response.json();
      if (response.ok) {
        setChatMessages(prev => [...prev, { role: "model", content: data.reply, mode: data.mode }]);
      } else {
        setChatMessages(prev => [...prev, { role: "model", content: `### Error Processing Prompt\n\nCould not fetch response: ${data.error || "Unknown server failure"}` }]);
      }
    } catch (err: any) {
      console.error(err);
      setChatMessages(prev => [...prev, { role: "model", content: `### Server Communication Failure\n\nFailed to dispatch prompt. Ensure your full-stack environment has compiled correctly.` }]);
    } finally {
      setIsChatLoading(false);
    }
  };

  return (
    <div className="space-y-6" id="nlp-copilot-pane">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6" id="nlp-top-grid">

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-nlp-distress">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-yellow-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [9]: Social Emergency NLP Intelligence
                </h3>
              </div>
              <Terminal className="w-4 h-4 text-yellow-400" />
            </div>

            <p className="text-xs text-slate-400 mb-4 font-sans leading-relaxed">
              Processes unstructured, noisy distress feeds in real-time. Translates sentence semantic maps using RoBERTa networks to automatically extract coordinates.
            </p>

            <div className="space-y-3 font-mono text-[10px]" id="nlp-presets">
              <span className="text-[9px] uppercase tracking-wider text-slate-500 font-bold block mb-1">
                Select Twitter/Social Distress Preset:
              </span>
              <div className="grid grid-cols-1 gap-2">
                {SOCIAL_PRESETS.map((preset, pIdx) => (
                  <button
                    key={pIdx}
                    onClick={() => setInputText(preset.text)}
                    className={`text-left p-2 rounded-lg border text-[9px] truncate transition-all ${
                      inputText === preset.text 
                        ? "bg-yellow-500/10 border-yellow-500/40 text-yellow-400 font-bold" 
                        : "bg-slate-950/60 border-slate-900 text-slate-400 hover:text-slate-200"
                    }`}
                  >
                    "{preset.text}"
                  </button>
                ))}
              </div>

              <div className="mt-3">
                <label className="block text-[9px] uppercase font-mono tracking-wider text-slate-500 mb-1.5 font-bold">Unstructured Input Feed Parser</label>
                <textarea
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  rows={2}
                  className="w-full bg-slate-950 border border-slate-900 rounded-lg py-2 px-3 text-xs text-slate-200 outline-none focus:border-yellow-500/50 resize-none font-sans"
                />
              </div>

              <button
                onClick={handleParseDistress}
                disabled={isParsing}
                className="w-full h-10 bg-yellow-950/40 border border-yellow-500/40 hover:bg-yellow-500/10 text-yellow-400 rounded-lg text-xs font-bold uppercase transition-all flex items-center justify-center gap-2"
                id="btn-parse-nlp"
              >
                {isParsing ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    Extracting Pydantic Boundaries...
                  </>
                ) : (
                  <>
                    <Search className="w-3.5 h-3.5" />
                    Parse Distress Feed
                  </>
                )}
              </button>
            </div>
          </div>

          <div className="mt-4" id="mod9-output">
            {parsedOutput ? (
              <div className="bg-[#04070d] border border-slate-950 rounded-xl p-3 space-y-2 font-mono text-[9px] animate-fadeIn">
                <div className="flex justify-between border-b border-slate-900 pb-1 font-bold text-slate-500">
                  <span>RoBERTa NLP Classifier Stream Output</span>
                  <span className="text-yellow-400">RESOLVED</span>
                </div>
                <div>Extracted Category: <span className="font-bold text-red-400">{parsedOutput.classification}</span></div>
                <div className="grid grid-cols-2 gap-2 pt-1 border-t border-slate-900/60">
                  <div>Model confidence: <span className="text-slate-200 font-bold">{parsedOutput.confidence}%</span></div>
                  <div>Geocodes: <span className="text-slate-300 font-bold select-all">{parsedOutput.coords}</span></div>
                </div>
              </div>
            ) : (
              <div className="bg-[#04070d] border border-slate-950 rounded-xl p-5 text-center text-slate-600 font-mono text-[10px] italic">
                Select a tweet above and trigger the NLP parser to decode variables.
              </div>
            )}
          </div>
        </div>

        
        <div className="bg-[#090e18] border border-slate-900 rounded-xl p-5 flex flex-col justify-between" id="card-module-rag-chat">
          <div>
            <div className="flex items-center justify-between border-b border-slate-900 pb-3 mb-4">
              <div className="flex items-center gap-2">
                <div className="w-2.5 h-2.5 bg-cyan-400 rounded-sm" />
                <h3 className="text-sm font-semibold uppercase tracking-wider text-slate-100 font-mono">
                  [10]: Multimodal Emergency Copilot
                </h3>
              </div>
              <MessageCircle className="w-4 h-4 text-cyan-400" />
            </div>

            <p className="text-xs text-slate-400 mb-3 font-sans leading-relaxed">
              Retrieval Augmented Generation (RAG) agent integrating local contingency briefs into LLM prompts.
            </p>

            <div className="bg-[#03060c] border border-slate-950 rounded-xl flex flex-col h-56 overflow-hidden" id="internal-chat-terminal">
              <div className="flex-1 p-3 overflow-y-auto space-y-2 scrollbar-thin">
                {chatMessages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`max-w-[90%] p-2 rounded-lg text-[10px] leading-relaxed font-sans ${
                      msg.role === "user"
                        ? "bg-slate-900 border border-slate-800 text-slate-200 self-end ml-auto"
                        : "bg-[#04070c] border border-slate-950 text-slate-300 mr-auto font-mono text-[9px]"
                    }`}
                  >
                    <div className="flex justify-between items-center text-[7.5px] uppercase font-mono text-slate-500 mb-1 font-bold">
                      <span>{msg.role === "user" ? "Command Ops" : "Aegis Assistant"}</span>
                      {msg.mode && (
                        <span className={`${msg.mode === "live" ? "text-emerald-400" : "text-amber-500"}`}>{msg.mode}</span>
                      )}
                    </div>
                    <div className="whitespace-pre-wrap select-text">{msg.content}</div>
                  </div>
                ))}

                {isChatLoading && (
                  <div className="bg-[#04070c] border border-slate-950 rounded-lg p-2 mr-auto text-[9px] font-mono text-cyan-400 flex items-center gap-1.5 animate-pulse">
                    <Loader2 className="w-3.5 h-3.5 animate-spin text-cyan-400" />
                    Consulting RAG vectors...
                  </div>
                )}
                <div ref={chatBottomRef} />
              </div>

              
              <div className="p-2 border-t border-slate-950 bg-slate-950 flex items-center gap-1">
                <input
                  type="text"
                  placeholder="Ask command copilot..."
                  value={chatInput}
                  onChange={(e) => setChatInput(e.target.value)}
                  onKeyDown={(e) => { if (e.key === "Enter") { e.preventDefault(); handleSendMessage(); } }}
                  className="flex-1 bg-slate-900 border border-slate-800 rounded px-2.5 py-1 text-[10px] text-slate-200 outline-none font-mono focus:border-cyan-500/50"
                />
                <button
                  onClick={() => handleSendMessage()}
                  disabled={isChatLoading || !chatInput.trim()}
                  className="p-1 px-2 border border-cyan-800/40 bg-cyan-950/20 text-cyan-400 rounded text-[9.5px] font-mono hover:bg-cyan-500/15"
                >
                  Send
                </button>
              </div>

            </div>
          </div>

          <div className="mt-3 flex gap-1.5 overflow-x-auto py-1 scrollbar-thin">
            <button
              onClick={() => handleSendMessage("Map out open road alternates bypassing high hazard points.")}
              className="py-1 px-2 border border-slate-800 bg-slate-950 rounded-lg text-[8.5px] text-slate-400 hover:text-cyan-400 font-mono font-semibold whitespace-nowrap uppercase transition-colors"
            >
              🗺️ Alternate Roads
            </button>
            <button
              onClick={() => handleSendMessage("Retrieve pre and post disaster satellite segmentations.")}
              className="py-1 px-2 border border-slate-800 bg-slate-950 rounded-lg text-[8.5px] text-slate-400 hover:text-cyan-400 font-mono font-semibold whitespace-nowrap uppercase transition-colors"
            >
              🛰️ SAR Multi-Poles
            </button>
          </div>
        </div>

      </div>
    </div>
  );
}
