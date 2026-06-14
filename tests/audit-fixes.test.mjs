// Regressionstests für das Backend-Audit (Logik/Physik/Effizienz):
//   A1  Resonanzbreiten = echte natürliche Breiten (keV-Bereich, nicht ×1000)
//   A7  kein „Higgs"-Label unterhalb der Produktions-Schwelle (Pilot-Leck)
//   C4  Reservoir-Sampling hält das Histogramm am HIST_CAP repräsentativ
//   B1  Generationen-Token: Reset + sofortiger Neustart zählt alte Batches nicht
//   B2  Beam-Dump gated manuelle Kollisionen/Neustart bis zum Reset
//   B3  Datennahme-Pause verjüngt den Strahl nicht (Burn-off-Uhr bleibt)
// B1–B3 booten die ECHTEN src-Module (main.js) gegen shell.html in jsdom —
// dieselben Stubs wie tests/helpers/boot-app.mjs, aber mit Zugriff auf App.
import { describe, it, expect, beforeAll } from 'vitest';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, resolve } from 'node:path';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');

function stubContext() {
  const p = new Proxy(function () { return p; }, { get: () => p, apply: () => p, set: () => true });
  return p;
}

let App, CERN_REAL, s;

beforeAll(async () => {
  const markup = readFileSync(resolve(ROOT, 'cern/app/shell.html'), 'utf8')
    .replace('{{STYLES}}', '').replace('{{SCRIPT}}', '');
  document.body.innerHTML = markup;
  if (!Object.getOwnPropertyDescriptor(window.HTMLElement.prototype, 'innerText')) {
    Object.defineProperty(window.HTMLElement.prototype, 'innerText', {
      get() { return this.textContent; },
      set(v) { this.textContent = v; },
      configurable: true,
    });
  }
  globalThis.requestAnimationFrame = () => 0;           // Animationen laufen nie an
  globalThis.cancelAnimationFrame = () => {};
  window.requestAnimationFrame = globalThis.requestAnimationFrame;
  window.cancelAnimationFrame = globalThis.cancelAnimationFrame;
  if (!window.devicePixelRatio) window.devicePixelRatio = 1;
  HTMLCanvasElement.prototype.getContext = () => stubContext();
  const svgProto = window.SVGElement && window.SVGElement.prototype;
  if (svgProto) { svgProto.getTotalLength = () => 100; svgProto.getPointAtLength = () => ({ x: 0, y: 0 }); }

  ({ App } = await import('../cern/app/src/core.js'));
  ({ CERN_REAL } = await import('../cern/app/src/data.gen.js'));
  await import('../cern/app/src/main.js');              // bootet (DOM steht bereits)
  s = App.state;
  expect(document.getElementById('cern-v4').__cernBooted).toBe(true);
});

describe('A1: Resonanzbreiten sind echte natürliche Breiten (PDG)', () => {
  it('Quarkonia-Breiten liegen im keV-Bereich (< 1 MeV), nicht ×1000 zu groß', () => {
    expect(CERN_REAL.reso['J/psi'][1]).toBeLessThan(1e-3);     // 92,6 keV
    expect(CERN_REAL.reso['J/psi'][1]).toBeGreaterThan(1e-5);
    expect(CERN_REAL.reso['Upsilon'][1]).toBeLessThan(1e-3);   // 54 keV
  });
  it('Z⁰ bleibt zu Recht breit (Γ ≈ 2,495 GeV) — der didaktische Kontrast', () => {
    expect(CERN_REAL.reso['Z0'][1]).toBeCloseTo(2.495, 2);
  });
  it('Klassifikation trifft die PDG-Fenster weiterhin', () => {
    expect(App.classify(3.097)).toBe('J/psi');
    expect(App.classify(91.19)).toBe('Z0');
  });
});

describe('A7: kein „Higgs" unterhalb der Produktions-Schwelle (Pilot-Leck)', () => {
  it('sampleEvent (CMS·pp·0.45 TeV) liefert nie name="Higgs" und zählt keine Kandidaten', () => {
    App.resetSpectrumData();
    s.selDet = 'CMS'; s.isIon = false; s.paramEnergy = 0.45;
    for (let i = 0; i < 300; i++) {
      const ev = App.sampleEvent();
      expect(ev.name).not.toBe('Higgs');
      expect(ev.signal).toBe(false);
    }
    expect(s.higgsCands).toBe(0);
    s.paramEnergy = 6.8;
  });
  it('bei voller Energie erscheinen wieder Higgs-Kandidaten', () => {
    App.resetSpectrumData();
    s.selDet = 'CMS'; s.isIon = false; s.paramEnergy = 6.8;
    let hit = 0;
    for (let i = 0; i < 400 && !hit; i++) if (App.sampleEvent().name === 'Higgs') hit++;
    expect(hit).toBeGreaterThan(0);
  });
});

describe('C4: Reservoir-Sampling am Histogramm-Cap', () => {
  it('Länge bleibt exakt am Cap, gesehene Events zählen weiter', () => {
    App.resetSpectrumData();
    s.selDet = 'ATLAS'; s.isIon = false; s.paramEnergy = 6.8;
    s.paramIntensity = 1.0; s.paramBetaStar = 1.0;
    s.massStore.ATLAS = Array(6000).fill(91.2);          // Cap simuliert erreicht
    s.histSeen.ATLAS = 6000;
    App.accumulateStatsFor('ATLAS', 10);                 // per=round(2.2)=2 → 20 neue Events
    expect(s.massStore.ATLAS.length).toBe(6000);         // friert NICHT weiter auf, wächst nicht
    expect(s.histSeen.ATLAS).toBe(6020);                 // Reservoir zählt alle gesehenen
  });
  it('echte ρ/ω/φ-Kinematik ist als topo.low vorhanden (pickTopo-Mapping)', () => {
    expect(CERN_REAL.topo.low.length).toBeGreaterThan(0);
  });
});

describe('B1: Generationen-Token gegen Zombie-Batches', () => {
  it('resetLHC erhöht die Füll-Generation', () => {
    const g0 = s.fillGen;
    App.resetLHC();
    expect(s.fillGen).toBe(g0 + 1);
  });
  it('injectTrain einer ALTEN Generation kehrt sofort folgenlos zurück', async () => {
    App.resetLHC();
    const stale = s.fillGen - 1;          // Generation vor dem Reset
    s.resetFlag = false;                  // neuer Lauf hat das Flag bereits gelöscht
    const before = s.b1Batches;
    await App.injectTrain(1, 2, stale);   // darf weder Dots erzeugen noch zählen
    expect(document.querySelectorAll('.traveling-dot').length).toBe(0);
    expect(s.b1Batches).toBe(before);
  });
});

describe('B2/B3: Beam-Dump-Gate + Burn-off-Uhr', () => {
  it('während des Dumps bleibt die manuelle Kollision gesperrt', () => {
    App.resetLHC();
    s.ramped = true; s.squeezed = true; s.dumping = true;
    App.stopAutoCollide();
    expect(document.getElementById('btn-coll').classList.contains('off')).toBe(true);
    s.dumping = false;
  });
  it('während des Dumps startet keine neue Datennahme', () => {
    s.ramped = true; s.squeezed = true; s.dumping = true;
    App.toggleAutoCollide();
    expect(s.autoCollInterval).toBe(null);
    s.dumping = false;
  });
  it('Pause/Weiter verjüngt den Strahl NICHT (dtElapsed & N₀ bleiben)', () => {
    s.ramped = true; s.squeezed = true; s.dumping = false; s.cryoRecovery = false;
    s.dtElapsed = 5000; s.intensity0 = 0.77;
    App.toggleAutoCollide();              // Start: darf N₀/Uhr nicht zurücksetzen
    expect(s.autoCollInterval).not.toBe(null);
    expect(s.dtElapsed).toBe(5000);
    expect(s.intensity0).toBe(0.77);
    App.stopAutoCollide();
    expect(s.dtElapsed).toBe(5000);       // Pause lässt die Uhr stehen, löscht sie nicht
    App.resetLHC();                       // erst der Refill setzt sie zurück
    expect(s.dtElapsed).toBe(0);
  });
});
