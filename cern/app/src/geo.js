// ═══════════════════════════════════════════════════════════════════════════
// GEO-OVERLAY — zeichnet das geo-genaue Overlay (See/Grenze/LHC-Footprint/POI)
// aus dem generierten Datensatz geo.gen.js in die #geo-layer-Gruppe des SVG.
//
// Wahrheitsanspruch (siehe docs/MIGRATION.md, Anhang „Karten-Geo-Genauigkeit"):
//   Diese EBENE ist geo-ehrlich (reale OSM-Geometrie, Web-Mercator, uniform
//   skaliert, Nord=oben). Die operative Beschleuniger-Kette darüber bleibt
//   bewusst schematisch/nicht maßstabsgetreu. Quelle: © OSM-Mitwirkende (ODbL).
// ═══════════════════════════════════════════════════════════════════════════
import { App, SVG_NS } from './core.js';
import { GEO } from './geo.gen.js';

const E = App.els;

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
  while (g.firstChild) g.removeChild(g.firstChild);   // idempotent (Re-Boot/Resize)

  // Lac Léman (Wasserfläche)
  GEO.lake.forEach(d => g.appendChild(path(d, {
    fill: 'rgba(88,166,255,0.10)', stroke: 'rgba(88,166,255,0.30)', 'stroke-width': 1 })));
  // CH/FR-Staatsgrenze (gestrichelt)
  GEO.border.forEach(d => g.appendChild(path(d, {
    stroke: 'rgba(255,255,255,0.24)', 'stroke-width': 1.1, 'stroke-dasharray': '6,5' })));
  // realer LHC-Footprint (fein gepunktet, zeigt die echte Lage/Form)
  GEO.lhc.forEach(d => g.appendChild(path(d, {
    stroke: 'rgba(88,166,255,0.22)', 'stroke-width': 1, 'stroke-dasharray': '2,3' })));

  // Standort-Marker (projizierte reale Koordinaten)
  (GEO.poi || []).forEach(p => {
    g.appendChild(mk('circle', { cx: p.x, cy: p.y, r: 2, fill: 'rgba(255,255,255,0.55)' }));
    g.appendChild(label(p.x + (p.a === 'start' ? 5 : 0), p.y - 4, p.t, {
      fill: 'rgba(255,255,255,0.45)', 'font-size': '7.5px', 'font-family': 'monospace', 'text-anchor': p.a }));
  });

  // Regions-/Gewässer-Beschriftungen
  if (GEO.lakeLabel) g.appendChild(label(GEO.lakeLabel.x, GEO.lakeLabel.y, 'LAC LÉMAN', {
    fill: 'rgba(88,166,255,0.55)', 'font-size': '8px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(label(110, 150, 'FRANKREICH (FR)', {
    fill: 'rgba(255,255,255,0.26)', 'font-size': '8.5px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(label(610, 150, 'SCHWEIZ (CH)', {
    fill: 'rgba(255,255,255,0.26)', 'font-size': '8.5px', 'font-family': 'monospace', 'text-anchor': 'middle' }));
  g.appendChild(label(64, 38, 'JURA (FR)', {
    fill: 'rgba(255,255,255,0.22)', 'font-size': '7px', 'font-family': 'monospace' }));

  // Attribution (ODbL verlangt Quellenangabe für die OSM-Geometrie)
  g.appendChild(label(6, 474, '© OpenStreetMap-Mitwirkende (ODbL) · Web-Mercator', {
    fill: 'rgba(255,255,255,0.28)', 'font-size': '6px', 'font-family': 'monospace' }));
}

App.drawGeo = drawGeo;
