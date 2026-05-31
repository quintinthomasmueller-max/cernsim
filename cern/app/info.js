// ═══════════════════════════════════════════════════════════════════════════
// INFO PANELS — Wikipedia-Stil Overlay für Beschleuniger & Detektoren
// Einheitliche Stat-Struktur: [Energie/Maße, β-Bereich / Kollisions-E., Gebaut/Gewicht]
// ═══════════════════════════════════════════════════════════════════════════
const INFO_DB = {
 LINAC4: {
  title: 'LINAC 4',
  sub: 'Linearbeschleuniger · Protonen (H⁻ → Stripping)',
  color: '#58a6ff',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#0a1628 0%,#0d2b52 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><defs><marker id="ah" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#58a6ff"/></marker></defs><line x1="18" y1="41" x2="172" y2="41" stroke="#58a6ff" stroke-width="2" marker-end="url(#ah)"/><circle cx="45" cy="41" r="5" fill="rgba(88,166,255,0.3)" stroke="#58a6ff" stroke-width="1.2"/><circle cx="85" cy="41" r="5" fill="rgba(88,166,255,0.3)" stroke="#58a6ff" stroke-width="1.2"/><circle cx="125" cy="41" r="5" fill="rgba(88,166,255,0.3)" stroke="#58a6ff" stroke-width="1.2"/><circle cx="162" cy="41" r="5" fill="rgba(88,166,255,0.3)" stroke="#58a6ff" stroke-width="1.2"/><text x="100" y="68" fill="rgba(88,166,255,0.45)" font-size="8" text-anchor="middle" font-family="monospace">H⁻ → 160 MeV → Stripping</text></svg></div>`,
  stats: [['Länge','86 m'],['β-Bereich','0 → 52 % c'],['Seit','2020']],
  text: 'LINAC4 ist der erste Schritt im Proton-Injektorkomplex. Er beschleunigt H⁻-Ionen (Protonen mit zwei Elektronen) mittels Hochfrequenz-Strukturen auf 160 MeV, entsprechend 52 % der Lichtgeschwindigkeit. Beim Transfer zum PSB entfernt eine Stripperfolie die Elektronen. Seit 2020 ersetzt er LINAC2 und verdoppelt die Strahlintensität für den LHC.'
 },
 LINAC3: {
  title: 'LINAC 3',
  sub: 'Linearbeschleuniger · Blei-Ionen (ECR-Quelle)',
  color: '#e377c2',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#1a0a28 0%,#380d52 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><defs><marker id="ai" markerWidth="6" markerHeight="6" refX="5" refY="3" orient="auto"><path d="M0,0 L6,3 L0,6 Z" fill="#e377c2"/></marker></defs><line x1="18" y1="41" x2="172" y2="41" stroke="#e377c2" stroke-width="2" marker-end="url(#ai)"/><ellipse cx="48" cy="41" rx="7" ry="5" fill="rgba(227,119,194,0.3)" stroke="#e377c2" stroke-width="1.2"/><ellipse cx="95" cy="41" rx="7" ry="5" fill="rgba(227,119,194,0.3)" stroke="#e377c2" stroke-width="1.2"/><ellipse cx="142" cy="41" rx="7" ry="5" fill="rgba(227,119,194,0.3)" stroke="#e377c2" stroke-width="1.2"/><text x="100" y="68" fill="rgba(227,119,194,0.45)" font-size="8" text-anchor="middle" font-family="monospace">Pb²⁹⁺ → 4,2 MeV/u</text></svg></div>`,
  stats: [['Länge','~30 m'],['β-Bereich','0 → 9 % c'],['Seit','1994']],
  text: 'LINAC3 beschleunigt Blei-Ionen (Pb²⁹⁺) aus einer Elektronen-Zyklotron-Resonanz-Quelle (ECR) auf 4,2 MeV pro Nukleon – nur 9 % der Lichtgeschwindigkeit, da Blei-Kerne (A=208) viel schwerer sind als Protonen. Die Ionen werden danach in LEIR gestapelt und durch Elektronenkühlung komprimiert. LINAC3 ist seit 1994 in Betrieb.'
 },
 PSB: {
  title: 'Proton Synchrotron Booster',
  sub: 'Synchrotron · 4 übereinander gestapelte Ringe',
  color: '#58a6ff',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#0a1628 0%,#0d3a5c 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="41" r="30" fill="none" stroke="#58a6ff" stroke-width="1.8" opacity="0.9"/><circle cx="100" cy="41" r="23" fill="none" stroke="#58a6ff" stroke-width="1.4" opacity="0.65"/><circle cx="100" cy="41" r="16" fill="none" stroke="#58a6ff" stroke-width="1" opacity="0.4"/><circle cx="100" cy="41" r="9" fill="none" stroke="#58a6ff" stroke-width="0.8" opacity="0.2"/><text x="100" y="72" fill="rgba(88,166,255,0.4)" font-size="7.5" text-anchor="middle" font-family="monospace">4 Ringe übereinander</text></svg></div>`,
  stats: [['Umfang','4 × 157 m'],['β-Bereich','52 → 95 % c'],['Gebaut','1972']],
  text: 'Der PSB besteht aus vier übereinandergestapelten Synchrotron-Ringen und beschleunigt Protonen von 160 MeV (52 % c) auf 2 GeV (95 % c). Nach dem LHC-Injector-Upgrade (LIU, 2020) liefert er doppelt so hohe Strahlintensitäten. Die vier Ringe erlauben das gleichzeitige Beschleunigen mehrerer Pakete mit unterschiedlichem Timing.'
 },
 LEIR: {
  title: 'Low Energy Ion Ring',
  sub: 'Ionen-Synchrotron · Elektronenkühlung',
  color: '#e377c2',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#1a0a28 0%,#2d1045 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="41" r="28" fill="none" stroke="#e377c2" stroke-width="2.5" opacity="0.9"/><line x1="100" y1="13" x2="100" y2="69" stroke="rgba(23,190,207,0.5)" stroke-width="1.5" stroke-dasharray="3,3"/><text x="100" y="36" fill="#e377c2" font-size="10" text-anchor="middle" font-family="monospace" opacity="0.85">Pb⁸²⁺</text><text x="100" y="72" fill="rgba(227,119,194,0.4)" font-size="7.5" text-anchor="middle" font-family="monospace">Elektronenkühlung</text></svg></div>`,
  stats: [['Umfang','78 m'],['β-Bereich','9 → 37 % c'],['Aus LEAR','2005']],
  text: 'LEIR (Low Energy Ion Ring) wurde 2005 aus dem Antiproton-Ring LEAR umgebaut. Er akkumuliert Blei-Ionen von LINAC3 (9 % c) und kühlt sie per Elektronenkühlung: Ein Elektronenstrahl gleicher Mittelsgeschwindigkeit reduziert die Impulsstreuung dramatisch. Danach werden die Ionen auf 72 MeV/u (37 % c) beschleunigt und an den PS übergeben.'
 },
 PS: {
  title: 'Proton Synchrotron',
  sub: 'Synchrotron · Ältester noch aktiver CERN-Beschleuniger',
  color: '#2ea44f',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#091a0f 0%,#0d3020 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="41" r="32" fill="none" stroke="#2ea44f" stroke-width="2.5" opacity="0.85"/><circle cx="100" cy="41" r="3" fill="#2ea44f" opacity="0.6"/><text x="100" y="37" fill="#2ea44f" font-size="9" text-anchor="middle" font-family="monospace" opacity="0.85">PS</text><text x="100" y="50" fill="#2ea44f" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.5">seit 1959</text><text x="100" y="72" fill="rgba(46,164,79,0.4)" font-size="7.5" text-anchor="middle" font-family="monospace">628 m · 26 GeV</text></svg></div>`,
  stats: [['Umfang','628 m'],['β-Bereich','95 → 99,94 % c'],['Seit','1959']],
  text: 'Das Proton-Synchrotron (PS) ist seit 1959 ununterbrochen in Betrieb. Es beschleunigt Protonen von 2 GeV (95 % c) auf 26 GeV (99,94 % c) – ab hier ist der Geschwindigkeitsgewinn minimal, aber der Energiegewinn enorm (Relativität!). Das PS war früher Europas stärkster Beschleuniger und ist heute unverzichtbares Bindeglied in der LHC-Injektorkette.'
 },
 SPS: {
  title: 'Super Proton Synchrotron',
  sub: 'Synchrotron · Nobelpreis-Beschleuniger (1984)',
  color: '#ff7f0e',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#1a0e00 0%,#3d2200 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="41" r="33" fill="none" stroke="#ff7f0e" stroke-width="2.5" opacity="0.85"/><text x="100" y="37" fill="#ff7f0e" font-size="9" text-anchor="middle" font-family="monospace" opacity="0.85">SPS</text><text x="100" y="50" fill="#ff7f0e" font-size="8" text-anchor="middle" font-family="monospace" opacity="0.5">W/Z 1983</text><text x="100" y="72" fill="rgba(255,127,14,0.4)" font-size="7.5" text-anchor="middle" font-family="monospace">6,9 km · 450 GeV</text></svg></div>`,
  stats: [['Umfang','6,9 km'],['β-Bereich','99,94 → 99,9998 % c'],['Gebaut','1976']],
  text: 'Das SPS (1976) beschleunigt auf 450 GeV – die Geschwindigkeit steigt dabei von 99,94 % auf 99,9998 % c, ein scheinbar kleiner Unterschied mit riesiger Energiewirkung. Berühmt durch die Entdeckung der W- und Z-Bosonen 1983 (Nobelpreis 1984). Als letzter Vorbeschleuniger liefert es beide LHC-Strahlen über TI 2 und TI 8.'
 },
 LHC: {
  title: 'Large Hadron Collider',
  sub: 'Proton-Proton / Pb-Pb Kollider · Leistungsstärkster der Welt',
  color: '#58a6ff',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#050d1a 0%,#0d2040 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><circle cx="100" cy="41" r="30" fill="none" stroke="rgba(88,166,255,0.22)" stroke-width="8"/><circle cx="100" cy="41" r="30" fill="none" stroke="#58a6ff" stroke-width="1.2" stroke-dasharray="4,3"/><circle cx="130" cy="41" r="4" fill="#f85149" opacity="0.9"/><circle cx="70" cy="41" r="4" fill="#f85149" opacity="0.9"/><circle cx="100" cy="71" r="3.5" fill="#f85149" opacity="0.7"/><circle cx="100" cy="11" r="3.5" fill="#f85149" opacity="0.7"/><text x="100" y="44" fill="rgba(88,166,255,0.32)" font-size="8" text-anchor="middle" font-family="monospace">27 km</text></svg></div>`,
  stats: [['Umfang','26 659 m'],['β bei 6,8 TeV','99,99999 % c'],['Temp.','1,9 K']],
  text: 'Im LHC sind Protonen mit 6,8 TeV nur noch 3 m/s langsamer als Licht (99,99999 % c). 1 232 supraleitende Dipolmagnete (8,33 T, NbTi bei 1,9 K) halten die Strahlen auf Kreisbahn. An vier Interaktionspunkten kollidieren Protonenpakete bei √s = 13,6 TeV – mehr Energie als je zuvor erreicht. 2012 führte der LHC zur Entdeckung des Higgs-Bosons.'
 },
 ATLAS: {
  title: 'ATLAS Detektor',
  sub: 'A Toroidal LHC Apparatus · IP1 · Allzweck-Detektor',
  color: '#58a6ff',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#0a1628 0%,#122040 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><line x1="100" y1="4" x2="100" y2="78" stroke="rgba(248,81,73,0.5)" stroke-width="1.5"/><ellipse cx="100" cy="41" rx="58" ry="26" fill="none" stroke="#58a6ff" stroke-width="2" opacity="0.9"/><ellipse cx="100" cy="41" rx="44" ry="18" fill="rgba(88,166,255,0.04)" stroke="#58a6ff" stroke-width="1.5" opacity="0.65"/><ellipse cx="100" cy="41" rx="28" ry="11" fill="rgba(46,164,79,0.04)" stroke="#2ea44f" stroke-width="1.2" opacity="0.65"/><ellipse cx="100" cy="41" rx="14" ry="5.5" fill="rgba(255,127,14,0.04)" stroke="#ff7f0e" stroke-width="1" opacity="0.65"/><text x="100" y="76" fill="rgba(88,166,255,0.35)" font-size="7" text-anchor="middle" font-family="monospace">Toroid · LAr · Tile · Tracker</text></svg></div>`,
  stats: [['Maße','46 × 25 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Gewicht','7 000 t']],
  text: 'ATLAS ist der größte Detektor am LHC. Kollisionen bei bis zu 99,99999 % c erzeugen Teilchenschauer, die alle Schichten durchqueren: Silizium-Pixel-Tracker (ab 5 mm vom Strahl), LAr-Kalorimeter, Tile-Kalorimeter und das Toroid-Magnetsystem (8 Spulen je 25 m). 2012 co-Entdecker des Higgs-Bosons bei mH = 125 GeV.'
 },
 CMS: {
  title: 'CMS Detektor',
  sub: 'Compact Muon Solenoid · IP5 · Allzweck-Detektor',
  color: '#17becf',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#051a1a 0%,#0d3535 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><line x1="100" y1="4" x2="100" y2="78" stroke="rgba(248,81,73,0.5)" stroke-width="1.5"/><ellipse cx="100" cy="41" rx="52" ry="22" fill="none" stroke="#17becf" stroke-width="2.5" opacity="0.9"/><ellipse cx="100" cy="41" rx="38" ry="15" fill="rgba(23,190,207,0.05)" stroke="#17becf" stroke-width="1.5" opacity="0.65"/><ellipse cx="100" cy="41" rx="22" ry="8" fill="rgba(23,190,207,0.05)" stroke="#2ea44f" stroke-width="1.2" opacity="0.65"/><text x="100" y="76" fill="rgba(23,190,207,0.35)" font-size="7" text-anchor="middle" font-family="monospace">3,8 T Solenoid · PbWO₄ · Si-Tracker</text></svg></div>`,
  stats: [['Maße','21 × 15 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Gewicht','14 000 t']],
  text: 'CMS ist mit 14 000 t der schwerste Detektor am LHC. Herzstück ist ein 3,8-Tesla-Solenoid (100 000× stärker als das Erdfeld). Teilchen aus 99,99999 % c schnellen Kollisionen werden durch Silizium-Tracker (200 m², 75 Mio. Pixel) und Bleiwolframat-Kristall-Kalorimeter (ECAL) gemessen. 2012 co-Entdecker des Higgs-Bosons.'
 },
 ALICE: {
  title: 'ALICE Detektor',
  sub: 'A Large Ion Collider Experiment · IP2 · Schwerionen-Physik',
  color: '#e377c2',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#1a0a28 0%,#2d1045 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><line x1="100" y1="4" x2="100" y2="78" stroke="rgba(248,81,73,0.5)" stroke-width="1.5"/><ellipse cx="100" cy="41" rx="55" ry="24" fill="none" stroke="#e377c2" stroke-width="2" opacity="0.9"/><ellipse cx="100" cy="41" rx="40" ry="16" fill="none" stroke="#e377c2" stroke-width="1.3" opacity="0.55"/><ellipse cx="100" cy="41" rx="24" ry="9" fill="none" stroke="#e377c2" stroke-width="1" opacity="0.35"/><text x="100" y="76" fill="rgba(227,119,194,0.35)" font-size="7" text-anchor="middle" font-family="monospace">TPC · ITS2 · TOF · QGP-Detektor</text></svg></div>`,
  stats: [['Maße','26 × 16 m'],['Pb-Pb √s_NN','≤ 5,5 TeV'],['Gewicht','10 000 t']],
  text: 'ALICE untersucht Pb-Pb-Kollisionen, bei denen Pb-Kerne mit ~99,999 % c aufeinanderprallen. Dabei entsteht Quark-Gluon-Plasma (QGP) – der Zustand der Materie microsekunden nach dem Urknall. Die TPC (90 m³) identifiziert tausende Teilchen gleichzeitig; der ITS2-Tracker hat 12,5 Mrd. Pixel auf 10 m² – höchste Pixeldichte am LHC.'
 },
 LHCB: {
  title: 'LHCb Detektor',
  sub: 'LHC beauty Experiment · IP8 · Vorwärtsspektrometer',
  color: '#ff7f0e',
  hdr: `<div style="height:82px;background:linear-gradient(135deg,#1a0e00 0%,#302000 100%);display:flex;align-items:center;justify-content:center"><svg viewBox="0 0 200 82" width="200" height="82" xmlns="http://www.w3.org/2000/svg"><circle cx="40" cy="41" r="4" fill="#f85149" opacity="0.9"/><line x1="40" y1="41" x2="185" y2="41" stroke="rgba(248,81,73,0.4)" stroke-width="1.5"/><line x1="40" y1="41" x2="185" y2="14" stroke="#ff7f0e" stroke-width="1.5" opacity="0.7"/><line x1="40" y1="41" x2="185" y2="68" stroke="#ff7f0e" stroke-width="1.5" opacity="0.7"/><line x1="40" y1="41" x2="185" y2="26" stroke="#ff7f0e" stroke-width="1" opacity="0.4"/><line x1="40" y1="41" x2="185" y2="56" stroke="#ff7f0e" stroke-width="1" opacity="0.4"/><rect x="62" y="32" width="8" height="18" fill="rgba(255,127,14,0.2)" stroke="#ff7f0e" stroke-width="0.8"/><rect x="92" y="27" width="8" height="28" fill="rgba(255,127,14,0.15)" stroke="#ff7f0e" stroke-width="0.8"/><rect x="132" y="21" width="8" height="40" fill="rgba(255,127,14,0.12)" stroke="#ff7f0e" stroke-width="0.8"/><text x="120" y="78" fill="rgba(255,127,14,0.35)" font-size="7" text-anchor="middle" font-family="monospace">VELO → RICH → MUON</text></svg></div>`,
  stats: [['Länge','21 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Akzeptanz','2–5 mrad']],
  text: 'LHCb misst bei p-p-Kollisionen (99,99999 % c) nur in einem engen Vorwärtskegel, wo B-Mesonen bevorzugt entstehen. Der VELO-Detektor nähert sich dem Kollisionspunkt bis auf 5,1 mm. RICH-Detektoren identifizieren Teilchen über Cherenkov-Strahlung. Ziel: die CP-Verletzung und die Asymmetrie zwischen Materie und Antimaterie im Universum verstehen.'
 }
};

// ═══════════════════════════════════════════════════════════════════════════
// PARAM INFO TEXTE — Erklärungen für CCC-Betriebsparameter
// ═══════════════════════════════════════════════════════════════════════════
const PARAM_INFO = {
 energy: 'Die Kollisionsenergie im Schwerpunktsystem beträgt das Doppelte: 6,8 TeV/Strahl → √s = 13,6 TeV. Höhere Energie ermöglicht schwerere Teilchen (E = mc²). Das Limit setzen die supraleitenden Dipolmagnete (max. 8,33 T bei 1,9 K). Die Injektionsenergie vom SPS beträgt immer 0,45 TeV.',
 intensity: 'Ein Bunch enthält ~10¹¹ Protonen. Im Nominalbetrieb hat der LHC bis zu 2 808 Bunches je Strahl (25 ns Abstand = 7,5 m). Die Luminosität wächst quadratisch mit der Intensität (L ∝ N²). Zu hohe Intensität verursacht kohärente Strahldynamik-Instabilitäten und Raumladungseffekte in den Injektoren.',
 beta: 'β* ist die Betatronfunktion am Interaktionspunkt – ein Maß für die Fokussierung in Metern. Kleines β* = kleiner Strahldurchmesser = hohe Luminosität. Bei β* = 0,30 m beträgt der Strahldurchmesser am IP nur ~13 μm – fünfmal dünner als ein Haar. Gesteuert durch supraleitende Quadrupol-Triplets 30 m vom Kollisionspunkt.',
 rampspeed: 'dB/dt bestimmt die Geschwindigkeit des Magnetfeldanstiegs. Zu schnelle Rampen erzeugen Wirbelströme in den Magnetkammern (Sextupol-Fehler) und verkleinern die dynamische Apertur. Die reale LHC-Rampe dauert ~22 min (≈ 0,008 T/s). ⚠ Werte über 0,10 T/s simulieren erhöhtes Quench-Risiko – ein Quench (Verlust der Supraleitung) stoppt den Betrieb für 2–12 Stunden.',
 ramp: 'Beim Ramping steigt der Dipolstrom von 763 A (0,45 TeV) auf bis zu 11 850 A (6,8 TeV). Die 1 232 supraleitenden NbTi-Magnete müssen dabei bei 1,9 K (unter dem λ-Punkt von ⁴He) bleiben. Gleichzeitig erhöhen die 400-MHz-HF-Hohlraumresonatoren ihre Spannung, um die Bunches per Phasenfokussierung synchron zu halten. Ein Quench erfordert Stunden der Regeneration.',
 squeeze: 'Nach dem Ramping werden die Strahlen am IP durch die innersten Quadrupol-Triplets (30 m vom Kollisionspunkt) von β* ≈ 11 m auf den Zielwert fokussiert. Bei β* = 0,3 m schrumpft der Strahldurchmesser von ~80 μm auf ~13 μm. Der Squeeze ist ein kritischer, langsamer Prozess: Zu schnelles Fokussieren überschreitet die dynamische Apertur – der Strahl geht verloren.'
};

function showInfo(key){
 const d = INFO_DB[key];
 if(!d) return;
 const panel = document.getElementById('info-panel');
 document.getElementById('info-hdr').innerHTML = d.hdr;
 document.getElementById('info-title').textContent = d.title;
 const sub = document.getElementById('info-sub');
 sub.textContent = d.sub;
 sub.style.color = d.color;
 document.getElementById('info-stats').innerHTML = d.stats.map(([l,v])=>
  `<div class="cv4-info-stat"><span class="cv4-info-stat-l">${l}</span><span class="cv4-info-stat-v" style="color:${d.color}">${v}</span></div>`
 ).join('');
 document.getElementById('info-text').textContent = d.text;
 panel.classList.add('visible');
}

function hideInfo(){
 document.getElementById('info-panel').classList.remove('visible');
}

function toggleParamInfo(id){
 const el = document.getElementById('pi-' + id);
 if(!el) return;
 const isOpen = el.classList.contains('open');
 document.querySelectorAll('.cv4-param-info.open').forEach(x => x.classList.remove('open'));
 if(!isOpen) el.classList.add('open');
}
