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

  drawInjector(g);
}

// ── Injektor-Komplex Meyrin: an der REALEN relativen Lage (statt separater Box) ──
// PS/PSB/SPS sind bereits real (OSM) in der Karte; LINAC 4 ebenfalls (echtes OSM-
// Gebäude, way 80305783). LEIR + LINAC 3 sind NICHT in OSM → hier schematisch an
// geographisch-richtiger relativer Position zu PS angedeutet. Im Vollbild nur ein
// dezenter Hinweis-Ring; die Detail-Beschriftung (.geo-inj-detail) erscheint beim
// Zoom (#svg.inj-zoom, gesetzt vom „🔬 Injektor-Komplex"-Button). App.geoInjectorView
// liefert das Zoom-Zielfenster (Cluster + SPS), damit der Button geo-genau hinzoomt.
function ptsOf(paths) {
  const o = []; (paths || []).forEach(d => d.slice(2).split(' L ').forEach(s => { const v = s.split(','); o.push([+v[0], +v[1]]); })); return o;
}
function avg(a, i) { return a.reduce((s, p) => s + p[i], 0) / a.length; }
function drawInjector(g) {
  const labs = GEO.accelLabels || [];
  const PS = labs.find(l => l.t === 'PS'), PSB = labs.find(l => l.t === 'PSB');
  if (!PS) return;
  const P = '#58a6ff', I = '#e377c2', PSc = '#2ea44f';

  // LINAC 4 — echtes OSM-Gebäude an realer Lage (klein)
  (GEO.linac4 || []).forEach(d => g.appendChild(path(d, { stroke: P, 'stroke-width': 1.2, fill: 'rgba(88,166,255,0.14)' })));
  const l4p = ptsOf(GEO.linac4), l4 = l4p.length ? [avg(l4p, 0), avg(l4p, 1)] : [PS.x - 6, PS.y + 4];

  // Detail-Ebene: erst beim Zoom sichtbar (CSS) → kein Gewusel im Vollbild
  const det = mk('g'); det.setAttribute('class', 'geo-element geo-inj-detail');
  const ln = (d, c, w) => det.appendChild(mk('path', { d, fill: 'none', stroke: c, 'stroke-width': w }));
  // LEIR (∉ OSM) schematisch SO von PS; LINAC 3 (∉ OSM) speist von West ein
  const leirX = PS.x + 5.5, leirY = PS.y + 5;
  det.appendChild(mk('circle', { cx: leirX, cy: leirY, r: 2.4, fill: 'none', stroke: I, 'stroke-width': 1.1 }));
  ln(`M ${PS.x - 4.5},${PS.y + 9} L ${leirX - 2.2},${leirY + 0.4}`, I, 1);   // LINAC3 → LEIR
  ln(`M ${leirX},${leirY} L ${PS.x + 1},${PS.y + 1}`, I, 1);                  // LEIR → PS
  if (PSB) { ln(`M ${l4[0]},${l4[1]} L ${PSB.x},${PSB.y}`, P, 1); ln(`M ${PSB.x},${PSB.y} L ${PS.x},${PS.y}`, P, 1); }  // LINAC4→PSB→PS
  // Nur die NICHT in OSM/accelLabels vorhandenen Elemente beschriften (PS/PSB/SPS
  // tragen bereits ihre accelLabels) → keine Doppel-Labels beim Zoom.
  const dl = (x, y, t, c, anc) => det.appendChild(label(x, y, t, { fill: c, 'font-size': '4px', 'font-family': 'monospace', 'text-anchor': anc || 'start', 'font-weight': 'bold' }));
  dl(leirX + 3.5, leirY + 1.5, 'LEIR', I, 'start');         // rechts neben LEIR
  dl(l4[0] - 1.5, l4[1] + 3.5, 'LINAC4', P, 'end');         // links von LINAC4
  dl(PS.x - 2, PS.y + 12, 'LINAC3', I, 'end');              // unten-links
  g.appendChild(det);

  // Dezenter Dauer-Hinweis im Vollbild (verschwindet beim Zoom): markiert die Lage.
  const hint = mk('g'); hint.setAttribute('class', 'geo-element geo-inj-hint');
  hint.appendChild(mk('circle', { cx: PS.x, cy: PS.y, r: 8, fill: 'none', stroke: 'rgba(46,164,79,0.55)', 'stroke-width': 0.9, 'stroke-dasharray': '2.5,2' }));
  hint.appendChild(label(PS.x - 11, PS.y + 18, '⊕ Injektor-Komplex (Zoom)', { fill: 'rgba(205,214,228,0.72)', 'font-size': '6.5px', 'font-family': 'monospace', 'text-anchor': 'start' }));
  g.appendChild(hint);

  // Zoom-Zielfenster = Bounding-Box von Cluster (LINAC4/PSB/PS/LEIR) + SPS + Marge.
  const all = ptsOf(GEO.sps).concat(ptsOf(GEO.ps), ptsOf(GEO.psb), l4p, [[leirX, leirY], [PS.x, PS.y]]);
  const xs = all.map(p => p[0]), ys = all.map(p => p[1]), m = 12;
  const x0 = Math.min(...xs) - m, y0 = Math.min(...ys) - m, x1 = Math.max(...xs) + m, y1 = Math.max(...ys) + m;
  App.geoInjectorView = { x: Math.round(x0), y: Math.round(y0), w: Math.round(x1 - x0), h: Math.round(y1 - y0) };
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
