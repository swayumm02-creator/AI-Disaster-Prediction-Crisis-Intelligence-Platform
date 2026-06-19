export interface  {
  id: number;
  title: string;
  category: string;
  architectureSummary: string;
  techStack: string[];
  equation?: string;
  equationDescription?: string;
  codeBlock?: {
    language: string;
    code: string;
  };
}

export const
  {
    id: 1,
    title: "Multi-Source Disaster Data Fusion Engine",
    category: "Ingestion Pipelines",
    architectureSummary: "Architects an event-driven ingestion pipeline handling asynchronous, heterogeneous data streams (Sentinel SAR images, river gauge IoT telemetries, and social distress calls). High-throughput data validated using Pydantic schemas is processed sequentially and dispatched into specific Apache Kafka clusters for downstream inference engines.",
    techStack: ["FastAPI", "Apache Kafka", "Pydantic v2", "Uvicorn"],
    codeBlock: {
      language: "python",
      code: `import json
import logging
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from fastapi import FastAPI, HTTPException
from kafka import KafkaProducer

app = FastAPI()
logging.basicConfig(level=logging.INFO)

# Thread-safe Kafka Producer Initialization (Lazy client configuration)
try:
    producer = KafkaProducer(
        bootstrap_servers=['kafka-broker.crisis-ops:9092'],
        value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )
except Exception as e:
    logging.error(f"Kafka client connection bypassed in offline mode: {e}")
    producer = None

class MultimodalPayload(BaseModel):
    source: str = Field(..., description="Ingestion origin channel: SAR, IoT, or SocialMedia")
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    sensor_value: Optional[float] = Field(None, description="Physical sensor telemetry reading (e.g. water height in meters)")
    unstructured_text: Optional[str] = Field(None, max_length=1000, description="Distress text messages")

    @field_validator('sensor_value')
    @classmethod
    def validate_sensors(cls, val: float, info) -> float:
        if info.data.get('source') == 'IoT' and val is None:
            raise ValueError("All physical inputs must carry sensor floating values.")
        return val

@app.post("/api/v1/ingest")
async def ingest_disaster_pulse(payload: MultimodalPayload):
    validated_data = payload.model_dump()
    topic = f"disaster.telemetry.{payload.source.lower()}"
    
    if producer:
        try:
            future = producer.send(topic, value=validated_data)
            future.get(timeout=5)  # Blocking sync confirm inside HTTP frame
            logging.info(f"Payload routed to kafka topic {topic}")
            return {"status": "SUCCESS", "topic": topic, "uuid": hash(str(validated_data))}
        except Exception as err:
            logging.error(f"Write failure: {err}")
            raise HTTPException(status_code=500, detail="Disaster pipeline queue full.")
    else:
        # Diagnostic Mock Response
        return {
            "status": "INGEST_SIMULATED", 
            "message": "Producer operating in detached mode.",
            "data": validated_data
        }
`
    }
  },
  {
    id: 2,
    title: "Satellite Image Intelligence Segmenter",
    category: "Computer Vision",
    architectureSummary: "Implements cloud-penetrating synthetic aperture radar (SAR) flood segmentation. Utilizing a dual-polarized co-polarization (VV) and cross-polarization (VH) Sentinel tensor pair, a deep neural segmentation pipeline (Swin/SegFormer backbone) isolates standing water anomalies overlaid against pre-event topological baselines.",
    techStack: ["PyTorch", "Swin Transformer", "Rasterio", "SegFormer"],
    codeBlock: {
      language: "python",
      code: `import torch
import torch.nn as nn
import torch.nn.functional as F

class SatelliteDifferenceSegmenter(nn.Module):
    def __init__(self, in_channels: int = 4, classes: int = 3):
        super(SatelliteDifferenceSegmenter, self).__init__()
        # Ingests pre-event (VV/VH) and post-event (VV/VH) dual-pol stacks
        self.encoder = nn.Sequential(
            nn.Conv2d(in_channels, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(2)
        )
        # Deep convolutional decoding segmenter with multi-scale skip layers
        self.decoder = nn.Sequential(
            nn.Conv2d(128, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.ConvTranspose2d(64, classes, kernel_size=2, stride=2)
        )

    def forward(self, pre_tensor: torch.Tensor, post_tensor: torch.Tensor) -> torch.Tensor:
        # Fuse dual-pol spatial dimensions of historical and target images
        # Dimensions: [Batch Size, Channels (VV+VH = 2), H, W]
        fused_stack = torch.cat([pre_tensor, post_tensor], dim=1) # [B, 4, H, W]
        latent = self.encoder(fused_stack)
        logit_output = self.decoder(latent)
        # Output: [B, Number of Classes (0: Normal, 1: Flash Flood, 2: Structural Rubble), H, W]
        return F.softmax(logit_output, dim=1)

# Execution instantiation
def run_damage_segmentation():
    # Model parameters: Batch=2, Channels=4, Extent=512x512
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = SatelliteDifferenceSegmenter().to(device)
    
    pre_event = torch.randn(2, 2, 512, 512).to(device)
    post_event = torch.randn(2, 2, 512, 512).to(device)
    
    segmentation_map = model(pre_event, post_event)
    print(f"Segmentation output shape configured successfully: {segmentation_map.shape}")
`
    }
  },
  {
    id: 3,
    title: "Disaster Risk Forecasting AI",
    category: "Predictive AI Systems",
    architectureSummary: "Models highly localized cascading disaster hazards. Solves flooding inundation vectors and wildland fuel thresholds across space and time using a hybrid Temporal Fusion Transformer (TFT) joined with Graph Neural Networks (GNNs). Spatiotemporal data is structured as dynamic networks representing rivers, road links, and forest barriers.",
    techStack: ["PyTorch Geometric", "DGL", "Temporal Fusion Transformer"],
    equation: "L_{total} = w_1 L_{empirical}(\\hat{y}, y) + w_2 L_{physics}(U_{river} - \\nabla \\cdot H_{topography})",
    equationDescription: "The total optimization objective function compounding empirical cross-entropy loss with spatial physical flood fluid-dynamics constraints (Navier-Stokes derivative estimators representing basin heights)."
  },
  {
    id: 4,
    title: "Geospatial AI Risk Engine (H3 Space)",
    category: "GIS & Geospatial",
    architectureSummary: "Aggregates massive raster boundaries into highly optimized discrete index cell indexes using Uber's H3 Spatial indexing and PostGIS layers. This eliminates slow polygons overlapping checks and projects all points, assets, and floodzones directly into highly queryable 64-bit integer H3 resolutions.",
    techStack: ["H3-Py", "GeoPandas", "Shapely", "PostGIS"],
    codeBlock: {
      language: "python",
      code: `import geopandas as gpd
from shapely.geometry import Polygon, Point
import h3

def compute_h3_geospatial_intersections(hazard_poly_coords, infrastructure_points, h3_resolution=9):
    # Step 1: Create a hazard geometry polygon
    hazard_geometry = Polygon(hazard_poly_coords)
    hazard_gdf = gpd.GeoDataFrame(index=[0], geometry=[hazard_geometry], crs="EPSG:4326")
    
    # Step 2: Extract spatial boundary polyfill in H3 Index space
    coords = list(hazard_geometry.exterior.coords)
    # Re-order to [lat, lng] list for H3 library formats
    lat_lng_coords = [[pt[1], pt[0]] for pt in coords]
    
    # Extract list of 64-bit cell addresses within the perimeter
    filled_cells = h3.polygon_to_cells(h3.LatLngPoly(lat_lng_coords), h3_resolution)
    h3_exclusion_set = set(filled_cells)
    
    # Step 3: Check critical infrastructure nodes
    vulnerable_assets = []
    for info in infrastructure_points:
        pt = Point(info['lng'], info['lat'])
        # Spatial H3 translation
        node_cell = h3.latlng_to_cell(info['lat'], info['lng'], h3_resolution)
        
        # O(1) intersection testing instead of slow geometric polygon overlay checks
        if node_cell in h3_exclusion_set:
            vulnerable_assets.append({
                "id": info['id'],
                "h3_index": node_cell,
                "lat": info['lat'],
                "lng": info['lng'],
                "risk_status": "CRITICAL_THREAT"
            })
            
    return vulnerable_assets, h3_exclusion_set

# Example execution dataset
hazard_zone = [(-122.42, 37.78), (-122.40, 37.78), (-122.40, 37.76), (-122.42, 37.76)]
telecom_substations = [
    {"id": "Sub-01", "lat": 37.77, "lng": -122.41},
    {"id": "Sub-02", "lat": 37.89, "lng": -122.21}
]

vulnerable, cells = compute_h3_geospatial_intersections(hazard_zone, telecom_substations)
print(f"Isolated Vulnerable Infrastructure Elements: {vulnerable}")
`
    }
  },
  {
    id: 5,
    title: "Digital Twin Sandbox Dynamics",
    category: "Sandbox Simulation",
    architectureSummary: "Executes a matrix-plane simulation engine illustrating systemic failure cascades. Translates severe storms into road gridlock indices and power substation outages dynamically. This models secondary risks prior to real-world escalation using a dynamic state transition graph.",
    techStack: ["Go Matrix", "SimPy", "NumPy Matrix Math"],
    equation: "S_{t+1} = A \\cdot S_t + B \\cdot C_{precipitation} - R_{mitigation}",
    equationDescription: "The state transitions matrix equation computing simultaneous degradation across energy grids, traffic capacity, and physical structures."
  },
  {
    id: 6,
    title: "Multi-Agent Autonomous Rescue Coordination",
    category: "Autonomous Agents",
    architectureSummary: "Runs an autonomous routing network mapping specific rescue objectives across a collaborative agent mesh (Rescue, Medical, Supply Chain, and Situation Analysis). Implemented using LangGraph to route critical event telemetry conditionally, synchronize global triage states, and dispatch assets dynamically.",
    techStack: ["LangGraph", "LangChain Core", "LangGraph State", "Pydantic"],
    codeBlock: {
      language: "python",
      code: `from typing import Dict, TypedDict, List, Annotated
from langgraph.graph import StateGraph, END

# Define absolute global crisis coordination state
class CommandCenterState(TypedDict):
    active_threat: str
    risk_level: str
    allocated_ambulances: int
    requested_supplies: list
    agent_logs: list
    cleared_for_dispatch: bool

# Agent Node A: Situation Analysis
def analyze_sensor_streams(state: CommandCenterState) -> Dict:
    logs = list(state.get("agent_logs", []))
    logs.append("Situation Agent: Assessed structural landslide triggers. High alert.")
    return {
        "risk_level": "V-H" if state["active_threat"] == "Landslide" else "MED",
        "agent_logs": logs
    }

# Agent Node B: Supply Allocation
def dispatch_supply_chain(state: CommandCenterState) -> Dict:
    logs = list(state.get("agent_logs", []))
    supplies = list(state.get("requested_supplies", []))
    supplies.append("Class-1 Trauma Packs")
    logs.append("Supply Chain Agent: Procured trauma units from regional base.")
    return {
        "requested_supplies": supplies,
        "agent_logs": logs
    }

# Agent Node C: Tactical Rescue
def manage_rescue_teams(state: CommandCenterState) -> Dict:
    logs = list(state.get("agent_logs", []))
    logs.append("Rescue Agent: Multi-spectral UAV sweeps dispatched.")
    return {
        "allocated_ambulances": state.get("allocated_ambulances", 0) + 4,
        "cleared_for_dispatch": True,
        "agent_logs": logs
    }

# Conditional routing branch based on computed hazard state
def command_evaluation_router(state: CommandCenterState) -> str:
    if state["risk_level"] == "V-H":
        return "supply_chain_node"
    return "rescue_dispatch_node"

# Building the absolute LangGraph Orchestration Topology
workflow = StateGraph(CommandCenterState)

workflow.add_node("situation_node", analyze_sensor_streams)
workflow.add_node("supply_chain_node", dispatch_supply_chain)
workflow.add_node("rescue_dispatch_node", manage_rescue_teams)

workflow.set_entry_point("situation_node")

# Dynamic state conditional transitions
workflow.add_conditional_edges(
    "situation_node",
    command_evaluation_router,
    {
        "supply_chain_node": "supply_chain_node",
        "rescue_dispatch_node": "rescue_dispatch_node"
    }
)

# Connect linear nodes to conclusion
workflow.add_edge("supply_chain_node", "rescue_dispatch_node")
workflow.add_edge("rescue_dispatch_node", END)

# Compile production-safe agent engine
autonomous_rescue_mesh = workflow.compile()
print("LangGraph Agent Coordination Network compiled successfully.")
`
    }
  },
  {
    id: 7,
    title: "Autonomous Evacuation Planner",
    category: "Routing & Physics",
    architectureSummary: "Isolates maximum safety routing algorithms through dense road corridors under catastrophic weather conditions. Applying custom Multi-Objective Dijkstra networks combined with Proximal Policy Optimization (PPO), the system calculates adaptive escape pathways dynamically modifying node weights based on flood gauges.",
    techStack: ["Reinforcement Learning (PPO)", "OMNet++", "NetworkX Math"],
    equation: "R_{s,a} = - (\\alpha T_{travel} + \\beta D_{hazard} + \\gamma C_{congestion})",
    equationDescription: "The reinforcement learning reward metric penalizing high hazard proximity weights and severe road congestion volumes."
  },
  {
    id: 8,
    title: "AI Rescue Resource Optimization Core",
    category: "Operations Research",
    architectureSummary: "Computes complex resource allocation vectors across critical tactical gear (Air Helicopters, Land Ambulances, Boat responders, and Medicine crates) using Operations Research Mixed-Integer Linear Programming (MILP) or advanced Genetic Mutators to secure maximum population coverage within a minimal time frame.",
    techStack: ["SciPy Opt", "GLPK solver", "DEAP Genetic Lib"],
    equation: "\\max_{X} \\sum_{i} P_i X_i - \\lambda \\sum_{j} c_j X_j"
  },
  {
    id: 9,
    title: "Social Media Emergency NLP Intelligence",
    category: "NLP & LLMs",
    architectureSummary: "Processes streaming, noisy unstructured text streams directly from geo-coded community feeds. Utilizing fine-tuned RoBERTa encoders and NER taggers, it performs real-time classification, filters disinformation vectors, and extracts geolocation variables to map active rescue coordinates.",
    techStack: ["Hugging Face", "PyTorch", "SpaCy GIS", "RoBERTa Clas"],
    equation: "P(x_{distress}) = \\sigma(W^T_d \\cdot h_{RoBERTa} + b_d)"
  },
  {
    id: 10,
    title: "Multimodal Emergency Copilot Architecture",
    category: "NLP & LLMs",
    architectureSummary: "Architects a dual-mode retrieval augmented generation (RAG) agent integrated into administrative servers. Merges local crisis templates, weather radars, and topological map overlays directly into LLM prompts using vector-context bindings to generate complete structured situational reports.",
    techStack: ["@google/genai", "LangChain LLM", "ChromaDB Vector"],
    equation: "E_{prompt} = \\Psi(Q_{user}, K_{context}, M_{raster})"
  },
  {
    id: 11,
    title: "Disaster Knowledge Graph System",
    category: "Graph Databases",
    architectureSummary: "Executes ultra-high speed structural query checks across highly relational entity vectors. By translating topological grids, critical facilities, and road links into a Graph Database, path finding algorithms isolate open escape routes the instant physical routes are compromised.",
    techStack: ["Neo4j Graph Database", "NetworkX", "GraphRAG"],
    codeBlock: {
      language: "cypher",
      code: `// Neo4j Cypher Optimized Alternate Route Solver Algorithm
// Designed to find the shortest viable path bypassing flooded/blocked road systems
MATCH (origin:Location {name: "District-A_Triage"})
MATCH (destination:Hospital {name: "Central_Trauma_Base"})

// Identify all intervening roads and nodes skipping BLOCKED paths
MATCH path = shortestPath((origin)-[:CONNECTED_BY*..15]->(destination))
WHERE NONE(road IN relationships(path) WHERE road.status = "BLOCKED")
  AND NONE(node IN nodes(path) WHERE node.status = "FLOOD_SURGE")

// Extract properties for automated routing coordination systems
RETURN 
  [n in nodes(path) | n.name] AS NodeSequence,
  [r in relationships(path) | r.roadCode] AS TransitCorridors,
  reduce(totalDist = 0.0, r IN relationships(path) | totalDist + r.distanceKm) AS TotalDistanceKm,
  reduce(transitTime = 0.0, r IN relationships(path) | transitTime + (r.distanceKm / r.maxSafeSpeedKmh)) AS ProjectedTransitTimeHrsByEMS
ORDER BY ProjectedTransitTimeHrsByEMS ASC
LIMIT 3;
`
    }
  },
  {
    id: 12,
    title: "Early Warning Cell Broadcast Core",
    category: "Emergency Alerting",
    architectureSummary: "Translates active spatial threat grids directly into live geo-fenced Cell Broadcast notifications. By indexing subscriber device positions inside H3 cells, localized multicellular alerts are dispatched in sub-second intervals across regional cellular networks.",
    techStack: ["H3 Hex Geo", "SMS Gateways", "Twilio API", "SIP Signaling"],
    equation: "A_{geo} = \\bigcup_{i=1}^n H3\\_Index_{resolution-8}"
  },
  {
    id: 13,
    title: "Explainable AI (XAI) Center",
    category: "Explainable AI",
    architectureSummary: "Extracts global feature classifications and SHAP relevance attributes from neural risk forecasters. Converts high-dimension model weights into explicit, human-comprehensible justifications explaining exactly why specific emergency actions have been prioritized.",
    techStack: ["SHAP", "LIME", "InterpretML"],
    equation: "g(z') = \\phi_0 + \\sum_{i=1}^M \\phi_i z'_i"
  },
  {
    id: 14,
    title: "Economic Impact Modeling Engine",
    category: "Predictive AI Systems",
    architectureSummary: "Models secondary macroeconomic and asset depreciation damage using structural equation networks. Leverages topographical satellite inundation contours, agricultural supply paths, and building assets variables to forecast systemic downstream supply chain halts.",
    techStack: ["Statsmodels", "SimPy Econometrics", "Excel Solver Engine"],
    equation: "D_{economic} = \\Phi_{direct}(Assets) \\times M_{multiplier}(Traffic\\_Loss)"
  },
  {
    id: 15,
    title: "Post-Disaster Change Differencer",
    category: "Computer Vision",
    architectureSummary: "Compares spatial rasters dynamically across pre/post target timelines to construct high-speed structural damage indices. Evaluates pixel-level difference ratios to isolate collapsed buildings and locate blocked emergency roads using robust F1-score evaluation boundaries.",
    techStack: ["OpenCV Geospatial", "PyTorch Segment", "PyDM"],
    equation: "D_{diff}(x,y) = || I_{post}(x,y) - I_{pre}(x,y) || > \\theta_{damage}"
  },
  {
    id: 16,
    title: "Drone Swarm Mesh Coordination Core",
    category: "Autonomous Systems",
    architectureSummary: "Orchestrates complex decentralized search path coordination algorithms across multi-UAV drone fleets. Node swarm agents maintain constant P2P ad-hoc mesh networks, optimizing collective search boundaries under intense wind metrics, and flagging human heat indices.",
    techStack: ["ROS-2 Swarm", "WebSockets P2PJS", "Pixhawk PX4 Autopilot"],
    equation: "V_{swarm, i} = w_a A_{alignment} + w_s S_{separation} + w_c C_{cohesion} + w_g G_{search\\_goal}"
  },
  {
    id: 17,
    title: "Generative AI Reporting Engine",
    category: "NLP & LLMs",
    architectureSummary: "Assembles and formats highly technical situational logs, damage segmentations, and agent traces into professional multi-page crisis briefings. Renders outputs dynamically using beautiful styled templates designed for command team signatures.",
    techStack: ["Markdown PDF Compiler", "JSZip Report", "React Parser"],
    equation: "T_{briefing} = \\Lambda(State_{logs}, Damage\\_Index, Resource_{allocation})"
  },
  {
    id: 18,
    title: "Predictive Recovery Planner",
    category: "Predictive AI Systems",
    architectureSummary: "Synthesizes comprehensive schedules mapping public helper entities restoration timelines over month-long recovery sequences. Considers dynamic critical dependencies (e.g. power substations must reboot prior to routing automated subways), optimizing workflows through critical path pipelines.",
    techStack: ["Gantt CPM Math", "NumPy Scheduling", "NetworkX Paths"],
    equation: "T_{recovery}(\\mathbf{U}) = \\sum_{u \\in \\mathbf{U}} \\max(Start_u + d_u, \\{Complete_{prev} | prev \\rightarrow u\\})"
  }
];
