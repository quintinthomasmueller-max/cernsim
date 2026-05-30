(function(){
const SVG_NS="http://www.w3.org/2000/svg";
const svg=document.getElementById("svg");

// ═══════════════════════════════════════════════════════════════════════════
// GEOMETRY CONFIG — all computed so path endpoints match ring entry/exit pts
// ═══════════════════════════════════════════════════════════════════════════
const R={
 PSB:{cx:142,cy:385,r:18}, LEIR:{cx:142,cy:275,r:18},
 PS:{cx:242,cy:332,r:38}, SPS:{cx:400,cy:148,r:65},
 LHC:{cx:350,cy:240,r:180}
};
// Junction angles (radians, SVG coords: 0=right, positive=CW/downward)
const J={
 PSB_ENTRY: Math.PI,    // from LINAC (left side)
 PSB_EXIT: Math.atan2(R.PS.cy-R.PSB.cy, R.PS.cx-R.PSB.cx),     // toward PS ≈-0.51
 LEIR_ENTRY: Math.PI,
 LEIR_EXIT: Math.atan2(R.PS.cy-R.LEIR.cy, R.PS.cx-R.LEIR.cx),  // toward PS ≈0.51
 PS_FROM_PSB: Math.atan2(R.PSB.cy-R.PS.cy, R.PSB.cx-R.PS.cx),   // from PSB ≈2.63
 PS_FROM_LEIR: Math.atan2(R.LEIR.cy-R.PS.cy, R.LEIR.cx-R.PS.cx),// from LEIR ≈-2.63→3.65
 PS_EXIT: Math.atan2(R.SPS.cy-R.PS.cy, R.SPS.cx-R.PS.cx),       // toward SPS ≈-0.84
 SPS_ENTRY: Math.atan2(R.PS.cy-R.SPS.cy, R.PS.cx-R.SPS.cx),     // from PS ≈2.30
 SPS_TI2: Math.atan2(240-R.SPS.cy, 170-R.SPS.cx),                // toward ALICE ≈2.77
 SPS_TI8: Math.atan2(240-R.SPS.cy, 530-R.SPS.cx),                // toward LHCb ≈0.61
 LHC_ALICE: Math.PI,   // ALICE at 180° (left)
 LHC_LHCB: 0           // LHCb at 0° (right)
};

