// ═══════════════════════════════════════════════════════════════════════════
// GEOMETRY — reine Konfiguration (Ringe + Junction-Winkel), keine DOM-Refs.
// Pfad-Endpunkte = Ring-Ein/Austritte (alle berechnet, keine optischen Schätzungen).
// (SVG-Element-Refs wie `svg`, `paths`, `nodes` werden bei Boot in App.g/App.els befüllt.)
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

const R = {
  PSB: { cx: 142, cy: 385, r: 18 }, LEIR: { cx: 142, cy: 275, r: 18 },
  PS: { cx: 242, cy: 332, r: 38 }, SPS: { cx: 345, cy: 350, r: 52 },
  LHC: { cx: 350, cy: 240, r: 180 },
};

// Junction-Winkel (rad, SVG-Koords: 0=rechts, positiv=CW/abwärts)
const J = {
  PSB_ENTRY: Math.PI,                                              // von LINAC (links)
  PSB_EXIT: Math.atan2(R.PS.cy - R.PSB.cy, R.PS.cx - R.PSB.cx),     // → PS ≈-0.51
  LEIR_ENTRY: Math.PI,
  LEIR_EXIT: Math.atan2(R.PS.cy - R.LEIR.cy, R.PS.cx - R.LEIR.cx),  // → PS ≈0.51
  PS_FROM_PSB: Math.atan2(R.PSB.cy - R.PS.cy, R.PSB.cx - R.PS.cx),   // von PSB ≈2.63
  PS_FROM_LEIR: Math.atan2(R.LEIR.cy - R.PS.cy, R.LEIR.cx - R.PS.cx),// von LEIR ≈-2.63→3.65
  PS_EXIT: Math.atan2(R.SPS.cy - R.PS.cy, R.SPS.cx - R.PS.cx),       // → SPS ≈0.17
  SPS_ENTRY: Math.atan2(R.PS.cy - R.SPS.cy, R.PS.cx - R.SPS.cx),     // von PS ≈-2.97
  SPS_TI2: Math.atan2(329.6 - R.SPS.cy, 193.9 - R.SPS.cx),           // → LHC Punkt 2 (unten-links) ≈-3.01
  SPS_TI8: Math.atan2(383.2 - R.SPS.cy, 459.0 - R.SPS.cx),           // → LHC Punkt 8 (unten-rechts) ≈0.28
  LHC_ALICE: Math.PI,   // ALICE bei 180° (links)
  LHC_LHCB: 0,          // LHCb bei 0° (rechts)
};

App.g.R = R;
App.g.J = J;

export { R, J };
