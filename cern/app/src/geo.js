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
  // Strichstärken in Bildschirm-Pixeln halten — sonst werden Linien beim
  // Injektor-Zoom (~20×) zu fetten Klötzen. (Bei Text ohne Wirkung.)
  el.setAttribute('vector-effect', 'non-scaling-stroke');
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

  // Detektoren an den ECHTEN IP-Positionen (Insertion-Zentroide). geo-far →
  // im Injektor-Zoom ausgeblendet (IP1/ATLAS liegt direkt neben Meyrin und
  // würde sonst ~20× vergrößert das Cluster überdecken).
  for (const name in (GEO.ip || {})) {
    const p = GEO.ip[name], c = DET_COL[name] || '#fff';
    const circ = mk('circle', { cx: p.x, cy: p.y, r: 4, fill: c, stroke: '#0d1117', 'stroke-width': 1 });
    const lab = label(p.x, p.y - 7, name, { fill: c, 'font-size': '8px', 'font-family': 'monospace', 'font-weight': 'bold', 'text-anchor': 'middle' });
    circ.classList.add('geo-far'); lab.classList.add('geo-far');
    g.appendChild(circ); g.appendChild(lab);
  }

  // Beschleuniger-Labels (Zentroide). Klasse geo-far → im Injektor-Zoom
  // ausgeblendet (sonst wären die 7px-PS/PSB-Labels ~20× zu groß); die feinen
  // Ersatz-Labels liefert dort die Detail-Ebene (drawInjector).
  (GEO.accelLabels || []).forEach(p => { const el = label(p.x, p.y, p.t, {
    fill: 'rgba(205,214,228,0.7)', 'font-size': '7px', 'font-family': 'monospace', 'text-anchor': 'middle' });
    el.classList.add('geo-far'); g.appendChild(el); });
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
  drawFCC(g);
}

// ── Easter Egg: Future Circular Collider (FCC) ──────────────────────────────
// Der GEPLANTE ~91-km-Ring, maßstäblich neben den echten Beschleunigern. Real
// FCC-Umfang 90,7 km vs LHC 26,7 km → Radius ×3,4. Der LHC sitzt real intern
// (fast tangential) am SW-Rand des FCC; der FCC dehnt sich nach NE unter den
// Léman. Standard versteckt; eingeblendet via #svg.fcc-on (handlers#revealFCC).
function drawFCC(g) {
  const LHC = { cx: 350, cy: 240, r: 180 };          // = geo_build-Anker (LHC_CX/CY/R)
  const k = 90.7 / 26.7, R = LHC.r * k;              // Umfangsverhältnis ≈ 3,4
  const ne = [0.6, -0.8], off = R - LHC.r - 4;       // NE; LHC innen ~tangential
  const cx = LHC.cx + ne[0] * off, cy = LHC.cy + ne[1] * off;
  const view = padToAspect([[cx - R, cy - R], [cx + R, cy + R], [LHC.cx, LHC.cy]], 700 / 480, 60);
  App.geoFccView = view;
  const FC = 'rgba(210,120,255,';
  const fcc = mk('g'); fcc.setAttribute('class', 'geo-element geo-fcc');
  fcc.appendChild(mk('circle', { cx, cy, r: R, fill: FC + '0.05)', stroke: FC + '0.85)', 'stroke-width': 2, 'stroke-dasharray': '10,7' }));
  const fs = s => (s * view.w / 700).toFixed(1) + 'px';
  const ti = label(cx, cy - R + (24 * view.w / 700), 'FCC — Future Circular Collider (geplant, ~91 km)',
    { fill: FC + '0.95)', 'font-size': fs(16), 'font-family': 'monospace', 'font-weight': 'bold', 'text-anchor': 'middle' });
  fcc.appendChild(ti);
  fcc.appendChild(label(cx, cy - R + (44 * view.w / 700), 'LHC 27 km · SPS 7 km · FCC 91 km   (×3,4)',
    { fill: FC + '0.7)', 'font-size': fs(11), 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(fcc);

  // Versteckter Auslöser: dezenter ✦ im See (FCC verläuft real unter dem Léman).
  if (GEO.lakeLabel) {
    const t = mk('text', { x: GEO.lakeLabel.x + 26, y: GEO.lakeLabel.y + 20, 'font-size': '11px',
      'font-family': 'monospace', fill: FC + '0.45)', 'text-anchor': 'middle' });
    t.textContent = '✦'; t.classList.add('fcc-trigger');
    const tip = document.createElementNS(SVG_NS, 'title'); tip.textContent = '?'; t.appendChild(tip);
    t.addEventListener('click', () => { if (App.revealFCC) App.revealFCC(); });
    g.appendChild(t);
  }
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

// Mittelpunkt + (Hüll-)Radius einer Punktwolke (für Kante-zu-Kante-Anschlüsse).
function bboxC(pts) {
  const xs = pts.map(p => p[0]), ys = pts.map(p => p[1]);
  const x0 = Math.min(...xs), x1 = Math.max(...xs), y0 = Math.min(...ys), y1 = Math.max(...ys);
  return { cx: (x0 + x1) / 2, cy: (y0 + y1) / 2, r: Math.max(x1 - x0, y1 - y0) / 2 || 1 };
}
// Pfad von Rand(A) zu Rand(B) entlang der Verbindungslinie der Mittelpunkte
// (saubere Transferlinie, die NICHT ins Ringinnere sticht).
function edgePath(A, B) {
  const dx = B.cx - A.cx, dy = B.cy - A.cy, d = Math.hypot(dx, dy) || 1, ux = dx / d, uy = dy / d, f = n => n.toFixed(2);
  return `M ${f(A.cx + ux * A.r)},${f(A.cy + uy * A.r)} L ${f(B.cx - ux * B.r)},${f(B.cy - uy * B.r)}`;
}
// Abgerundetes Rechteck (für reale Formen wie LEIR, die kein Kreis sind).
function roundedRectPath(cx, cy, w, h, r) {
  r = Math.min(r, w / 2, h / 2);
  const x = cx - w / 2, y = cy - h / 2, f = n => n.toFixed(2);
  return `M ${f(x + r)},${f(y)} H ${f(x + w - r)} A ${f(r)},${f(r)} 0 0 1 ${f(x + w)},${f(y + r)}`
       + ` V ${f(y + h - r)} A ${f(r)},${f(r)} 0 0 1 ${f(x + w - r)},${f(y + h)} H ${f(x + r)}`
       + ` A ${f(r)},${f(r)} 0 0 1 ${f(x)},${f(y + h - r)} V ${f(y + r)} A ${f(r)},${f(r)} 0 0 1 ${f(x + r)},${f(y)} Z`;
}

// Bounding-Box der Punkte (+ Marge) auf ein Ziel-Seitenverhältnis aufpolstern
// (zentriert), damit der gezoomte viewBox unverzerrt das Cluster rahmt.
function padToAspect(pts, aspect, m) {
  let x0 = Math.min(...pts.map(p => p[0])) - m, x1 = Math.max(...pts.map(p => p[0])) + m;
  let y0 = Math.min(...pts.map(p => p[1])) - m, y1 = Math.max(...pts.map(p => p[1])) + m;
  let w = x1 - x0, h = y1 - y0;
  if (w / h < aspect) { const nw = h * aspect; x0 -= (nw - w) / 2; w = nw; }
  else { const nh = w / aspect; y0 -= (nh - h) / 2; h = nh; }
  const r = n => +n.toFixed(1);
  return { x: r(x0), y: r(y0), w: r(w), h: r(h) };
}

function drawInjector(g) {
  const labs = GEO.accelLabels || [];
  const PS = labs.find(l => l.t === 'PS'), PSB = labs.find(l => l.t === 'PSB');
  if (!PS) return;
  const P = '#58a6ff', I = '#e377c2', PSc = '#2ea44f';

  // LINAC 4 — echtes OSM-Gebäude an realer Lage (klein); dünner Strich (non-scaling)
  (GEO.linac4 || []).forEach(d => g.appendChild(path(d, { stroke: P, 'stroke-width': 1, fill: 'rgba(88,166,255,0.14)' })));
  const l4p = ptsOf(GEO.linac4), psPts = ptsOf(GEO.ps), psbPts = ptsOf(GEO.psb);
  // Reale OSM-Ringe → Mittelpunkt + Radius (maßstäblich zueinander): PS, PSB,
  // LINAC4. Anschlüsse werden Kante-zu-Kante entlang der echten Kette gezogen.
  const psC = psPts.length ? bboxC(psPts) : { cx: PS.x, cy: PS.y, r: 4 };
  const psbC = psbPts.length ? bboxC(psbPts) : null;
  const l4C = l4p.length ? bboxC(l4p) : null;

  // MASSSTAB aus echtem OSM-Ring ableiten (gilt uniform für ALLES): PS-Bbox-
  // Radius = real 101 m (PSB bestätigt 25 m) → geo-Einheiten pro Meter.
  const gpm = psC.r / 101, M = m => m * gpm;

  // LEIR & LINAC 3 sind in KEINER Geodatenquelle (OSM/Nominatim/Wikidata) →
  // echte GRÖSSE & FORM, Lage approximiert (∉ OSM → gestrichelt). LEIR = ab-
  // gerundetes Rechteck 24×18 m (Umfang ~77 m ≈ real 78,5 m), S-SW des PS
  // (Ionen-Seite), außerhalb des Rings. LINAC 3 ~30 m, speist LEIR von West.
  const leirW = M(24), leirH = M(18), leirCr = M(4);
  const dir = [-0.29, 0.96];                          // S-SW (−x=West, +y=Süd in geo)
  const dist = psC.r + M(14) + leirW / 2;
  const leirC = { cx: psC.cx + dir[0] * dist, cy: psC.cy + dir[1] * dist, r: leirW / 2 };
  const l3len = M(30), l3y = leirC.cy + M(2);
  const l3b = [leirC.cx - leirW / 2, l3y];            // Eintritt an LEIR-Westkante
  const l3a = [leirC.cx - leirW / 2 - l3len, l3y];    // LINAC3-Anfang (West)

  // Zoom-Zielfenster = NUR der Injektor-Cluster (ohne das riesige SPS — sonst
  // wäre das Cluster nur ein 12px-Fleck), aufs SVG-Seitenverhältnis gepolstert.
  const view = padToAspect(
    psPts.concat(psbPts, l4p,
      [[leirC.cx - leirW / 2, leirC.cy], [leirC.cx + leirW / 2, leirC.cy + leirH / 2], l3a, [psC.cx, psC.cy]]),
    700 / 480, 6);
  App.geoInjectorView = view;

  // Detail-Ebene: erst beim Zoom sichtbar (CSS). Schrift ~ Zoomfaktor → lesbar
  // (≈13px) statt riesig; Linien non-scaling (Bildschirm-px). Reale Kette:
  //   Protonen:  LINAC4 → PSB → PS → (SPS)     Ionen:  LINAC3 → LEIR → PS
  const FS = (13 * view.w / 700).toFixed(2) + 'px';
  const det = mk('g'); det.setAttribute('class', 'geo-element geo-inj-detail');
  const beam = (d, c, dash) => det.appendChild(mk('path', Object.assign(
    { d, fill: 'none', stroke: c, 'stroke-width': 1.1 }, dash ? { 'stroke-dasharray': dash } : {})));

  // Ionen-Kette (LINAC3/LEIR schematisch = gestrichelt): LINAC3 → LEIR → PS
  det.appendChild(mk('path', { d: roundedRectPath(leirC.cx, leirC.cy, leirW, leirH, leirCr), fill: 'none', stroke: I, 'stroke-width': 1.1, 'stroke-dasharray': '3,2' }));
  beam(`M ${l3a[0].toFixed(2)},${l3a[1].toFixed(2)} L ${l3b[0].toFixed(2)},${l3b[1].toFixed(2)}`, I, '3,2');  // LINAC3 → LEIR
  beam(edgePath(leirC, psC), I);                                                                              // LEIR → PS
  // Protonen-Kette (real OSM, durchgezogen): LINAC4 → PSB → PS
  if (psbC) { if (l4C) beam(edgePath(l4C, psbC), P); beam(edgePath(psbC, psC), P); }

  const dl = (x, y, t, c, anc) => det.appendChild(label(x, y, t, { fill: c, 'font-size': FS, 'font-family': 'monospace', 'text-anchor': anc || 'middle', 'font-weight': 'bold' }));
  // Im Zoom sind die groben accelLabels ausgeblendet (geo-far) → hier alle fein.
  dl(psC.cx, psC.cy + psC.r * 0.12, 'PS', PSc, 'middle');
  if (psbC) dl(psbC.cx, psbC.cy - psbC.r - 0.8, 'PSB', P, 'middle');
  if (l4C) dl(l4C.cx - l4C.r - 0.6, l4C.cy + 1.5, 'LINAC4', P, 'end');
  dl(leirC.cx, leirC.cy + leirH / 2 + 1.2, 'LEIR', I, 'middle');
  dl(l3a[0] - 0.6, l3y + 0.4, 'LINAC3', I, 'end');
  g.appendChild(det);

  // Dezenter Dauer-Hinweis im Vollbild (verschwindet beim Zoom): markiert die Lage.
  const hint = mk('g'); hint.setAttribute('class', 'geo-element geo-inj-hint');
  hint.appendChild(mk('circle', { cx: PS.x, cy: PS.y, r: 8, fill: 'none', stroke: 'rgba(46,164,79,0.55)', 'stroke-width': 0.9, 'stroke-dasharray': '2.5,2' }));
  hint.appendChild(label(PS.x - 11, PS.y + 18, '⊕ Injektor-Komplex (Zoom)', { fill: 'rgba(205,214,228,0.72)', 'font-size': '6.5px', 'font-family': 'monospace', 'text-anchor': 'start' }));
  g.appendChild(hint);
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
