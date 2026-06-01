// ═══════════════════════════════════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════════════════════════════════
let isIon=false, injecting=false, ramped=false, filling=false;
let b1Count=0, b2Count=0, collisions=0;
const NEEDED=6;
let lhcDots={b1:[],b2:[]};
let lhcSpeed=0.0078; // rad/ms bei Injektionsenergie (Proton) – schneller als alle Vorbeschleuniger
let lhcAngle=0, lhcRunning=false, lhcLastT=null;
let lhcEnergy=450; // GeV
// Per-Detektor-Datenspeicher: jeder Detektor akkumuliert NUR sein eigenes Spektrum.
// So zeigt ein Detektorwechsel konsequent das physikalisch mögliche Spektrum dieses Detektors.
let massStore = {ATLAS:[], CMS:[], ALICE:[], LHCB:[]};   // akkumulierte Massen je Detektor
let collStore = {ATLAS:0,  CMS:0,  ALICE:0,  LHCB:0};    // Kollisionen je Detektor (für Signifikanz)
let lastEvent=null;      // zuletzt gesampeltes physikalisches Event (Display==Histogramm)
let goldenEvent=null;    // eingefrorenes "Golden Event" (Klick aufs Display)
let higgsCands=0;        // Higgs→4ℓ-Kandidaten (Goldkanal, nur E>=4 TeV)
let selDet="ATLAS";
let activePhysicsMode="HIGGS"; // HIGGS|QGP|LHCB|PILOT – Maschinen-Betriebsmodus (entkoppelt vom Detektor-Tab)
let isFastMode=true; // Toggleable speed mode

function getDurations() {
  // Didaktisches Geschwindigkeitsmodell: die visuelle BAHNGESCHWINDIGKEIT (px/ms)
  // steigt MONOTON durch die Beschleunigerkette (LINAC -> PSB -> PS -> SPS -> TI),
  // und der LHC-Ring ist IMMER der schnellste. Nicht maßstabsgetreu, aber physikalisch
  // konsistent: Teilchen werden beschleunigt, niemals in Tunneln "schneller als im LHC".
  // Dauer = Pfadlänge / Geschwindigkeit (Pfadlängen aus der SVG-Geometrie gemessen).
  const V = { linac:0.52, psb:0.75, trPs:0.75, ps:0.93, trSps:0.93, sps:1.12, ti:1.32 };
  const LEN = { linac:94, psb:112*3, trPs:56, ps:238*3, trSps:138, sps:408*2, ti:182 };
  const slow = timeScale();   // "Didaktisch (langsam)" streckt die Zeit gleichmäßig
  const ion  = isIon ? 1.6 : 1.0;        // Ionen: schwerer, niedrigere Injektionsgeschwindigkeit
  const d = (len,v)=>Math.round(len/v*slow*ion);
  return {
    linac:   d(LEN.linac,  V.linac),
    ring1:   d(LEN.psb,    V.psb),
    trToPs:  d(LEN.trPs,   V.trPs),
    ps:      d(LEN.ps,     V.ps),
    trToSps: d(LEN.trSps,  V.trSps),
    sps:     d(LEN.sps,    V.sps),
    ti:      d(LEN.ti,     V.ti),
    autoDelay: isFastMode ? 150 : 600
  };
}

// CCC OPERATOR STATES
let paramEnergy = 6.8;      // Target Energy (TeV)
let paramIntensity = 1.15;  // Bunch Intensity (10^11 protons)
let paramBetaStar = 1.5;    // Beam size at IP (meters)
let paramRampSpeed = 0.05;  // Magnetic field ramp rate (T/s)
let squeezing = false;      // Squeeze in progress
let squeezed = false;       // Squeeze complete
let cryoRecovery = false;   // Cryogenic recovery active
let autoCollInterval = null; // Auto Collide loop

