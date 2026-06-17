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
import { INJ } from './inj.gen.js';
import { SAT, SAT_FCC, SAT_INJ, SAT_FCC_VIEW, SAT_INJ_VIEW, SAT_ATTRIB } from './sat.gen.js';

const E = App.els;
const DET_COL = { ATLAS: '#58a6ff', CMS: '#17becf', ALICE: '#e377c2', LHCB: '#ff7f0e' };

function mk(tag, attrs?) {
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

// Klickbare Hitbox im Real-Modus: oeffnet dasselbe Info-Panel (App.showInfo) wie die
// Schema-Hitboxen. #geo-layer hat pointer-events:none -> die Klasse .geo-hit aktiviert
// sie wieder (CSS regelt zoom-abhaengig an/aus, daher NICHT inline). Detektoren werden
// zusaetzlich als aktiver Detektor gewaehlt (Spektrum/Tabs), aber NICHT gezoomt
// (zoomToDetector wirkt auf die Schema-Ansicht).
// opts.ring -> Ring/Linien-Hitbox (.geo-hit-ring, Hover hebt den STRICH hervor, wie
// .info-hit-ring beim LHC im Schema); sonst gefuellte Hitbox (.geo-hit, Hover-Fill).
// opts.det -> Detektor: zusaetzlich aktiv waehlen.
function hit(el, key, opts?) {
  const o = opts || {};
  el.classList.add(o.ring ? 'geo-hit-ring' : 'geo-hit');
  el.setAttribute('id', 'geohit-' + key);
  el.addEventListener('click', e => {
    e.stopPropagation();
    if (App.showInfo) App.showInfo(key);
    if (o.det && App.selectDetector) App.selectDetector(key);
  });
  return el;
}

function drawGeo() {
  const g = E.geoLayer;
  if (!g || !GEO) return;
  while (g.firstChild) g.removeChild(g.firstChild);   // idempotent

  // Satellitenfotos (Sentinel-2 cloudless, EOX) — drei Kacheln für die drei Zoom-
  // Stufen, je pixelgenau auf das SVG-Fenster ausgerichtet (geo_build.py#svg_window_to_bbox_3857).
  // Bei hoher Opazität (0.9) als dominanter geografischer Hintergrund; die Vektorebene
  // liegt darüber. Wrapper-<g> mit der Sichtbarkeits-Klasse, innen
  // <image opacity="0.9"> → CSS-Überblendung (0↔1) × 0.9 = korrekte Opazität.

  // FCC-Kachel (geo-fcc → versteckt; bei fcc-on sichtbar)
  if (SAT_FCC && SAT_FCC_VIEW) {
    const wrap = document.createElementNS(SVG_NS, 'g');
    wrap.setAttribute('class', 'geo-element geo-fcc');
    const v = SAT_FCC_VIEW;
    const img = document.createElementNS(SVG_NS, 'image');
    img.setAttribute('x', String(v.x)); img.setAttribute('y', String(v.y));
    img.setAttribute('width', String(v.w)); img.setAttribute('height', String(v.h));
    img.setAttribute('opacity', '0.9'); img.setAttribute('preserveAspectRatio', 'none');
    img.setAttribute('href', SAT_FCC);
    wrap.appendChild(img); g.appendChild(wrap);
  }

  // Injektor-Kachel (geo-inj-detail → versteckt; bei inj-zoom sichtbar)
  if (SAT_INJ && SAT_INJ_VIEW) {
    const wrap = document.createElementNS(SVG_NS, 'g');
    wrap.setAttribute('class', 'geo-element geo-inj-detail');
    const v = SAT_INJ_VIEW;
    const img = document.createElementNS(SVG_NS, 'image');
    img.setAttribute('x', String(v.x)); img.setAttribute('y', String(v.y));
    img.setAttribute('width', String(v.w)); img.setAttribute('height', String(v.h));
    img.setAttribute('opacity', '0.9'); img.setAttribute('preserveAspectRatio', 'none');
    img.setAttribute('href', SAT_INJ);
    wrap.appendChild(img); g.appendChild(wrap);
  }

  // Normal-Kachel (0,0–700,480; geo-far → beim Injektor-Zoom ausgeblendet)
  if (SAT) {
    const img = mk('image', { x: 0, y: 0, width: 700, height: 480,
      opacity: 0.9, preserveAspectRatio: 'none' });
    img.setAttribute('href', SAT);
    img.setAttributeNS('http://www.w3.org/1999/xlink', 'xlink:href', SAT);
    img.classList.add('geo-far');
    g.appendChild(img);
  }

  // (Der See-Wasserfläche-Overlay ist entfernt — der Lac Léman ist im 0.9-Satellitenbild
  //  ohnehin sichtbar; ein blaues Füll-Polygon darüber wäre nur Redundanz.)

  // CERN-Gelände (Meyrin, Prévessin) als dezent gefülltes Gebiets-Polygon markieren.
  // Stilisierte ~1-km-Fläche (Achteck) um die beiden CERN-Standort-POIs herum — KEINE
  // vermessene Grenze, sondern ein flächiger Standort-Hinweis bei niedriger Opazität,
  // damit das Satellitenbild durchscheint. geo-far: im Injektor-Zoom ausgeblendet.
  (GEO.poi || []).filter(p => /^CERN /.test(p.t)).forEach(p => {
    const w = 26, h = 22, ch = 8;   // Halbbreite/-höhe + abgeschrägte Ecke (Nord oben, achsen-parallel)
    const d = `M ${p.x - w + ch},${p.y - h} L ${p.x + w - ch},${p.y - h} L ${p.x + w},${p.y - h + ch}`
      + ` L ${p.x + w},${p.y + h - ch} L ${p.x + w - ch},${p.y + h} L ${p.x - w + ch},${p.y + h}`
      + ` L ${p.x - w},${p.y + h - ch} L ${p.x - w},${p.y - h + ch} Z`;
    const poly = path(d, { fill: 'rgba(46,164,79,0.22)', stroke: 'rgba(57,211,83,0.95)', 'stroke-width': 1.4, 'stroke-dasharray': '5,3' });
    poly.classList.add('geo-far'); g.appendChild(poly);
  });

  // CH/FR-Staatsgrenze
  GEO.border.forEach(d => g.appendChild(path(d, {
    stroke: 'rgba(255,255,255,0.26)', 'stroke-width': 1.1, 'stroke-dasharray': '6,5' })));

  // LHC-Ring (echte Form/Lage) — im Real-Modus die Hauptstruktur
  GEO.lhc.forEach(d => g.appendChild(path(d, { stroke: 'rgba(88,166,255,0.85)', 'stroke-width': 2 })));
  g.appendChild(hit(path(GEO.lhc.join(' '), { stroke: 'rgba(88,166,255,0)', 'stroke-width': 16 }), 'LHC', { ring: true }));
  // Vorbeschleuniger in ECHTER Größe (SPS ≈ ¼ LHC; PS/PSB winzig)
  (GEO.sps || []).forEach(d => g.appendChild(path(d, { stroke: 'rgba(255,127,14,0.85)', 'stroke-width': 1.8 })));
  if ((GEO.sps || []).length) g.appendChild(hit(path(GEO.sps.join(' '), { stroke: 'rgba(255,127,14,0)', 'stroke-width': 13 }), 'SPS', { ring: true }));
  // PS & PSB als saubere KREISE — jetzt aus den VERMESSUNGSGENAUEN acc-models-Survey-
  // Ringen (INJ, CCS-Meter → SVG; PS R=100,0 m, PSB R=25,0 m), nicht mehr aus den groben
  // OSM-Polygonen. Die echten Ringe sind kreisrund; Survey-Zentroid+Radius ergibt saubere Kreise.
  const psRing = ptsOf(INJ.ps).length ? bboxC(ptsOf(INJ.ps)) : null;
  const psbRing = ptsOf(INJ.psb).length ? bboxC(ptsOf(INJ.psb)) : null;
  if (psRing) {
    g.appendChild(mk('circle', { cx: psRing.cx, cy: psRing.cy, r: psRing.r, fill: 'none', stroke: 'rgba(46,164,79,0.9)', 'stroke-width': 1.5 }));
    g.appendChild(hit(mk('circle', { cx: psRing.cx, cy: psRing.cy, r: psRing.r, fill: 'none', stroke: 'rgba(46,164,79,0)', 'stroke-width': 12 }), 'PS', { ring: true }));
  }
  if (psbRing) {
    g.appendChild(mk('circle', { cx: psbRing.cx, cy: psbRing.cy, r: psbRing.r, fill: 'none', stroke: 'rgba(88,166,255,0.9)', 'stroke-width': 1.5 }));
    g.appendChild(hit(mk('circle', { cx: psbRing.cx, cy: psbRing.cy, r: Math.max(psbRing.r, 1.5), fill: 'none', stroke: 'rgba(88,166,255,0)', 'stroke-width': 10 }), 'PSB', { ring: true }));
  }

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
    const circ = mk('circle', { cx: p.x, cy: p.y, r: 4, fill: c, stroke: '#0e141d', 'stroke-width': 1 });   // = --screen (Theme)
    const lab = label(p.x, p.y - 7, name, { fill: c, 'font-size': '8px', 'font-family': 'monospace', 'font-weight': 'bold', 'text-anchor': 'middle' });
    const hb = hit(mk('circle', { cx: p.x, cy: p.y, r: 9, fill: 'rgba(0,0,0,0.001)' }), name, { det: true });   // grosszuegige Hitbox
    circ.classList.add('geo-far'); lab.classList.add('geo-far'); hb.classList.add('geo-far');
    g.appendChild(circ); g.appendChild(lab); g.appendChild(hb);
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
  g.appendChild(label(6, 474, '© OpenStreetMap (ODbL)' + (SAT ? ' · ' + SAT_ATTRIB : '') + ' · Web-Mercator', {
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
  const ti = label(cx, cy - R + (24 * view.w / 700), 'FCC, Future Circular Collider (geplant, ~91 km)',
    { fill: FC + '0.95)', 'font-size': fs(16), 'font-family': 'monospace', 'font-weight': 'bold', 'text-anchor': 'middle' });
  fcc.appendChild(ti);
  fcc.appendChild(label(cx, cy - R + (44 * view.w / 700), 'LHC 27 km · SPS 7 km · FCC 91 km   (×3,4)',
    { fill: FC + '0.7)', 'font-size': fs(11), 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(fcc);

  // Versteckter Auslöser: dezenter Punkt im See (FCC verläuft real unter dem Léman).
  if (GEO.lakeLabel) {
    const t = mk('circle', { cx: GEO.lakeLabel.x + 26, cy: GEO.lakeLabel.y + 16, r: 3.4,
      fill: FC + '0.45)' });
    t.classList.add('fcc-trigger');
    const tip = document.createElementNS(SVG_NS, 'title'); tip.textContent = '?'; t.appendChild(tip);
    t.addEventListener('click', () => { if (App.revealFCC) App.revealFCC(); });
    g.appendChild(t);
  }
}

// ── Injektor-Komplex Meyrin: an der REALEN Lage (acc-models-Survey) ───────────
// PS, PSB UND LEIR kommen jetzt aus den vermessungsgenauen CERN-acc-models-Survey-
// Ringen (INJ aus inj.gen.js, MAD-X SURVEY in CCS-Metern → SVG; PS R=100,0 m, PSB
// R=25,0 m, LEIR R=12,0 m). LEIR liegt laut Survey 21 m vom PS-Zentrum, also INNERHALB
// des PS-Rings (frühere LEAR-Halle) — nicht mehr schematisch südlich. LINAC 4 ist real
// (OSM-Gebäude way 80305783), gezeichnet als GERADE Strahllinie vom Gebäude bis an den
// PSB-Ring. LINAC 3 ist NICHT in der geholten Survey → Quelle weiter schematisch (WSW
// von LEIR), aber an die echte LEIR-Lage verankert. Alle Ring-Injektionen laufen
// TANGENTIAL ein (echte Synchrotron-Injektion ist streifend, nicht radial/90°). Die
// Detail-Ebene (.geo-inj-detail) erscheint erst beim Zoom; App.geoInjectorView liefert
// das Zoom-Zielfenster.
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
// Tangenten von Ring `from` an Ring `to`: BEIDE Lösungen als {start,T}, sortiert nach
// Nähe zum radialen Eintritt (Index 0 = natürliche Seite). Synchrotron-Injektion ist
// streifend (tangential), NICHT radial/90°. `from.r=0` ⇒ Punktquelle (z. B. Linac).
function tangentOptions(from, to) {
  const dx = from.cx - to.cx, dy = from.cy - to.cy, d = Math.hypot(dx, dy) || 1;
  const rad = [to.cx + to.r * dx / d, to.cy + to.r * dy / d];
  let opts;
  if (d <= to.r) {
    opts = [{ start: [from.cx - from.r * dx / d, from.cy - from.r * dy / d], T: rad }];
  } else {
    const phi = Math.atan2(dy, dx), beta = Math.acos(Math.min(1, to.r / d));
    opts = [phi + beta, phi - beta].map(a => {
      const T = [to.cx + to.r * Math.cos(a), to.cy + to.r * Math.sin(a)];
      const sx = T[0] - from.cx, sy = T[1] - from.cy, sd = Math.hypot(sx, sy) || 1;
      return { start: [from.cx + from.r * sx / sd, from.cy + from.r * sy / sd], T };
    });
  }
  return opts.sort((p, q) => Math.hypot(p.T[0] - rad[0], p.T[1] - rad[1]) - Math.hypot(q.T[0] - rad[0], q.T[1] - rad[1]));
}
function tangentPath(from, to) { const o = tangentOptions(from, to)[0], f = n => n.toFixed(2); return `M ${f(o.start[0])},${f(o.start[1])} L ${f(o.T[0])},${f(o.T[1])}`; }
// Schneiden sich die Segmente ab und cd? (für den „über Kreuz"-Ein-/Auslauf am PSB).
function segCross(a, b, c, d) {
  const ccw = (p, q, r) => (r[1] - p[1]) * (q[0] - p[0]) - (q[1] - p[1]) * (r[0] - p[0]);
  return ccw(a, c, d) * ccw(b, c, d) < 0 && ccw(a, b, c) * ccw(a, b, d) < 0;
}
// Über-Kreuz-Injektion (PS-Lageplan): Punktquelle `src` → Ring `ring` → Zielring `target`.
// Ein-/Auslauf laufen tangential UND ÜBER KREUZ am Ring (Einlaufkreuz). Von den 2×2
// Tangenten-Kombis die wählen, deren Einlauf- (src→ring) und Auslauf-Linie (ring→target)
// sich schneiden. biasPt = bevorzugter Auslauf-Auftreffpunkt am Zielring (z. B. Inflektor).
function injectCross(src, ring, target, biasPt?) {
  const inO = tangentOptions({ cx: src.cx, cy: src.cy, r: 0 }, ring);
  let outO = tangentOptions(ring, target);
  if (biasPt) outO = outO.slice().sort((a, b) =>
    Math.hypot(a.T[0] - biasPt[0], a.T[1] - biasPt[1]) - Math.hypot(b.T[0] - biasPt[0], b.T[1] - biasPt[1]));
  let best = null;
  for (let i = 0; i < inO.length; i++) for (let j = 0; j < outO.length; j++) {
    if (segCross([src.cx, src.cy], inO[i].T, outO[j].start, outO[j].T)) {
      const s = i + (biasPt ? 3 * j : j);    // mit Bias: Inflektor-Auslaufseite stark bevorzugen
      if (!best || s < best.s) best = { I: inO[i], O: outO[j], s };
    }
  }
  const I0 = best ? best.I : inO[0], O0 = best ? best.O : outO[0], f = n => n.toFixed(2);
  return {
    inj: `M ${f(src.cx)},${f(src.cy)} L ${f(I0.T[0])},${f(I0.T[1])}`,
    ext: `M ${f(O0.start[0])},${f(O0.start[1])} L ${f(O0.T[0])},${f(O0.T[1])}`,
    crossed: !!best,
  };
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
  // Hand-Lageplan (cern/data/injector_drawing.svg) -> inj.gen.js: am PS verankert,
  // 41 Grad gedreht (TT2 auf die echte SPS-Richtung), kategorisiert. Beschleuniger
  // hell/dick, Transfertunnel orange, LEIR lila. Kette real:
  //   Protonen: LINAC4 -> PSB -> PS -> (SPS via TT2)     Ionen: LINAC3 -> LEIR -> PS
  // PS/PSB-Kreise kommen aus dem Vollbild (oben), hier nur die Detail-Ebene (Zoom).
  // TT2 wird NICHT separat gezeichnet: die echte PS->SPS-Trasse liegt schon gruen im
  // Vollbild (geo.gen.js 'tt'); ein rotes inj.gen.js-TT2 waere eine versetzte Dublette.
  const view = INJ.view;
  if (!view) return;
  App.geoInjectorView = view;
  const PSc = '#2ea44f', PSBc = '#58a6ff', LEIRc = '#c678dd', ACC = '#eaeaea', TR = '#e8820e';
  const FS = (13 * view.w / 700).toFixed(2) + 'px';
  const det = mk('g'); det.setAttribute('class', 'geo-element geo-inj-detail');
  const addP = (d, c, sw) => det.appendChild(mk('path', { d, fill: 'none', stroke: c, 'stroke-width': sw }));
  (INJ.leir     || []).forEach(d => addP(d, LEIRc, 1.5));
  (INJ.transfer || []).forEach(d => addP(d, TR, 1.4));
  (INJ.accel    || []).forEach(d => addP(d, ACC, 2.4));   // Linac3/Linac4 zuletzt = obenauf
  const lc = { PS: PSc, Booster: PSBc, LEIR: LEIRc, LINAC3: ACC, LINAC4: ACC };
  (INJ.labels || []).forEach(l => det.appendChild(label(l.x, l.y, l.t,
    { fill: lc[l.t] || '#fff', 'font-size': FS, 'font-family': 'monospace', 'text-anchor': 'middle', 'font-weight': 'bold' })));

  // Hitboxen (Real-Modus, nur im Injektor-Zoom aktiv via CSS): LEIR + die zwei Linacs.
  // PS/PSB liegen als Ring-Hitboxen schon im Vollbild (oben). accel[0]=Linac3, [1]=Linac4.
  const acc = INJ.accel || [];
  if (acc[0]) det.appendChild(hit(mk('path', { d: acc[0], fill: 'none', stroke: 'rgba(234,234,234,0)', 'stroke-width': 8 }), 'LINAC3', { ring: true }));
  if (acc[1]) det.appendChild(hit(mk('path', { d: acc[1], fill: 'none', stroke: 'rgba(234,234,234,0)', 'stroke-width': 8 }), 'LINAC4', { ring: true }));
  const leirP = ptsOf(INJ.leir);
  if (leirP.length) { const c = bboxC(leirP); det.appendChild(hit(mk('circle', { cx: c.cx, cy: c.cy, r: c.r + 0.8, fill: 'rgba(0,0,0,0.001)' }), 'LEIR')); }
  g.appendChild(det);

  // Dezenter Dauer-Hinweis im Vollbild (verschwindet beim Zoom): markiert die Lage.
  const PS = (GEO.accelLabels || []).find(l => l.t === 'PS');
  if (PS) {
    const hint = mk('g'); hint.setAttribute('class', 'geo-element geo-inj-hint');
    hint.appendChild(mk('circle', { cx: PS.x, cy: PS.y, r: 8, fill: 'none', stroke: 'rgba(46,164,79,0.55)', 'stroke-width': 0.9, 'stroke-dasharray': '2.5,2' }));
    hint.appendChild(label(PS.x - 11, PS.y + 18, 'Injektor-Komplex (Zoom)', { fill: 'rgba(205,214,228,0.72)', 'font-size': '6.5px', 'font-family': 'monospace', 'text-anchor': 'start' }));
    g.appendChild(hint);
  }
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
