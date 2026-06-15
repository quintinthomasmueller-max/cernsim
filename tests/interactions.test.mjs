// Phase-3-Interaktionen (jsdom, esbuild-Bundle): deckt Buttons, Detektor-Tabs,
// SVG-Hits (Info-Panel + Detektorwahl), Param-Info-Akkordeon und Preset-Anzeigen
// ab — genau die Verdrahtung, die in Jupyter still scheitern kann.
import { describe, it, expect, beforeEach } from 'vitest';
import { bootApp, $ } from './helpers/boot-app.mjs';

// SVG-Elemente haben in jsdom kein .click() → Event dispatchen.
function clickEl(el) {
  el.dispatchEvent(new window.MouseEvent('click', { bubbles: true }));
}

describe('Interaktionen (esbuild-Bundle, jsdom)', () => {
  beforeEach(() => { bootApp(); });

  it('alle vier Detektor-Tabs werden aktiv geschaltet', () => {
    for (const d of ['atlas', 'cms', 'alice', 'lhcb']) {
      $('dt-' + d).click();
      expect($('dt-' + d).classList.contains('act')).toBe(true);
    }
  });

  it('Großansicht-Button togglet den Vollbild-Ring (diagram-full) am Handy', () => {
    const btn = $('btn-diagram-full'), root = $('cern-v4');
    expect(root.classList.contains('diagram-full')).toBe(false);
    btn.click();
    expect(root.classList.contains('diagram-full')).toBe(true);
    expect(btn.textContent).toMatch(/Schließen/);
    btn.click();
    expect(root.classList.contains('diagram-full')).toBe(false);
    expect(btn.textContent).toMatch(/Großansicht/);
  });

  it('Info-Panels haben je Kategorie EINHEITLICHE Stat-Struktur + Quelle', () => {
    const labels = () => [...document.querySelectorAll('#info-stats .cv4-info-stat-l')].map(e => e.textContent);
    // Schicht zuerst (frischer ATLAS-Event-Display → Mitte = Spurdetektor)
    $('cv-ev').dispatchEvent(new window.MouseEvent('click', { bubbles: true, clientX: 114, clientY: 90 }));
    expect(labels()).toEqual(['Aufgabe', 'Prinzip', 'Detektor']);
    expect($('info-src').textContent).toMatch(/^Quelle:/);
    clickEl($('hit-sps'));     // Beschleuniger
    expect(labels()).toEqual(['Umfang', 'Geschwindigkeit', 'In Betrieb seit']);
    clickEl($('hit-lhc'));     // Beschleuniger (früher abweichend: „Temperatur")
    expect(labels()).toEqual(['Umfang', 'Geschwindigkeit', 'In Betrieb seit']);
    clickEl($('hit-atlas'));   // Detektor
    expect(labels()).toEqual(['Maße', 'Schwerpunktsenergie', 'Gewicht']);
    clickEl($('hit-lhcb'));    // Detektor (früher abweichend: „Länge")
    expect(labels()).toEqual(['Maße', 'Schwerpunktsenergie', 'Gewicht']);
    expect($('info-src').textContent).toMatch(/^Quelle:/);
  });

  it('SVG-Detektor-Klick (ATLAS) öffnet Info-Panel + wählt Detektor', () => {
    clickEl($('hit-atlas'));
    expect($('info-panel').classList.contains('visible')).toBe(true);
    expect($('info-title').textContent).toMatch(/ATLAS/);
    expect($('dt-atlas').classList.contains('act')).toBe(true);
    $('info-close').click();
    expect($('info-panel').classList.contains('visible')).toBe(false);
  });

  it('Beschleuniger-Hit (SPS) öffnet das passende Info-Panel', () => {
    clickEl($('hit-sps'));
    expect($('info-panel').classList.contains('visible')).toBe(true);
    expect($('info-title').textContent).toMatch(/Super Proton Synchrotron/);
  });

  it('Param-Info-Akkordeon füllt Text und öffnet genau eine Box', () => {
    const btn = document.querySelector('.cv4-pi-btn[data-pi="prePp"]');
    btn.click();
    const box = $('pi-prePp');
    expect(box.classList.contains('open')).toBe(true);
    expect(box.textContent.length).toBeGreaterThan(20);
    // zweite Box öffnen → erste schließt (nur eine offen)
    document.querySelector('.cv4-pi-btn[data-pi="preQgp"]').click();
    expect($('pi-preQgp').classList.contains('open')).toBe(true);
    expect($('pi-prePp').classList.contains('open')).toBe(false);
  });

  it('Tempo-Toggle wechselt die Beschriftung', () => {
    const b = $('btn-speed-toggle');
    expect(b.textContent).toMatch(/Didaktisch/);
    b.click();
    expect(b.textContent).toMatch(/Zeitraffer/);
    b.click();
    expect(b.textContent).toMatch(/Didaktisch/);
  });

  it('Strahl-Parameter sind Preset-Anzeigen (keine Slider mehr)', () => {
    // Die früheren <input type=range> sind entfernt; nur noch Anzeige-Spans.
    expect($('sli-energy')).toBeNull();
    expect($('sli-rampspeed')).toBeNull();
    expect($('sli-beta')).toBeNull();
    expect($('sli-intensity')).toBeNull();
  });

  it('Preset setzt die Parameter-Anzeigen (β* live unsqueezed, Ramp-Rate)', () => {
    $('btn-pre-pp').click();
    expect($('lbl-energy').textContent).toMatch(/6[.,]8/);
    expect($('lbl-beta').textContent).toMatch(/1[.,]50?\s*m/);      // β* live: 1,50 m vor dem Squeeze
    expect($('lbl-rampspeed').textContent).toMatch(/0[.,]05\s*T\/s/);
  });

  it('Pilot-Preset: 0.45 TeV + keine Signifikanz (Inbetriebnahme)', () => {
    $('btn-pre-pilot').click();
    expect($('lbl-energy').textContent).toMatch(/0[.,]45/);
    expect($('dt-atlas').classList.contains('act')).toBe(true);
    expect($('lbl-sig').textContent).toMatch(/0[.,]00\s*σ/);
  });

  it('Protonen-Physik-Preset (pp, 13.6 TeV) wählt CMS als Default-Tab', () => {
    $('btn-pre-pp').click();
    expect($('lbl-energy').textContent).toMatch(/6[.,]8/);
    expect($('dt-cms').classList.contains('act')).toBe(true);
  });
  it('Nur noch 3 Presets (Higgs+CP zu pp-Physik zusammengeführt)', () => {
    expect(document.querySelectorAll('[id^="btn-pre-"]').length).toBe(3);
    expect($('btn-pre-lhcb')).toBeNull();
  });

  it('Geo-Overlay (generiert) wird beim Boot in #geo-layer gezeichnet', () => {
    const layer = $('geo-layer');
    expect(layer).toBeTruthy();
    expect(layer.childElementCount).toBeGreaterThan(20);       // Pfade + POI + Labels
    expect(layer.querySelectorAll('path').length).toBeGreaterThan(10);
    // alle Kinder tragen .geo-element → reagieren auf den Dim-Toggle
    expect([...layer.children].every(c => c.classList.contains('geo-element'))).toBe(true);
  });

  it('Modus-Umschaltung blendet Schema bzw. Geo-Layer hart um (kein Overlap)', () => {
    // Default Didaktik
    expect($('geo-layer').style.display).toBe('none');
    expect($('schematic').style.display).toBe('');
    $('btn-toggle-geo').click();             // Reale Ansicht
    expect($('geo-layer').style.display).toBe('');
    expect($('schematic').style.display).toBe('none');
    expect($('btn-toggle-geo').textContent).toMatch(/Didaktik/);
  });

  it('Schema-Detektoren sitzen auf den Strahlrohr-Überkreuzungen (Kardinalpunkte)', () => {
    const at = (id) => [+$(id).getAttribute('cx'), +$(id).getAttribute('cy')];
    // Didaktik-Schema: Detektoren = Crossover-Punkte der lhc-pipe1/2 (Geo-Modus nutzt echte IPs separat)
    expect(at('d-atlas')).toEqual([350, 420]);
    expect(at('d-cms')).toEqual([350, 60]);
    expect(at('d-alice')).toEqual([170, 240]);
    expect(at('d-lhcb')).toEqual([530, 240]);
  });

  it('Geo-Overlay enthält reale Vorbeschleuniger + TI-Linien (akkurate Lage)', () => {
    const txt = $('geo-layer').textContent;
    expect(txt).toMatch(/SPS/);            // Vorbeschleuniger-Label
    expect(txt).toMatch(/TI 2/);           // Transferlinie SPS→IP2
    expect(txt).toMatch(/TI 8/);           // Transferlinie SPS→IP8
  });

  it('Reale Ansicht zeigt Detektoren an echten IPs im Geo-Layer', () => {
    const txt = $('geo-layer').textContent;
    // Detektor-Labels im Geo-Layer (an realen IP-Positionen gezeichnet)
    ['ATLAS','CMS','ALICE','LHCB'].forEach(n => expect(txt).toContain(n));
  });

  it('Injektor-Komplex an realer Lage: LINAC3/4 + LEIR + PSB + Hinweis', () => {
    const txt = $('geo-layer').textContent;
    ['LINAC4','LINAC3','LEIR','PSB','Injektor-Komplex'].forEach(n => expect(txt).toContain(n));
  });
  it('Injektor-Detail steckt in .geo-inj-detail (erst beim Zoom sichtbar)', () => {
    expect($('geo-layer').querySelector('.geo-inj-detail')).toBeTruthy();
    expect($('geo-layer').querySelector('.geo-inj-hint')).toBeTruthy();
    // kein separater Inset-Kasten mehr (rect im geo-layer)
    expect($('geo-layer').querySelector('rect')).toBeNull();
  });

  // ── Event-Display: klickbare Schichten + Signaturen-Tour ──────────────────
  it('Klick in die Detektor-Mitte öffnet das Spurdetektor-Info-Panel', () => {
    // jsdom-Fallback-Maße: evW=340, evH=180 → Barrel-Zentrum bei (114, 90)
    $('cv-ev').dispatchEvent(new window.MouseEvent('click', { bubbles: true, clientX: 114, clientY: 90 }));
    expect($('info-panel').classList.contains('visible')).toBe(true);
    expect($('info-title').textContent).toMatch(/Spurdetektor/);
  });

  it('Signaturen-Tour: 6 Schritte mit Erklärtext, sauberes Ende', () => {
    const btn = $('btn-ev-tour'), cap = $('ev-caption');
    btn.click();
    expect(cap.textContent).toMatch(/1\/6/);
    expect(cap.textContent).toMatch(/Myon/);
    for (let i = 0; i < 5; i++) btn.click();
    expect(cap.textContent).toMatch(/6\/6/);
    btn.click();   // letzter Klick beendet die Tour
    expect(btn.textContent).toMatch(/Signaturen-Tour/);
    expect(cap.textContent).not.toMatch(/Schritt/);
  });

  it('Detektorwechsel während der Tour beendet sie (kein Standbild)', () => {
    $('btn-ev-tour').click();
    $('dt-cms').click();                      // selectDetector → drawDetBg → Tour-Ende
    expect($('btn-ev-tour').textContent).toMatch(/Signaturen-Tour/);
  });

  it('„Bild lesen"-Akkordeon enthält das echte Higgs-Event-Vorbild', () => {
    document.querySelector('.cv4-pi-btn[data-pi="evRead"]').click();
    const box = $('pi-evRead');
    expect(box.classList.contains('open')).toBe(true);
    expect(box.querySelector('img.cv4-pi-img')).toBeTruthy();
    expect(box.textContent).toMatch(/Higgs-Kandidaten/);
  });
});
