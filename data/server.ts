import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { GoogleGenAI } from "@google/genai";
import dotenv from "dotenv";

dotenv.config();

async function startServer() {
  const app = express();
  const PORT = 3000;

  app.use(express.json());

// Simulated Action Generator for offline or unavailable Gemini API key states
function generateSimulatedReply(message: string, context: string): string {
  const lower = message.toLowerCase();
  const contextStr = context || "Active Command Grid";

  if (lower.includes("evac") || lower.includes("route") || lower.includes("transport") || lower.includes("road") || lower.includes("bypass") || lower.includes("dijkstra")) {
    return `### 🛰️ Simulated Action Plan: Autonomous Routing & Navigation
    
Based on your request regarding **evacuation routing and transit corridor states**, Aegis has formulated the following safe navigation criteria for **${contextStr}**:

1. **Optimal Path Calculation**: 
   - Primary route corridor (Highway Alpha) is congested or waterlocked. Rerouting traffic through **Corridor Beta** (Alternative H3 Index Cell: \`832685fffffffff\`).
   - Dijkstra's weight parameters adjusted: Hazard risk factor increased to \`0.92\`, road friction multiplier set to \`0.45\`.

2. **Flow & Bottleneck Gating**:
   - Limit flow rate to **280 vehicles/minute** to prevent gridlock at key intersection points.
   - Dispatch emergency route maps directly to onboard vehicular navigation units via regional networks.

3. **Asset Operations**:
   - Standard transit buses are restricted from flooded zone sections. 
   - Deploying 3 Tactical All-Terrain Utility Vehicles to shepherd stranded citizen units.`;
  }
  
  if (lower.includes("agent") || lower.includes("langgraph") || lower.includes("coordinate") || lower.includes("autonomous") || lower.includes("mesh")) {
    return `### 🤖 Task Plan: Cooperating Multi-Agent State Machine
    
The **Multi-Agent Rescue Grid** is running deep coordination sequences for **${contextStr}**. Running plan state details:

- **Situation Assessment Agent (Node-A)**: Logs 84% probability of downstream blockage. Initiates immediate warning broadcast.
- **Decision Router (Node-B)**: Evaluates structural decay of alternate crossing points. Identifies 2 viable helicopter landing cells.
- **Supply Allocation Agent (Node-C)**: Redirects 6 tactical medics with emergency response packs to the northeast quadrant.
- **Tactical Rescue Agent (Node-D)**: Coordinates drone paths and issues search patterns over heat signature grids.

*Plans are fully consolidated in the central control registry.*`;
  }

  if (lower.includes("satellite") || lower.includes("flood") || lower.includes("damage") || lower.includes("sar") || lower.includes("image") || lower.includes("radar")) {
    return `### 🛰️ Geospatial Inference: Satellite Intelligence Analysis
    
Analyzing the requested post-event dual-polarized **Sentinel SAR (Synthetic Aperture Radar)** VV/VH difference tensor for **${contextStr}**:

- **Pre/Post Difference SSIM**: Structural Similarity Index exhibits a 34% drop compared to baseline mapping.
- **Flood Zone Extent Classifier (Swin-VIT)**: 
  - Estimated 1,482 Hectares fully submerged.
  - Pixel-wise intersection-over-union confidence is evaluated at \`96.2%\`.
  - Inundation contours are populated in the GIS interface layers.`;
  }

  if (lower.includes("alert") || lower.includes("broadcast") || lower.includes("warn") || lower.includes("cell") || lower.includes("report")) {
    return `### 🚨 Strategic Communication & Early Warning Dispatch
    
Executing active early warning broadcast protocols within the targeted **${contextStr}** boundary:

1. **Broadcast Density**: Transmitting high-priority Cell Broadcast warning packets to all mobile devices within the calculated threat radius.
2. **Channel Modulation**: Multi-frequency alert signals dispatched. Local transceiver cells are operating at 95% throughput reliability.
3. **Drafted Advisory Action**:
   - *\"CRITICAL SURGE INBOUND. Reroute immediately to upper ridge shelters. Avoid using Sector-4 bridges. Emergency personnel are standing by.\"*`;
  }

  return `### 🚨 Crisis Command Copilot Response

Acknowledging tactical input for grid context **${contextStr}**:
*\"${message}\"*

Aegis has synthesized the current system parameters and generated the following situational analysis:

- **Risk Identification**: High priority indices isolated to coastal drainage regions. Topographic slope vectors indicate cascading flash surge risks.
- **Dynamic Optimization**: The genetic fleet allocator suggests maintaining a defensive staging formation near the central hub while waiting for radar visual validation.
- **Next Tactical Steps**:
  1. Audit active river gauge telemetry streams in the GIS sub-pane.
  2. Query the Knowledge Graph to verify if evacuation corridors remain clear of structural debris.
  3. Dispatch high-resolution thermal imaging drones to scan for isolated personnel.`;
}

  // API Route - Disaster Management Copilot Chat
  app.post("/api/copilot", async (req, res) => {
    try {
      const { message, context, history } = req.body;
      if (!message) {
        return res.status(400).json({ error: "Message is required." });
      }

      const apiKey = process.env.GEMINI_API_KEY;

      if (!apiKey || apiKey === "MY_GEMINI_API_KEY" || apiKey.trim() === "" || apiKey === "undefined") {
        console.warn("GEMINI_API_KEY is not configured or placeholder. Falling back to local offline simulation.");
        const reply = generateSimulatedReply(message, context);
        return res.json({ reply, mode: "simulated" });
      }

      // Initialize real server-side Gemini Client
      const ai = new GoogleGenAI({
        apiKey: apiKey,
        httpOptions: {
          headers: {
            "User-Agent": "aistudio-build",
          },
        },
      });

      // Assemble system instruction detailing the platform's role
      const systemInstruction = `You are the core cognitive engine of the "AI-Powered Disaster Prediction, Crisis Intelligence & Autonomous Response Platform," acting as an elite command advisor for global crisis coordinators. 
You possess advanced knowledge in geospatial intelligence, satellite image processing (SAR, ViTs), Temporal Fusion Transformers, graph search routing algorithms (Neo4j, D9-Dijkstra), operations research (Genetic Algorithms for supply distribution), LangGraph multi-agent orchestration, and early warning broadcasting.

Structure your responses using clean, professional, action-oriented, technical Markdown. Never use flowery language. Maintain the perspective of a command console assistant. Use technical terms like H3 indexing, dual-polarized SAR tensors, cascading risks, causal graph analysis, explainable SHAP values, and network flow optimization where appropriate, aligning with the platform's 18 core systems.

Current context is active in the user UI. Focus on actionable crisis logic. Reference the user's selected disaster settings (${context || 'N/A'}) in your answer.`;

      // Build chat or single prompt
      const contents = history && history.length > 0 
        ? [...history.map((h: any) => ({
            role: h.role === "user" ? "user" as const : "model" as const,
            parts: [{ text: h.content }]
          })), { role: "user" as const, parts: [{ text: message }] }]
        : [{ role: "user" as const, parts: [{ text: message }] }];

      try {
        const response = await ai.models.generateContent({
          model: "gemini-3.5-flash",
          contents: contents,
          config: {
            systemInstruction: systemInstruction,
            temperature: 0.15,
          }
        });

        return res.json({ reply: response.text || "No response received.", mode: "live" });
      } catch (geminiError: any) {
        console.warn("Real Gemini API request failed. Falling back to simulated reply:", geminiError);
        const reply = generateSimulatedReply(message, context);
        return res.json({ 
          reply: reply + `\n\n*Note: Operating in local diagnostic mode (Gemini API unavailable: ${geminiError.message || "Endpoint error - status unavailable"})*`, 
          mode: "simulated" 
        });
      }
    } catch (error: any) {
      console.error("Gemini Copilot Error:", error);
      return res.status(500).json({ error: error.message || "Failed to process Copilot request." });
    }
  });

  // Serve static files in production or hook Vite in development
  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa",
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`Server executing successfully on http://0.0.0.0:${PORT}`);
  });
}

startServer();
