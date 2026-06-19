export interface DisasterConfig {
  id: string;
  name: string;
  type: "flood" | "wildfire" | "earthquake" | "hurricane";
  severity: "CAT-3" | "CAT-4" | "CAT-5" | "E-X" | "V-H";
  coordinates: { lat: number; lng: number };
  activeThreatCount: number;
  sheltersOpen: number;
}

export interface SatelliteImage {
  id: string;
  name: string;
  preUrl: string;
  postUrl: string;
}

export interface IngestedLog {
  timestamp: string;
  source: string;
  id: string;
  type: string;
  status: "SUCCESS" | "VALIDATING" | "ERROR" | "INGESTED";
  payload: any;
}

export interface AgentStep {
  agent: string;
  statusString: string;
  action: string;
  log: string;
  targetUnit?: string;
  coordinates?: string;
}

export interface DroneNode {
  id: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  status: "SEARCHING" | "SCANNING" | "SIGNAL_LOCKED" | "RETURN";
  meshStrength: number;
  targetsFound: number;
}

export interface SimulationState {
  precipitation: number; // mm/hr
  powerGridCapacity: number; // %
  roadCongestion: number; // %
  hazardSpreadRadius: number; // meters
}

export interface OptimizationResult {
  generation: number;
  bestFitness: number;
  allocation: {
    helicopters: number;
    ambulances: number;
    tacticalSquads: number;
    drones: number;
  };
  efficiencyPct: number;
}
