// ═══════════════════════════════════════════════════════════════════════════
// TYPEN — Pilot der TypeScript-Einführung (Schritt 1, siehe docs/MIGRATION.md).
//
// Ambiente JSDoc-Typen für das Stellwerk-Widget. Werden via jsconfig.json
// (`checkJs`) projektweit sichtbar, OHNE dass eine .js in .ts umbenannt wird —
// reine Additions, Runtime unverändert (esbuild ignoriert .d.ts).
//
// Quelle der Shapes:
//   AppState        ← state.js (Object.assign(App.state, …))
//   SpectrumProfile ← spectrum.js#DETSPEC-Eintrag
//   Resonance       ← spectrum.js#Z0/JPSI/…
//   DetConfig       ← display.js#DETKONFIG-Eintrag
//
// Bewusst lenient: dynamisch registrierte App.*-Funktionen + DOM-Refs bleiben
// `any` (das ist ein späterer Rollout-Schritt, nicht der Pilot). Der Wert liegt
// in den drei getypten Verträgen — Tippfehler/fehlende Felder bei `s.*`, `sp.*`
// und `D.*` fallen jetzt beim `tsc --noEmit`-Gate auf, nicht erst im Browser.
// ═══════════════════════════════════════════════════════════════════════════

type DetKey = 'ATLAS' | 'CMS' | 'ALICE' | 'LHCB';

/** Resonanz-Baustein (PDG-Masse + Form). spectrum.js#Z0/JPSI/U1/… */
interface Resonance {
  key: string;
  label: string;
  m: number;      // Masse (GeV)
  hw: number;     // Halbfenster fürs Energie-Gating (GeV)
  sg: number;     // Gauß-Breite (GeV)
  thr: number;    // Raten-Schwelle (TeV/Strahl)
  amp: number;    // relative Amplitude
  raa?: number;   // R_AA < 1 = QGP-Unterdrückung (deklariertes Modell)
}

/** Strahl-Profil (Detektor × Strahl). spectrum.js#DETSPEC-Eintrag. */
interface SpectrumProfile {
  channel: '2mu' | '4l' | 'B';
  pool: () => number[];           // echte Massen je Fenster (CERN-Open-Data) bzw. Sim-Pool
  range: [number, number];
  bins: number;
  bg: (v: number) => number;      // Untergrund-Fallback (Kurve sonst datenkalibriert)
  reson: Resonance[];
  primary: string;                // Schlüssel der namensgebenden Resonanz
  disco: boolean;                 // ist hier eine 5σ-Entdeckung physikalisch möglich?
  rate: number;                   // Kandidaten-Rate (∝ Kanal-Häufigkeit)
  target: number;                 // Kandidaten für 5σ
  reference?: boolean;            // p-p-Referenzspektrum (unverdrängte Quarkonia)
  supp?: boolean;                 // QGP-Unterdrückung deklarieren
  note?: string;                  // Sonderfall (z. B. LHCb Pb-Pb spezialisiert)
  title?: string;
  sub?: string;
  prov?: string;                  // Datenherkunft (echt vs. Modell)
  real?: string;                  // „was würde man real messen"
  discoMsg?: string;              // 5σ-Meldung
  col?: string;
  fc?: unknown;                   // datenkalibrierte Kurven-Funktion (Cache)
  _raw?: unknown;                 // Roh-Pool-Cache-Anker
}

/** Detektor-Konfiguration. display.js#DETKONFIG-Eintrag. Barrel (ATLAS/CMS/ALICE) und
 *  Forward (LHCb) haben unterschiedliche Felder → die variantenspezifischen sind optional. */
interface DetConfig {
  typ: 'barrel' | 'forward';
  farbe: string;
  rolle: string;
  fakt: string;
  bend?: number;
  realRmu?: number;               // echter Außenradius der Myonlage (m) → Maßstab (barrel)
  realLen?: number;               // Länge (m) (forward)
  lagen?: any[];                  // Zwiebelschalen (barrel)
  stationen?: any[];              // Stations-Platten (forward/LHCb)
  [k: string]: any;               // weitere Detail-Felder (Feld, infoKey, …) — Pilot-lenient
}

/** Alle veränderlichen Querschnittsvariablen. state.js#Object.assign(App.state,…). */
interface AppState {
  isIon: boolean; ramped: boolean; filling: boolean;
  b1Count: number; b2Count: number; b1Batches: number; b2Batches: number;
  collisions: number;
  dtElapsed: number; intensity0: number; intensityNow: number;
  dumping: boolean;
  fillGen: number;
  spsDots: { b1: any[]; b2: any[] }; spsAngle: number; spsRunning: boolean; spsLastT: number | null;
  lhcDots: { b1: any[]; b2: any[] };          // umlaufende Bunch-Dots (Animations-Interna) — Pilot-lenient
  lhcSpeed: number; lhcAngle: number; lhcRunning: boolean; lhcLastT: number | null;
  lhcEnergy: number;
  massStore: Record<DetKey, number[]>;
  collStore: Record<DetKey, number>;
  histAcc: Record<DetKey, number>;
  histSeen: Record<DetKey, number>;
  lastEvent: any; goldenEvent: any; higgsCands: number;   // Event-Shape Pilot-lenient (any)
  selDet: DetKey;
  tourStep: number;
  isFastMode: boolean;
  paramEnergy: number; paramIntensity: number; paramBetaStar: number;
  targetBetaStar: number; paramRampSpeed: number;
  isPilot: boolean;
  squeezing: boolean; squeezed: boolean; cryoRecovery: boolean;
  autoCollInterval: number | null; // setInterval-Handle (Browser/jsdom: number)
  resetFlag: boolean;
  dpr: number; evW: number; evH: number; histW: number; histH: number;
  activeLayerKey?: string | null; // display.js setzt/liest dies (fehlt im state.js-Init)
}

/** Geteilter Namespace. core.js#App. */
interface AppNamespace {
  state: AppState;
  els: Record<string, any>;       // DOM-Refs (bei Boot via main.js#initDom befüllt) — Pilot-lenient
  g: any;                         // SVG-Geometrie (R/J/paths/nodes); `any`, da Object.values()
                                  // sonst unknown[] liefert — echte Geometrie-Typen = späterer Schritt
  timeScale?: () => number;
  [k: string]: any;               // dynamisch registrierte Funktionen (drawHist, setStatus, …)
}

/** Laufzeit-Properties, die die Engine an SVG-Elemente haengt:
 *  __geo = Geo-Zwilling-Punkt (Realansicht), __len/__glen = gecachte Pfadlaengen. */
interface SVGCircleElement { __geo?: any; }
interface SVGGeometryElement { __len?: number; __glen?: number; }
