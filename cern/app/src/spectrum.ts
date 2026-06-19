// ═══════════════════════════════════════════════════════════════════════════
// MASSENSPEKTRUM — STRAHL-BEWUSST (Detektor × Strahl), ECHTDATEN-GESTÜTZT
// ═══════════════════════════════════════════════════════════════════════════
// Physikalische Soll-Matrix (jeder Detektor zeigt IMMER ein für den AKTUELLEN
// Strahl korrektes Spektrum; die 5σ-„Entdeckung" ist an den physikalisch richtigen
// Strahl gekoppelt):
//
//            p-p (Protonen)                     Pb-Pb (Schwerionen)
//   ATLAS    Z⁰→μμ (echt)                       Z⁰ Standardkerze (echt, EW-blind fürs QGP)
//   CMS      H→ZZ*→4ℓ (Sim)                     Υ-Sequenzunterdrückung (R_AA, modelliert)
//   ALICE    Quarkonia-Referenz (echt, voll)    Quarkonia QGP-unterdrückt (R_AA, modelliert)
//   LHCb     B⁰/CP (Sim, Vorwärts)              spezialisiert (SMOG) — keine Standard-Entdeckung
//
// DATENHERKUNFT (ehrlich): pp/ion/low + topo = ECHTE CMS-Open-Data (Record 545,
// Run2011A DoubleMu, √s = 7 TeV, p-p) inkl. echter μμ-Kinematik & echtem Untergrund-
// Bucket. higgs4l = kalibrierte Simulation. Es gibt KEIN echtes Pb-Pb → QGP-
// Unterdrückung ist ein deklariertes Modell (R_AA) auf den echten p-p-Quarkonia.
// SKALEN: Resonanzmassen sind energieunabhängig (7-TeV-Daten didaktisch für Run 3
// gültig); Produktionsraten sind energieabhängig & didaktisch modelliert.
import { App, $ } from './core.js';
import { CERN_REAL } from './data.gen.js';

const s = App.state, E = App.els, R = CERN_REAL;
const META = R.meta || { sqrt_s_TeV: 7, source: "CMS Open Data" };

// LHCb-B⁰-Pool: kalibrierte Simulation (das CMS-Dimuon-Set enthält keine B-Mesonen).
let _lhcbPool = null;
function lhcbPool() {
 if (_lhcbPool) return _lhcbPool;
 _lhcbPool = []; for (let i = 0; i < 1400; i++) {
  _lhcbPool.push(Math.random() < 0.45
   ? 5.279 + (Math.random() + Math.random() + Math.random() - 1.5) * 0.06   // B⁰ @ 5.279 GeV
   : 4.6 + Math.random() * 1.4);                                            // komb. Untergrund
 }
 return _lhcbPool;
}
// LHCb im Pb-Pb-Lauf: KEIN Standard-B⁰→h⁺h⁻-Kollider-Spektrum. LHCb nimmt Schwerionen
// nur eingeschränkt im Vorwärts-/Fixed-Target-Modus (SMOG, geringe Akzeptanz) auf — der
// saubere B⁰-Peak fehlt, es bleibt nur kombinatorischer Untergrund (didaktische Sim).
// Eigener Pool, damit sich das Pb-Pb-Histogramm sichtbar vom pp-B⁰-Peak unterscheidet.
let _lhcbPoolPbPb = null;
function lhcbPoolPbPb() {
 if (_lhcbPoolPbPb) return _lhcbPoolPbPb;
 _lhcbPoolPbPb = []; for (let i = 0; i < 1400; i++) _lhcbPoolPbPb.push(4.6 + Math.random() * 1.4);  // nur komb. Untergrund
 return _lhcbPoolPbPb;
}

const G = (v, m, sg) => Math.exp(-0.5 * ((v - m) / sg) ** 2);

// ── Resonanz-Bausteine (PDG-Massen). raa=1 (unverdrängt) sofern nicht überschrieben. ──
const Z0   = { key: "Z0",    m: 91.19, hw: 6.0,  sg: 3.0,  thr: 0.9,  amp: 1.00, label: "Z⁰" };
const JPSI = { key: "Jpsi",  m: 3.097, hw: 0.35, sg: 0.10, thr: 0.4,  amp: 0.92, label: "J/ψ" };
const PSI2 = { key: "psi2S", m: 3.686, hw: 0.22, sg: 0.09, thr: 0.4,  amp: 0.18, label: "ψ(2S)" };
const U1   = { key: "Ups",   m: 9.46,  hw: 0.40, sg: 0.16, thr: 0.6,  amp: 0.36, label: "Υ(1S)" };
const U2   = { key: "Ups2S", m: 10.02, hw: 0.28, sg: 0.15, thr: 0.6,  amp: 0.15, label: "Υ(2S)" };
const U3   = { key: "Ups3S", m: 10.36, hw: 0.26, sg: 0.15, thr: 0.6,  amp: 0.09, label: "Υ(3S)" };
// Higgs-thr: Raten-Schwelle, historisch geeicht — die Entdeckung 2012 lief bei
// 4 TeV/Strahl (√s = 8 TeV); ab ~3,5 TeV/Strahl ist der Kanal messbar, volle Rate Run 3.
const HIG  = { key: "H",     m: 125.0, hw: 5.0,  sg: 2.8,  thr: 3.5,  amp: 0.62, label: "H(125)" };
// Z4l-hw = 6 (wie Z⁰): die echten Z→4ℓ-Flanken reichen bis ±6 GeV — ein engeres
// Fenster ließe Peak-Flanken als „Kontinuum" durchs Energie-Gating rutschen.
const Z4L  = { key: "Z4l",   m: 91.19, hw: 6.0,  sg: 2.6,  thr: 0.9,  amp: 0.85, label: "Z→4ℓ" };  // echter Z-Peak im 4ℓ-Datensatz
const B0   = { key: "B0",    m: 5.279, hw: 0.18, sg: 0.07, thr: 0.45, amp: 0.75, label: "B⁰" };
const sup = (r, raa) => ({ ...r, raa });   // R_AA<1 = QGP-Unterdrückung (deklariertes Modell)

// ── Die 8 Strahl-Profile (Detektor × Strahl) ────────────────────────────────
// Jedes Profil: pool() (echte Massen), range/bins, channel, bg(v), reson[], primary,
// disco (ist hier eine 5σ-Entdeckung physikalisch möglich?), target (Kandidaten für 5σ),
// title/sub, prov (Datenherkunft), real (was würde man real messen), discoMsg, optional
// supp (QGP-Unterdrückung deklarieren) / note (Sonderfall, z. B. LHCb Pb-Pb).
const DETSPEC = {
 ATLAS: {
  col: "#58a6ff", fc: "rgba(88,166,255,0.38)",
  beams: {
   pp: {
    channel: "2mu", pool: () => R.pp, range: [50, 150], bins: 60,
    bg: v => Math.exp(-(v - 50) / 30) * 0.12, reson: [Z0], primary: "Z0", disco: true, rate: 1.0, target: 300,
    title: "ATLAS · Z⁰→μ⁺μ⁻ (p-p · echte CMS-Daten)",
    sub: "EW-Eichkanal · Z⁰-Resonanz bei 91 GeV",
    prov: "Massen: echte CMS-Open-Data (μ⁺μ⁻) · Spuren & Pile-up: illustrativ",
    real: "Real ~30 Z⁰→μμ pro s bei L=2·10³⁴, ein Präzisions-Eichkanal",
    explain: "Aus je zwei Myonen (μ⁺μ⁻) wird die gemeinsame Masse berechnet; sie häuft sich scharf bei 91 GeV — der Masse des Z-Bosons. Weil dieser Wert extrem genau bekannt ist, eicht man mit dem Z die Energiemessung der Detektoren. Die Massen stammen aus echten CMS-Daten.",
    discoMsg: "5σ: Z⁰-Resonanz präzise vermessen."
   },
   PbPb: {
    channel: "2mu", pool: () => R.pp, range: [50, 150], bins: 60,
    bg: v => Math.exp(-(v - 50) / 30) * 0.12, reson: [Z0], primary: "Z0", disco: true, rate: 0.6, target: 200,
    title: "ATLAS · Z⁰→μ⁺μ⁻ (Pb-Pb · Standardkerze)",
    sub: "Z⁰ ist elektroschwach und koppelt nicht ans QGP, bleibt also unverändert",
    prov: "Massen: echte CMS-p-p-Z⁰ (in Pb-Pb identisch, EW) · Spuren: illustrativ",
    real: "Z⁰ als QGP-blinde Standardkerze, eicht den Pb-Pb-Lauf",
    explain: "Auch in Blei-Blei-Kollisionen erscheint das Z-Boson bei 91 GeV. Das Besondere: Das Z ist elektroschwach und spürt das heiße Quark-Gluon-Plasma nicht — es durchquert es unverändert. Daher dient es als Standardkerze, an der man prüft, ob die Messung im Schwerionenlauf richtig geeicht ist.",
    discoMsg: "5σ: Z⁰-Standardkerze in Pb-Pb vermessen."
   }
  }
 },
 CMS: {
  col: "#2ea44f", fc: "rgba(46,164,79,0.38)",
  beams: {
   pp: {
    channel: "4l", pool: () => R.higgs4l, range: [80, 200], bins: 60,
    bg: v => Math.exp(-(v - 80) / 46), reson: [HIG, Z4L], primary: "H", disco: true, rate: 0.12, target: 90,
    title: "CMS · H→ZZ*→4ℓ (p-p · goldener Kanal)",
    sub: "Z→4ℓ-Peak (91) + Higgs-Bump (125) auf ZZ*-Untergrund · Higgs-Rate steigt steil mit der Energie",
    prov: "4ℓ-Massen und -Kinematik: echte CMS-Open-Data (Record 5200, 278 Kandidaten 2011/2012)",
    real: "Real nur ~1 H→4ℓ pro Tag; die 278 echten Kandidaten zeigen Z→4ℓ und den Higgs-Bump",
    explain: "Der goldene Kanal (englisch: golden channel) der Higgs-Entdeckung: Das Higgs zerfällt über zwei Z-Bosonen in vier Leptonen. Im Spektrum erkennst du zwei Strukturen — einen Peak bei 91 GeV (ein einzelnes Z, das in vier Leptonen zerfällt) und einen kleinen Hügel bei 125 GeV: das Higgs-Boson. Der Kanal ist sehr selten (real etwa 1 Ereignis pro Tag), aber besonders sauber. Die gezeigten 278 Kandidaten sind echte CMS-Ereignisse von 2011/2012.",
    discoMsg: "5σ: Higgs-Boson entdeckt."
   },
   PbPb: {
    channel: "2mu", pool: () => R.ion, range: [7, 12], bins: 50,
    bg: v => 0.20, reson: [sup(U1, 0.45), sup(U2, 0.12), sup(U3, 0.02)], primary: "Ups", disco: true, rate: 0.5, target: 220,
    title: "CMS · Υ→μ⁺μ⁻ (Pb-Pb · sequentielle Unterdrückung)",
    sub: "Bottomonium-Thermometer: Υ(3S)>Υ(2S)>Υ(1S) zunehmend geschmolzen",
    prov: "Υ-Massen: echte CMS-p-p · Pb-Pb-Unterdrückung modelliert (R_AA)",
    real: "Sequentielle Υ-Unterdrückung misst die QGP-Temperatur (reales CMS-Resultat)",
    explain: "Hier sind die Υ-Mesonen (ein Bottom- und ein Antibottom-Quark) ein Thermometer für das Quark-Gluon-Plasma. Je heißer es ist, desto eher schmelzen locker gebundene Zustände: Υ(3S) verschwindet zuerst, Υ(2S) danach, das fest gebundene Υ(1S) hält am längsten. Aus dieser Reihenfolge liest man die Temperatur ab. Massen echt (CMS), die Plasma-Unterdrückung (R_AA) ist modelliert.",
    discoMsg: "5σ: sequentielle Υ-Unterdrückung (QGP) nachgewiesen.", supp: true
   }
  }
 },
 ALICE: {
  col: "#e377c2", fc: "rgba(227,119,194,0.38)",
  beams: {
   pp: {
    channel: "2mu", pool: () => R.ion, range: [1, 12], bins: 55,
    bg: v => 0.27, reson: [JPSI, PSI2, U1, U2, U3], primary: "Jpsi", disco: true, reference: true, rate: 1.2, target: 450,
    title: "ALICE · J/ψ + Υ → μ⁺μ⁻ (p-p-Referenz · echte CMS-Daten)",
    sub: "Vakuum-Referenz: unverdrängte Quarkonia, keine Entdeckung (QGP nur in Pb-Pb)",
    prov: "Massen: echte CMS-Open-Data (μ⁺μ⁻) · Spuren & Multiplizität: illustrativ",
    real: "Unverdrängte Quarkonia, die p-p-Baseline, gegen die Pb-Pb verglichen wird",
    explain: "Dies ist die Vergleichsbasis ohne Plasma: In Proton-Proton-Kollisionen entstehen Quarkonia (J/ψ bei 3,1 GeV, Υ bei 9,5 GeV) ungestört im Vakuum. Ihre Peaks zeigen die ungestörte Ausbeute. Erst der Vergleich mit dem Blei-Blei-Lauf verrät, welche im Plasma fehlen — deshalb ist dies bewusst keine Entdeckung, sondern der Maßstab.",
    discoMsg: "5σ: Quarkonia-Referenzspektrum (Vakuum) etabliert."
   },
   PbPb: {
    channel: "2mu", pool: () => R.ion, range: [1, 12], bins: 55,
    bg: v => 0.27, reson: [sup(JPSI, 0.60), sup(PSI2, 0.25), sup(U1, 0.45), sup(U2, 0.12), sup(U3, 0.02)],
    primary: "Jpsi", disco: true, rate: 0.85, target: 380,
    title: "ALICE · Quarkonia in Pb-Pb (QGP-Unterdrückung)",
    sub: "R_AA < 1 vs. p-p-Referenz · Schmelzen gebundener Zustände im Quark-Gluon-Plasma",
    prov: "Massen: echte CMS-p-p-Quarkonia · QGP-Unterdrückung modelliert (R_AA)",
    real: "J/ψ und Υ im QGP unterdrückt (R_AA<1), verglichen mit der unverdrängten p-p-Referenz",
    explain: "Im Blei-Blei-Lauf vergleicht man die Quarkonia-Ausbeute mit der Proton-Proton-Referenz. Kleinere Peaks (R_AA < 1) bedeuten: Die gebundenen Quark-Antiquark-Paare wurden im heißen Plasma teilweise aufgelöst. Beim J/ψ kann sich am LHC sogar ein Teil neu bilden (Rekombination). Massen echt (CMS), Unterdrückung modelliert.",
    discoMsg: "5σ: Quarkonia-Unterdrückung (QGP) nachgewiesen.", supp: true
   }
  }
 },
 LHCB: {
  col: "#ff7f0e", fc: "rgba(255,127,14,0.38)",
  beams: {
   pp: {
    channel: "B", pool: () => lhcbPool(), range: [4.6, 6.0], bins: 50,
    bg: v => 0.25, reson: [B0], primary: "B0", disco: true, rate: 0.7, target: 500,
    title: "LHCb · B⁰→h⁺h⁻ (p-p · CP-Verletzung)",
    sub: "Materie-Antimaterie-Asymmetrie im B-Mesonen-Zerfall",
    prov: "B-Masse: kalibrierte Simulation (kein B im Dimuon-Set) · Vertex: illustrativ",
    real: "B⁰→h⁺h⁻: CP-Asymmetrie baut sich über viele Fills auf",
    explain: "LHCb sucht den winzigen Unterschied zwischen Materie und Antimaterie (CP-Verletzung). Dazu vergleicht es, wie oft B⁰-Mesonen (Peak bei 5,28 GeV) in bestimmte Endzustände zerfallen — und wie oft ihre Antiteilchen. Die Asymmetrie baut sich über viele Kollisionen auf. Hinweis: Der B-Peak ist hier kalibrierte Simulation, da der offene CMS-Datensatz keine B-Mesonen enthält.",
    discoMsg: "5σ: CP-Verletzung etabliert."
   },
   PbPb: {
    channel: "B", pool: () => lhcbPoolPbPb(), range: [4.6, 6.0], bins: 50,
    bg: v => 0.25, reson: [], primary: "B0", disco: false, rate: 0.05, target: 600,
    title: "LHCb · spezialisiertes Vorwärtsprogramm (Pb-Pb)",
    sub: "kein Standard-Schwerionen-Collider-Detektor, daher kein sauberes B⁰-Signal",
    prov: "Pb-Pb-Vorwärts/SMOG: kein Standard-B⁰-Kollider-Spektrum (didaktische Simulation)",
    real: "LHCb misst Pb-Pb nur im Vorwärts- oder Fixed-Target-Modus (SMOG): geringe Akzeptanz, kein B⁰→h⁺h⁻-Peak",
    explain: "LHCb ist kein klassischer Rundum-Schwerionendetektor: Im Blei-Blei-Lauf nimmt es nur eingeschränkt teil (Vorwärts-/Fixed-Target-Modus SMOG). Ein sauberer B⁰-Peak entsteht dabei nicht — im Standardkanal bleibt nur Untergrund. Deshalb gibt es in diesem Modus keine Standard-Entdeckung.",
    discoMsg: "", note: "LHCb ist im Pb-Pb-Collider-Lauf nur eingeschränkt aktiv (spezialisiertes Vorwärts-/SMOG-Programm); im Standard-Kanal nur Untergrund."
   }
  }
 }
};

const DETS = ["ATLAS", "CMS", "ALICE", "LHCB"];
const curBeam = () => s.isIon ? "PbPb" : "pp";
// _raw = das Beam-Objekt selbst (Cache-Anker für die Kurven-Kalibrierung, da der
// Spread bei jedem Aufruf ein neues Objekt erzeugt).
function profile(det, beam?) { const d = DETSPEC[det] || DETSPEC.ATLAS; const b = d.beams[beam || curBeam()]; return { col: d.col, fc: d.fc, ...b, _raw: b }; }
function spec() { return profile(s.selDet, curBeam()); }
// Im aktuellen Strahl datennehmende Detektoren — REAL nehmen alle Experimente
// denselben Fill GLEICHZEITIG auf (alle 4 in beiden Strahlen aktiv; LHCb im Pb-Pb
// nur eingeschränkt → trägt nicht zu einer Entdeckung bei, siehe disco:false).
function liveDetectors() { return DETS.slice(); }
App.liveDetectors = liveDetectors;

function primaryReson(sp) { return sp.reson.find(r => r.key === sp.primary) || sp.reson[0]; }

// ── Strahl-Konfiguration → Sichtbarkeit einer Resonanz ──────────────────────
// energyVis: 0 unter der Erzeugungs-Schwelle, weicher Anstieg auf 1 darüber.
// prodVis:  Erzeugbarkeit (nur energieabhängig). drawVis: zusätzlich R_AA (QGP).
//
// GEGATET WIRD AUF DEN ARBEITSPUNKT (paramEnergy), die Energie, mit der DIESER
// Lauf kollidiert — NICHT die Momentan-Energie der Rampe. Gemessen wird nur bei
// Stable Beams (lhcEnergy == paramEnergy); zwischen Füllungen (Strahl-Dump →
// lhcEnergy fällt auf Injektion, Daten bleiben aber erhalten, s. resetLHC(keepData))
// muss die bereits erreichte Signifikanz erhalten bleiben — ein momentaner
// Energie-Bezug würde eine laufende Mehr-Fill-Entdeckung fälschlich auf 0 σ
// zurücksetzen. Ein Pilot-Lauf (Arbeitspunkt 0,45 TeV) zeigt daher korrekt nur
// Untergrund; die „kein Signal vor der Rampe"-Ehrlichkeit liefert der Status-Text
// (leeres Histogramm + „Noch keine Kollisionen"), nicht ein Umschalten der Physik.
function energyVis(thr) { const span = 0.15 * thr + 0.30; return Math.max(0, Math.min(1, (s.paramEnergy - thr) / span)); }
function prodVis(r) { return energyVis(r.thr); }
function drawVis(r) { return prodVis(r) * (r.raa != null ? r.raa : 1); }
function classifyReson(sp, m) { for (const r of sp.reson) { if (Math.abs(m - r.m) <= r.hw) return r; } return null; }

// ── Daten-kalibrierte Modell-Kurve ──────────────────────────────────────────
// Die gezeichnete Kurve wird EINMAL pro Profil aus dem ECHTEN Pool geschätzt:
// Untergrund = Kern-Dichteschätzer (KDE) der Nicht-Resonanz-Events, Peaks =
// Pool-Anteil × normierter Gauß mit empirischer Breite. Vorher kamen bg-Formel
// und amp-Werte von Hand und lagen bis zu 46σ neben den echten Daten (fehlende
// ZZ-Schulter bei ~190 GeV im 4ℓ-Satz, J/ψ-/B⁰-Peaks ~2× zu flach). drawVis
// (Energie-Schwelle × R_AA) skaliert die Peaks weiterhin physikalisch; die
// bg()/amp-Felder in DETSPEC bleiben nur als Fallback für leere Pools.
const SQRT2PI = 2.5066282746310002;
function calib(sp) {
 const key = sp._raw || sp;
 if (key._cal !== undefined) return key._cal;
 const pool = sp.pool(), [mn, mx] = sp.range;
 const inR = pool.filter(m => m >= mn && m < mx);
 const cont = inR.filter(m => !classifyReson(sp, m));
 let cal = null;
 // robuster Streuungs-Schätzer: min(Standardabweichung, IQR/1.349) — ein scharfer
 // Peak über flachem Untergrund bläht die std auf, der IQR bleibt beim Peak.
 const spread = arr => {
  const n = arr.length, mu = arr.reduce((a, b) => a + b, 0) / n;
  const sd = Math.sqrt(arr.reduce((a, b) => a + (b - mu) ** 2, 0) / n);
  const sorted = [...arr].sort((a, b) => a - b);
  const iqr = sorted[Math.floor(n * 0.75)] - sorted[Math.floor(n * 0.25)];
  return Math.min(sd || 1e-9, iqr / 1.349 || sd || 1e-9);
 };
 if (inR.length >= 30 && cont.length >= 10) {
  const n = cont.length;
  const sd = spread(cont) || (mx - mn) / 6;
  // schärfere Bandbreite als Silverman (0.55×): bildet FSR-Schultern/Knicke ab,
  // ohne bei den Pool-Größen (140–1600 Events) zackig zu werden.
  const h = Math.max((mx - mn) / 70, 0.55 * sd * Math.pow(n, -0.2));
  // Rand-Korrektur: Kontinuum-Events KNAPP AUSSERHALB des Sichtfensters schmieren
  // hinein — ohne sie fiele die KDE an den Rändern künstlich ab.
  const contX = pool.filter(m => m >= mn - 3 * h && m < mx + 3 * h && !classifyReson(sp, m));
  const NS = 96, grid = new Float64Array(NS);
  for (let i = 0; i < NS; i++) {
   const v = mn + (i + 0.5) / NS * (mx - mn);
   let y = 0; for (const m of contX) y += G(v, m, h);
   grid[i] = y / (n * h * SQRT2PI);
  }
  const kde = v => {
   const x = (v - mn) / (mx - mn) * NS - 0.5;
   const i = Math.max(0, Math.min(NS - 1, Math.floor(x)));
   const j = Math.min(NS - 1, i + 1), f = Math.min(1, Math.max(0, x - i));
   return grid[i] * (1 - f) + grid[j] * f;
  };
  // Peak-Breite = empirische Streuung ⊕ Bin-Auflösung (quadratisch): ein Peak,
  // der schmaler als ein Histogramm-Bin ist (J/ψ: ~40 MeV vs. 200-MeV-Bins),
  // würde sonst als überhöhte Nadel ÜBER den gebinnten Balken gezeichnet.
  const binw = (mx - mn) / (sp.bins || 60);
  const res = sp.reson.map(r => {
   const ev = inR.filter(m => Math.abs(m - r.m) <= r.hw);
   let sg = r.sg;
   if (ev.length >= 8) sg = Math.max(0.25 * r.sg, Math.hypot(spread(ev), binw / 2.355));
   return { r, P: ev.length / inR.length, sg };
  });
  cal = { kde, Pc: cont.length / inR.length, res };
 }
 key._cal = cal;   // auch null cachen (→ Fallback-Formeln)
 return cal;
}
// w(e) = Gewicht einer Resonanz in der Kurve (drawVis bzw. Nullhypothese-Variante)
function curveVal(sp, v, w) {
 const cal = calib(sp);
 if (cal) {
  let y = cal.Pc * cal.kde(v);
  for (const e of cal.res) y += w(e.r) * e.P * G(v, e.r.m, e.sg) / (e.sg * SQRT2PI);
  return y;
 }
 let y = sp.bg(v);
 for (const r of sp.reson) y += w(r) * r.amp * G(v, r.m, r.sg);
 return y;
}
function fitVal(sp, v) { return curveVal(sp, v, drawVis); }
// Nullhypothese fürs Overlay — der historische Beweis-Mechanismus: Daten gegen
// die Erwartung OHNE den gesuchten Effekt. QGP-Profile → „ohne QGP" (R_AA = 1,
// volle Peaks); sonst → „ohne <primäre Resonanz>" (ihr Beitrag = 0).
function nullVal(sp, v) {
 const prim = primaryReson(sp);
 const w = sp.supp ? (r => prodVis(r)) : (r => r.key === prim.key ? 0 : drawVis(r));
 return curveVal(sp, v, w);
}
function resoName(key) {
 return { Jpsi: "J/psi", psi2S: "psi(2S)", Ups: "Upsilon(1S)", Ups2S: "Upsilon(2S)", Ups3S: "Upsilon(3S)", Z0: "Z0", Z4l: "Z(4l)", B0: "B0" }[key] || key;
}

function classify(m) {
 // ordnet eine reale Masse der nächstgelegenen PDG-Resonanz zu (sonst Untergrund)
 let best = null, bd = 1e9;
 for (const k in R.reso) {
  if (k === "Higgs") continue;                  // anderer Kanal (4ℓ)
  let mm = R.reso[k][0], br = R.reso[k][1];
  let tol = Math.max(0.15, br * 1.5 + 0.035 * mm);
  let d = Math.abs(m - mm);
  if (d < tol && d < bd) { bd = d; best = k; }
 }
 return best;
}

// ── ECHTE Untergrund-Kinematik fürs Event-Display (topo.bg = echte Off-Peak-Paare) ──
let _bgTracks = null;
function bgTracks() {
 if (_bgTracks) return _bgTracks;
 _bgTracks = [];
 const arr = (R.topo && R.topo.bg) || [];
 arr.forEach(t => {
  _bgTracks.push({ pt: t[0], eta: t[1], phi: t[2], q: t[3] });
  _bgTracks.push({ pt: t[4], eta: t[5], phi: t[6], q: t[7] });
 });
 return _bgTracks;
}
// Ein echter Untergrund-Track (für display.js). Fallback nur falls keine bg-Daten.
function sampleBgTrack() {
 const a = bgTracks();
 if (a.length) return a[(Math.random() * a.length) | 0];
 return { pt: 4 + Math.random() * 9, eta: (Math.random() - .5) * 3, phi: Math.random() * 6.283, q: Math.random() < .5 ? 1 : -1 };
}
App.sampleBgTrack = sampleBgTrack;

// ── ECHTE 4-Lepton-Ereignisse (Record 5200): Masse + 4 Lepton-Spuren gepaart ──
// topo.h4l[k] = [pt,eta,phi,q,flavor]×4 (flavor 0=μ,1=e); gehört zu higgs4l[k] (M).
let _h4l = null;
function h4lEvents() {
 if (_h4l) return _h4l;
 const T = (R.topo && R.topo.h4l) || [], M = R.higgs4l || [];
 _h4l = T.map((a, k) => ({ M: M[k],
  leptons: [0, 1, 2, 3].map(i => ({ pt: a[i * 5], eta: a[i * 5 + 1], phi: a[i * 5 + 2], q: a[i * 5 + 3], lep: a[i * 5 + 4] ? "e" : "μ" })) }));
 return _h4l;
}
function sampleH4l() { const e = h4lEvents(); return e.length ? e[(Math.random() * e.length) | 0] : null; }
App.sampleH4l = sampleH4l;

function pickTopo(name) {
 // echte CMS-μμ-Kinematik [pt1,eta1,phi1,q1, pt2,eta2,phi2,q2] je Resonanz;
 // Untergrund (name==null) zieht aus dem ECHTEN bg-Bucket.
 const map = { Z0: "Z0", "J/psi": "Jpsi", "psi(2S)": "psi2S", "Upsilon(1S)": "Ups", "Upsilon(2S)": "Ups", "Upsilon(3S)": "Ups",
               "rho/omega": "low", "phi": "low" };   // Niedrigmasse: echte ρ/ω/φ-Kinematik (topo.low)
 let key = name ? map[name] : "bg";
 let arr = (key && R.topo) ? R.topo[key] : null;
 if (arr && arr.length) {
  let t = arr[(Math.random() * arr.length) | 0];
  return [{ pt: t[0], eta: t[1], phi: t[2], q: t[3], lep: "μ" }, { pt: t[4], eta: t[5], phi: t[6], q: t[7], lep: "μ" }];
 }
 let pt = 5 + Math.random() * 20, a = Math.random() * 6.283;
 return [{ pt: pt, eta: (Math.random() - .5) * 3, phi: a, q: 1, lep: "μ" },
         { pt: pt * (0.6 + Math.random() * 0.6), eta: (Math.random() - .5) * 3, phi: a + Math.PI, q: -1, lep: "μ" }];
}

// Zieht eine Masse aus dem ECHTEN Pool, gewichtet mit Strahl/Energie/R_AA:
//  • Nicht-Resonanz (Kontinuum) → immer akzeptiert (echtes Event).
//  • Resonanz-Event → überlebt mit Wahrscheinlichkeit drawVis (Energie × R_AA);
//    sonst wird VERWORFEN und neu gezogen (Rejection-Sampling). Physik: Die
//    Unterdrückung senkt die PEAK-Ausbeute, das echte Kontinuum bleibt — genau
//    die R_AA-Messung. (Früher wurden unterdrückte Events uniform über den Range
//    verschmiert → unphysikalisches Plateau im Pilot-/Pb-Pb-Spektrum.)
function sampleMass(sp) {
 const pool = sp.pool();
 for (let t = 0; t < 80; t++) {
  const m = pool[(Math.random() * pool.length) | 0];
  const r = classifyReson(sp, m);
  if (!r || Math.random() < drawVis(r)) return m;
 }
 for (let t = 0; t < 200; t++) {   // Extremfall: Pool fast nur (unterdrückte) Resonanz
  const m = pool[(Math.random() * pool.length) | 0];
  if (!classifyReson(sp, m)) return m;
 }
 return sp.range[0] + Math.random() * (sp.range[1] - sp.range[0]);   // letzter Fallback
}

function sampleEvent() {
 const sp = spec();
 if (sp.channel === "4l") {
  // Higgs-Goldkanal: ECHTES 4-Lepton-Ereignis (Masse + 4 reale Lepton-Spuren).
  // Energie-Gating als Rejection über GANZE Events: JEDE Resonanz im Profil
  // (H UND Z→4ℓ) überlebt mit p = drawVis, sonst wird ein neues Event gezogen —
  // Masse und Spur-Topologie bleiben zusammen. (Früher: nur das H-Fenster wurde
  // gegatet, Z→4ℓ lief z. B. im Pilot-Modus ungegatet durch; und das re-gesmearte
  // Event behielt die Leptonen des verworfenen Higgs-Kandidaten.)
  const H = primaryReson(sp);
  if (h4lEvents().length) {
   let ev = sampleH4l(), r = classifyReson(sp, ev.M);
   for (let t = 0; r && Math.random() >= drawVis(r) && t < 80; t++) {
    ev = sampleH4l(); r = classifyReson(sp, ev.M);
   }
   if (r && drawVis(r) <= 0) {   // Sicherung: nie eine nicht-erzeugbare Resonanz zeigen
    const cont = h4lEvents().filter(e => !classifyReson(sp, e.M));
    if (cont.length) { ev = cont[(Math.random() * cont.length) | 0]; r = null; }
   }
   const isSig = !!r && r.key === H.key;
   return { M: ev.M, name: isSig ? "Higgs" : null, channel: "4l", leptons: ev.leptons, signal: isSig };
  }
  // Fallback (keine 4ℓ-Daten geladen): illustrative Topologie; sampleMass gated
  // bereits alle Resonanzen — Fenster-Treffer unterhalb der Schwelle gibt es nicht.
  let m = sampleMass(sp), leptons = [];
  for (let i = 0; i < 4; i++) leptons.push({ pt: 8 + Math.random() * 40, eta: (Math.random() - .5) * 4, phi: Math.random() * 6.283, q: i % 2 ? 1 : -1, lep: Math.random() < .5 ? "e" : "μ" });
  let isSig = drawVis(H) > 0 && Math.abs(m - H.m) < H.hw;
  return { M: m, name: isSig ? "Higgs" : null, channel: "4l", leptons: leptons, signal: isSig };
 }
 let m = sampleMass(sp);
 // Dimuon (ATLAS/ALICE/CMS-Pb-Pb) bzw. B-Vertex (LHCb) → echte 2-Spur-Topologie
 let r = classifyReson(sp, m);
 let name = r ? resoName(r.key) : null;
 return { M: m, name: name, channel: sp.channel, leptons: pickTopo(name), signal: !!name };
}

function resetSpectrumData() {
 s.massStore = { ATLAS: [], CMS: [], ALICE: [], LHCB: [] };
 s.collStore = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
 s.histAcc = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
 s.histSeen = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
 s.higgsCands = 0;
}

// Histogramm-Eintrag mit Deckel: bis HIST_CAP normal anhängen, danach RESERVOIR-
// SAMPLING (zufälliges Ersetzen mit p = CAP/gesehen) — das Histogramm bleibt eine
// repräsentative Stichprobe ALLER Events statt bei Erreichen des Caps einzufrieren
// (wichtig für Mehr-Fill-Läufe, in denen die Signifikanz weiterwächst).
const HIST_CAP = 6000;
function pushMass(det, m) {
 // Higgs-Fenster-Zähler (120–130 GeV): zählt ALLE akkumulierten 4ℓ-Kandidaten —
 // konsistent zum Histogramm/collStore, nicht nur zufällig angezeigte Display-Events.
 if (det === "CMS" && !s.isIon && Math.abs(m - HIG.m) < HIG.hw) s.higgsCands++;
 const store = s.massStore[det];
 if (!s.histSeen) s.histSeen = { ATLAS: 0, CMS: 0, ALICE: 0, LHCB: 0 };
 const seen = ++s.histSeen[det];
 if (store.length < HIST_CAP) { store.push(m); return; }
 const j = (Math.random() * seen) | 0;
 if (j < HIST_CAP) store[j] = m;
}

// Histogramm EINES Detektors mit 'units' sichtbaren Kandidaten füllen (echte Massen).
// Die Signifikanz-Zählung (collStore) führt die Engine kontinuierlich.
function accumulateStatsFor(det, units) {
 units = Math.floor(units); if (units <= 0) return;
 const sp = profile(det);
 const rateFactor = Math.pow(s.paramIntensity, 2) / Math.max(0.3, s.paramBetaStar);
 const per = Math.max(1, Math.round(rateFactor * (sp.channel === "4l" ? 1.0 : 2.2)));
 for (let k = 0; k < units; k++)
  for (let i = 0; i < per; i++) pushMass(det, sampleMass(sp));
}
App.accumulateStatsFor = accumulateStatsFor;

function generateMassData() {
 // Manueller Einzelschuss: füllt NUR den gewählten Detektor (Inspektions-Werkzeug).
 const sp = spec();
 let rateFactor = Math.pow(s.paramIntensity, 2) / Math.max(0.3, s.paramBetaStar);
 let n = Math.max(1, Math.round(rateFactor * (sp.channel === "4l" ? 1.5 : 5)));
 for (let i = 0; i < n; i++) pushMass(s.selDet, sampleMass(sp));
 s.collStore[s.selDet] += 1;
 s.lastEvent = sampleEvent();
 pushMass(s.selDet, s.lastEvent.M);
 return s.lastEvent;
}

function sigFor(det) {
 const sp = profile(det), n = s.collStore[det];
 if (n <= 0) return 0;
 if (!sp.disco) return 0;                 // in diesem Strahl keine Entdeckung (z. B. LHCb Pb-Pb)
 const pv = prodVis(primaryReson(sp));
 if (pv <= 0) return 0;                    // Energie unter Erzeugungs-Schwelle
 let sig = 5.0 * Math.sqrt(n / sp.target) * pv;
 // REFERENZMESSUNG (z. B. ALICE p-p): misst das Spektrum, ist aber per Definition
 // KEINE Entdeckung → unter 5σ gedeckelt (die Entdeckung braucht den Pb-Pb-Vergleich).
 if (sp.reference) sig = Math.min(sig, 4.6);
 return sig;
}
function getSignificance() { return sigFor(s.selDet); }
App.sigFor = sigFor;

// ── Histogramm + Signifikanz zeichnen ───────────────────────────────────────
function drawHist() {
 const sp = spec();
 const ctxHist = E.ctxHist;
 let w = s.histW, h = s.histH;
 ctxHist.clearRect(0, 0, w, h);
 ctxHist.strokeStyle = "#3a4656"; ctxHist.lineWidth = 1;
 ctxHist.beginPath(); ctxHist.moveTo(30, 10); ctxHist.lineTo(30, h - 16); ctxHist.lineTo(w - 8, h - 16); ctxHist.stroke();
 ctxHist.fillStyle = "#aab8c7"; ctxHist.font = "8px sans-serif";
 let [mn, mx] = sp.range;
 ctxHist.fillText((""+mn).replace(".",",") + " GeV", 30, h - 4); ctxHist.fillText((""+mx).replace(".",",") + " GeV", w - 44, h - 4);

 let sig = getSignificance();
 const prim = primaryReson(sp);
 const specialized = !sp.disco;                       // LHCb im Pb-Pb (spezialisiert)
 const notProd = !specialized && prodVis(prim) <= 0;  // Energie zu gering
 $("lbl-sig").innerText = App.de(sig,2) + " σ";

 // ── Kopf-/Fuß-Texte als HTML AUSSERHALB des Canvas (nicht mehr über die Balken
 //    gemalt → lesbar, hell). drawHist setzt sie bei jedem Neuzeichnen. ──
 const elT = $("sp-title"); if (elT) { elT.textContent = sp.title; elT.style.color = sp.col; }
 const elS = $("sp-sub");   if (elS) elS.textContent = sp.sub;

 let sigBar = $("sig-bar"), sigStatus = $("lbl-sig-status");
 sigBar.style.width = ((specialized || notProd) ? 0 : Math.min(100, (sig / 5.0) * 100)) + "%";
 if (sig === 0) {
  sigStatus.innerText = specialized ? "Spezialisiert · keine Standard-Entdeckung"
   : notProd ? "Inbetriebnahme · " + prim.label + "-Rate zu gering"
   : "Noch keine Kollisionen";
  sigStatus.style.color = "#a3b4c6"; sigBar.style.background = "#3a4656";
 } else if (sp.reference) {
  sigStatus.innerText = "p-p-Referenz (Vakuum) · keine Entdeckung";
  sigStatus.style.color = "#58a6ff"; sigBar.style.background = "#58a6ff";
 } else if (sig < 3.0) {
  sigStatus.innerText = "Rauschen (keine Signifikanz)";
  sigStatus.style.color = "#a3b4c6"; sigBar.style.background = "#58a6ff";
 } else if (sig < 5.0) {
  sigStatus.innerText = "Signal-Hinweis (Evidenz)";
  sigStatus.style.color = "#ff7f0e"; sigBar.style.background = "#ff7f0e";
 } else {
  sigStatus.innerText = sp.discoMsg;
  sigStatus.style.color = "#2ea44f"; sigBar.style.background = "#2ea44f";
 }

 // Detail-Status + „was man real misst" + Datenherkunft → HTML-Fuß (war im Canvas).
 let statusTxt;
 if (specialized)        statusTxt = sp.note;
 else if (notProd)       statusTxt = prim.label + "-Produktionsrate bei " + App.de(s.paramEnergy,2) + " TeV pro Strahl zu gering für eine Messung; wird ab ~" + App.de(prim.thr,1) + " TeV pro Strahl sichtbar (Raten-Modell).";
 else if (sig <= 0)      statusTxt = "Noch keine Kollisionen aufgezeichnet. Bring den Strahl in Stable Beams (Füllen, Ramp, Squeeze) und starte die Datennahme.";
 else if (sp.supp)       statusTxt = "QGP-Unterdrückung (Modell): R_AA Υ(1S) ≈ 0,45, sequenziell · Signifikanz " + App.de(sig,1) + " σ / 5 σ.";
 else if (sp.reference)  statusTxt = "p-p-Referenz: unverdrängte Quarkonia (Vakuum). Die QGP-Unterdrückung (R_AA < 1) erscheint erst im Pb-Pb-Lauf.";
 else                    statusTxt = "Datennahme läuft, Signifikanz " + App.de(sig,1) + " σ von 5,0 σ.";
 const elStat = $("sp-status"); if (elStat) elStat.textContent = statusTxt;
 let realTxt = "→ " + sp.real;
 if (sp.channel === "4l") realTxt += " · Higgs-Fenster (120–130 GeV): " + s.higgsCands + " 4ℓ-Kandidaten";
 const elR = $("sp-real"); if (elR) elR.textContent = realTxt;
 const elP = $("sp-prov"); if (elP) elP.textContent = sp.prov
  + " · Maßstab: Massen aus CMS-Open-Data (√s = 7 TeV, energieunabhängig), Raten modelliert, Kandidaten statt Roh-Kollisionen · Modellkurve aus den Daten kalibriert.";
 // Dynamische Erklär-Box „Dieser Graph": pro Variante neu gesetzt (Akkordeon-Inhalt).
 const elE = $("pi-spExplain"); if (elE) elE.textContent = sp.explain || "";

 const activeData = s.massStore[s.selDet];
 if (!activeData.length) {
  ctxHist.fillStyle = "#aab8c7"; ctxHist.font = "10px monospace";
  ctxHist.fillText("WARTEN AUF KOLLISIONSDATEN…", w / 2 - 92, h / 2);
  return;
 }

 // Histogramm
 let nb = sp.bins, bins = Array(nb).fill(0);
 activeData.forEach(v => { if (v >= mn && v < mx) { let i = Math.floor((v - mn) / (mx - mn) * nb); if (i >= 0 && i < nb) bins[i]++; } });
 let maxB = Math.max(...bins, 1), bw = (w - 40) / nb;
 for (let i = 0; i < nb; i++) {
  let bh = bins[i] / maxB * (h - 30); let x = 30 + i * bw, y = h - 16 - bh;
  ctxHist.fillStyle = sp.fc; ctxHist.fillRect(x, y, bw - 1, bh); ctxHist.fillStyle = sp.col; ctxHist.fillRect(x, y, bw - 1, 1.5);
 }
 // Fehlerbalken (±√N pro Bin) – Poisson
 if (activeData.length > 20) {
  ctxHist.strokeStyle = sp.col; ctxHist.globalAlpha = 0.7; ctxHist.lineWidth = 0.9;
  for (let i = 0; i < nb; i++) {
   if (bins[i] < 3) continue;
   let bh = bins[i] / maxB * (h - 30); let x = 30 + (i + 0.5) * bw, y = h - 16 - bh;
   let err = Math.sqrt(bins[i]) / maxB * (h - 30);
   ctxHist.beginPath(); ctxHist.moveTo(x, y - err); ctxHist.lineTo(x, y + err); ctxHist.stroke();
   ctxHist.beginPath(); ctxHist.moveTo(x - 2, y - err); ctxHist.lineTo(x + 2, y - err); ctxHist.stroke();
   ctxHist.beginPath(); ctxHist.moveTo(x - 2, y + err); ctxHist.lineTo(x + 2, y + err); ctxHist.stroke();
  }
  ctxHist.globalAlpha = 1;
 }
 // Resonanz-Marker (gestrichelt) bei den PDG-Massen; unterdrückte (R_AA<1) bekommen
 // ein „↓"-Zeichen, nicht-erzeugbare (Energie) werden blass.
 { ctxHist.save(); ctxHist.setLineDash([3, 3]); ctxHist.lineWidth = 0.9;
  sp.reson.forEach(r => { if (r.m < mn || r.m > mx) return;
   const xm = 30 + (r.m - mn) / (mx - mn) * (w - 40);
   const on = prodVis(r) > 0, suppd = r.raa != null && r.raa < 1;
   ctxHist.strokeStyle = on ? "rgba(255,255,255,0.30)" : "rgba(255,255,255,0.12)";
   ctxHist.beginPath(); ctxHist.moveTo(xm, h - 16); ctxHist.lineTo(xm, 10); ctxHist.stroke();
   ctxHist.fillStyle = on ? "rgba(255,255,255,0.5)" : "rgba(255,255,255,0.22)";
   ctxHist.font = "6.5px sans-serif";
   ctxHist.fillText(r.label + (suppd ? " ↓" : ""), xm + 2, 16); });
  ctxHist.restore(); }

 // Fit-Kurve (datenkalibriert, s. calib) + NULLHYPOTHESE als gestrichelte
 // Vergleichskurve — der historische Beweis-Mechanismus: erst der Überschuss der
 // Daten über die „ohne Higgs"-Erwartung (bzw. das Defizit unter der „ohne QGP"-
 // Erwartung) macht aus Statistik eine Entdeckung.
 if (sig > 0.5) {
  let alpha = Math.min(1.0, Math.max(0, (sig - 0.5) / 3.5));
  const showNull = sp.disco && !sp.reference;   // nur wo eine Entdeckung erzählt wird
  ctxHist.save(); ctxHist.globalAlpha = alpha;
  let ys = [], ys0 = [], ymax = 1e-9;
  // x-Skala identisch zu Bins/Markern: 30 … 30+(w-40) (sonst ~2 px Versatz rechts)
  for (let xp = 30; xp <= w - 10; xp++) {
   let v = mn + (xp - 30) / (w - 40) * (mx - mn), yv = fitVal(sp, v);
   ys.push(yv); if (yv > ymax) ymax = yv;
   if (showNull) { const y0 = nullVal(sp, v); ys0.push(y0); if (y0 > ymax) ymax = y0; }
  }
  const toY = yv => Math.max(8, Math.min(h - 16, h - 16 - (yv / ymax) * (h - 30)));
  if (showNull) {   // Nullhypothese zuerst (liegt hinter der Modell-Kurve)
   ctxHist.strokeStyle = "rgba(255,255,255,0.60)"; ctxHist.lineWidth = 1.2; ctxHist.setLineDash([5, 4]);
   ctxHist.beginPath();
   ys0.forEach((yv, k) => { const yp = toY(yv); k === 0 ? ctxHist.moveTo(30 + k, yp) : ctxHist.lineTo(30 + k, yp); });
   ctxHist.stroke(); ctxHist.setLineDash([]);
  }
  ctxHist.strokeStyle = sp.col; ctxHist.lineWidth = 1.7; ctxHist.beginPath();
  ys.forEach((yv, k) => { const yp = toY(yv); k === 0 ? ctxHist.moveTo(30 + k, yp) : ctxHist.lineTo(30 + k, yp); });
  ctxHist.stroke();
  if (showNull) {   // Mini-Legende (oben links, kompakt)
   const lbl0 = sp.supp ? "╌ ohne QGP (R_AA = 1)" : "╌ ohne " + prim.label + " (Nullhypothese)";
   ctxHist.font = "6.5px sans-serif";
   ctxHist.fillStyle = sp.col;                       ctxHist.fillText("— Modell (mit Signal)", 34, 13);
   ctxHist.fillStyle = "rgba(255,255,255,0.75)";     ctxHist.fillText(lbl0, 34, 22);
  }
  ctxHist.restore();
 }

}

// Relative Kandidaten-Akkumulationsrate je Detektor im aktuellen Strahl (Higgs
// selten → kleine Rate; Z⁰/Quarkonia häufig). Speist die gleichzeitige Datennahme.
App.detRate = det => (profile(det).rate || 1);
// Kurven-Auswertung für Tests/Audit (χ²-Formvergleich Daten ↔ gezeichnete Kurve).
App.fitValFor = (det, v) => fitVal(profile(det), v);
App.nullValFor = (det, v) => nullVal(profile(det), v);
App.profileMeta = () => META;
App.classify = classify;
App.sampleEvent = sampleEvent;
App.resetSpectrumData = resetSpectrumData;
App.generateMassData = generateMassData;
App.getSignificance = getSignificance;
App.drawHist = drawHist;
