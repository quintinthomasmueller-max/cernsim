// ═══════════════════════════════════════════════════════════════════════════
// GEO-OVERLAY / REALE ANSICHT — zeichnet die geo-genaue Karte (#geo-layer) aus
// dem generierten Datensatz geo.gen.js und schaltet zwischen den zwei Modi um.
//
// ZWEI MODI (docs/MIGRATION.md, Anhang „Karten-Geo-Genauigkeit"):
//   • Didaktik-Modus  → #schematic sichtbar (stilisiert, animiert), #geo-layer aus.
//   • Reale Ansicht   → #geo-layer sichtbar (reale Lage UND reale Größen, alles aus
//                       OSM-Geodaten), #schematic aus. Keine Doppelbilder/Overlap.
// Reale Größen: SPS ≈ ¼ LHC, PS/PSB winzig (didaktisch ehrlich). Nord = oben.
// Quelle: © OpenStreetMap-Mitwirkende (ODbL). Ausnahme: die SPS→LHC-Tunnel
// (TI 2/TI 8) sind in OSM nicht vorhanden → echte Endpunkte, gekrümmt approximiert.
// ═══════════════════════════════════════════════════════════════════════════
import { App, SVG_NS } from './core.js';
import { GEO } from './geo.gen.js';

const E = App.els;
const DET_COL = { ATLAS: '#58a6ff', CMS: '#17becf', ALICE: '#e377c2', LHCB: '#ff7f0e' };

function mk(tag, attrs) {
  const el = document.createElementNS(SVG_NS, tag);
  for (const k in attrs) el.setAttribute(k, attrs[k]);
  el.classList.add('geo-element');
  return el;
}
function path(d, attrs) { return mk('path', Object.assign({ d, fill: 'none' }, attrs)); }
function label(x, y, t, attrs) { const el = mk('text', Object.assign({ x, y }, attrs)); el.textContent = t; return el; }

function drawGeo() {
  const g = E.geoLayer;
  if (!g || !GEO) return;
  while (g.firstChild) g.removeChild(g.firstChild);   // idempotent

  // Lac Léman (Wasserfläche)
  GEO.lake.forEach(d => g.appendChild(path(d, {
    fill: 'rgba(88,166,255,0.10)', stroke: 'rgba(88,166,255,0.32)', 'stroke-width': 1 })));
  // CH/FR-Staatsgrenze
  GEO.border.forEach(d => g.appendChild(path(d, {
    stroke: 'rgba(255,255,255,0.26)', 'stroke-width': 1.1, 'stroke-dasharray': '6,5' })));

  // LHC-Ring (echte Form/Lage) — im Real-Modus die Hauptstruktur
  GEO.lhc.forEach(d => g.appendChild(path(d, { stroke: 'rgba(88,166,255,0.85)', 'stroke-width': 2 })));
  // Vorbeschleuniger in ECHTER Größe (SPS ≈ ¼ LHC; PS/PSB winzig)
  (GEO.sps || []).forEach(d => g.appendChild(path(d, { stroke: 'rgba(255,127,14,0.85)', 'stroke-width': 1.8 })));
  (GEO.ps || []).forEach(d => g.appendChild(path(d, { stroke: 'rgba(46,164,79,0.9)', 'stroke-width': 1.5 })));
  (GEO.psb || []).forEach(d => g.appendChild(path(d, { stroke: 'rgba(88,166,255,0.9)', 'stroke-width': 1.5 })));

  // Echte interne Transferlinien TT2/TT10 + TT60 (OSM)
  (GEO.tt || []).forEach(d => g.appendChild(path(d, {
    stroke: 'rgba(46,164,79,0.6)', 'stroke-width': 1.3, 'stroke-dasharray': '4,3' })));
  // TI 2 / TI 8 (echte gekrümmte OSM-Trasse + IP-Anbindung)
  if (GEO.ti) {
    ['ti2', 'ti8'].forEach(k => { if (GEO.ti[k]) g.appendChild(path(GEO.ti[k], {
      stroke: 'rgba(46,164,79,0.8)', 'stroke-width': 1.7, 'stroke-dasharray': '5,4' })); });
  }

  // Detektoren an den ECHTEN IP-Positionen (Insertion-Zentroide)
  for (const name in (GEO.ip || {})) {
    const p = GEO.ip[name], c = DET_COL[name] || '#fff';
    g.appendChild(mk('circle', { cx: p.x, cy: p.y, r: 4, fill: c, stroke: '#0d1117', 'stroke-width': 1 }));
    g.appendChild(label(p.x, p.y - 7, name, { fill: c, 'font-size': '8px', 'font-family': 'monospace', 'font-weight': 'bold', 'text-anchor': 'middle' }));
  }

  // Beschleuniger-Labels (Zentroide)
  (GEO.accelLabels || []).forEach(p => g.appendChild(label(p.x, p.y, p.t, {
    fill: 'rgba(205,214,228,0.7)', 'font-size': '7px', 'font-family': 'monospace', 'text-anchor': 'middle' })));
  // TI-Labels an der Trassen-Mitte (Polylinie M..L..L..)
  if (GEO.ti) ['ti2', 'ti8'].forEach(k => {
    const d = GEO.ti[k]; if (!d) return;
    const cs = d.replace('M ', '').split(' L ').map(s => s.split(',').map(Number));
    const m = cs[Math.floor(cs.length / 2)];
    if (m && m.length === 2) g.appendChild(label(m[0], m[1] - 3, k.toUpperCase().replace('TI', 'TI '), {
      fill: 'rgba(46,164,79,0.9)', 'font-size': '7px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  });

  // POI (projizierte reale Standorte)
  (GEO.poi || []).forEach(p => {
    g.appendChild(mk('circle', { cx: p.x, cy: p.y, r: 2, fill: 'rgba(255,255,255,0.55)' }));
    g.appendChild(label(p.x + (p.a === 'start' ? 5 : 0), p.y - 4, p.t, {
      fill: 'rgba(255,255,255,0.5)', 'font-size': '7px', 'font-family': 'monospace', 'text-anchor': p.a }));
  });

  // Regions-/Gewässer-Labels
  if (GEO.lakeLabel) g.appendChild(label(GEO.lakeLabel.x, GEO.lakeLabel.y, 'LAC LÉMAN', {
    fill: 'rgba(88,166,255,0.6)', 'font-size': '8px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(label(112, 252, 'FRANKREICH (FR)', { fill: 'rgba(255,255,255,0.3)', 'font-size': '8.5px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(label(610, 150, 'SCHWEIZ (CH)', { fill: 'rgba(255,255,255,0.3)', 'font-size': '8.5px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(label(64, 38, 'JURA (FR)', { fill: 'rgba(255,255,255,0.24)', 'font-size': '7px', 'font-family': 'monospace' }));
  g.appendChild(label(6, 474, '© OpenStreetMap-Mitwirkende (ODbL) · Web-Mercator', {
    fill: 'rgba(255,255,255,0.3)', 'font-size': '6px', 'font-family': 'monospace' }));

  drawInset(g);
}

// ── Zoom-Inset: Injektorkomplex Meyrin (Detail) ─────────────────────────────
// LINAC3/4 und LEIR sind in OSM NICHT als Geometrie vorhanden (nur PS/PSB/SPS/
// LHC/TI/TT). Damit man die im Maßstab winzigen Vorbeschleuniger trotzdem sieht,
// zeigt dieses Inset die Injektorkette TOPOLOGISCH (schematisch, klar so betitelt);
// PS/PSB sind real in der Hauptkarte. So bleibt die Hauptkarte rein OSM-basiert.
function ring(g, cx, cy, r, col, w) { g.appendChild(mk('circle', { cx, cy, r, fill: 'none', stroke: col, 'stroke-width': w || 1.5 })); }
function seg(g, x1, y1, x2, y2, col, w, dash) {
  const a = { d: `M ${x1},${y1} L ${x2},${y2}`, fill: 'none', stroke: col, 'stroke-width': w || 1.5 };
  if (dash) a['stroke-dasharray'] = dash;
  g.appendChild(mk('path', a));
}
function drawInset(g) {
  // links neben dem Ring (Frankreich-Seite, kein Detektor) → verdeckt nichts Wichtiges
  const BX = 8, BY = 56, BW = 166, BH = 150;
  const P = '#58a6ff', I = '#e377c2', PSc = '#2ea44f', O = '#ff7f0e';
  g.appendChild(mk('rect', { x: BX, y: BY, width: BW, height: BH, rx: 6, fill: 'rgba(13,17,23,0.85)', stroke: 'rgba(139,148,158,0.5)', 'stroke-width': 1 }));
  g.appendChild(label(BX + 8, BY + 14, 'INJEKTOR-KOMPLEX MEYRIN', { fill: '#c9d1d9', 'font-size': '7.5px', 'font-family': 'monospace', 'font-weight': 'bold' }));
  g.appendChild(label(BX + 8, BY + 24, 'Detail · schematisch (LINAC/LEIR ∉ OSM)', { fill: 'rgba(139,148,158,0.9)', 'font-size': '6px', 'font-family': 'monospace' }));

  const psX = BX + 120, psY = BY + 92;
  ring(g, psX, psY, 20, PSc, 2);                                   // PS (größter Vorbeschleuniger)
  // Proton-Zweig: LINAC4 → PSB → PS
  const psbX = BX + 60, psbY = BY + 60;
  ring(g, psbX, psbY, 8, P, 1.6);
  seg(g, BX + 14, BY + 53, psbX - 7, psbY - 2, P, 1.6);            // LINAC4
  seg(g, psbX + 7, psbY + 4, psX - 16, psY - 12, P, 1.4);          // PSB → PS
  // Ionen-Zweig: LINAC3 → LEIR → PS
  const leirX = BX + 60, leirY = BY + 120;
  ring(g, leirX, leirY, 7, I, 1.6);
  seg(g, BX + 14, BY + 130, leirX - 6, leirY + 2, I, 1.6);         // LINAC3
  seg(g, leirX + 6, leirY - 3, psX - 16, psY + 12, I, 1.4);        // LEIR → PS
  // PS → SPS/LHC (Ausgang)
  const ex = BX + BW - 8;
  seg(g, psX + 20, psY, ex, psY, O, 1.6, '4,3');
  g.appendChild(mk('path', { d: `M ${ex},${psY} l -6,-3 l 0,6 z`, fill: O }));

  const lab = (x, y, t, c, anc) => g.appendChild(label(x, y, t, { fill: c, 'font-size': '7px', 'font-family': 'monospace', 'text-anchor': anc || 'start', 'font-weight': 'bold' }));
  lab(BX + 12, BY + 49, 'LINAC4', P);
  lab(psbX + 11, psbY - 4, 'PSB', P);
  lab(BX + 12, BY + 144, 'LINAC3', I);
  lab(leirX + 10, leirY + 4, 'LEIR', I);
  lab(psX, psY + 3, 'PS', PSc, 'middle');
  lab(ex - 2, psY - 6, 'SPS', O, 'end');
}

// ── Modus-Umschaltung (hart: kein Overlay/Overlap) ──────────────────────────
// (NICHT App.setMode — das ist in engine.js die Teilchenwahl Proton/Ion!)
let _real = false;
function setViewMode(real) {
  _real = !!real;
  if (E.schematic) E.schematic.style.display = _real ? 'none' : '';
  if (E.geoLayer) E.geoLayer.style.display = _real ? '' : 'none';
}
function isRealMode() { return _real; }

App.drawGeo = drawGeo;
App.setViewMode = setViewMode;
App.isRealMode = isRealMode;
