// ═══════════════════════════════════════════════════════════════════════════
// INFO PANELS — Wikipedia-Stil Overlay für Beschleuniger & Detektoren
// Einheitliche Stat-Struktur: [Energie/Maße, β-Bereich / Kollisions-E., Gebaut/Gewicht]
// Self-contained: greift den DOM zur Klick-Zeit per document.getElementById.
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

const INFO_DB = {
 LINAC4: {
  title: 'LINAC 4',
  sub: 'Linearbeschleuniger · Protonen (H⁻ → Stripping)',
  color: '#58a6ff',
  img: 'Linac 4 at CERN.jpg',
  cred: 'M. Brice/CERN · CC BY-SA 4.0',
  stats: [['Länge','86 m'],['β-Bereich','0 → 52 % c'],['Seit','2020']],
  text: 'LINAC4 ist der erste Schritt im Proton-Injektorkomplex. Er beschleunigt H⁻-Ionen (Protonen mit zwei Elektronen) mittels Hochfrequenz-Strukturen auf 160 MeV, entsprechend 52 % der Lichtgeschwindigkeit. Beim Transfer zum PSB entfernt eine Stripperfolie die Elektronen. Seit 2020 ersetzt er LINAC2 und verdoppelt die Strahlintensität für den LHC.'
 },
 LINAC3: {
  title: 'LINAC 3',
  sub: 'Linearbeschleuniger · Blei-Ionen (ECR-Quelle)',
  color: '#e377c2',
  img: 'Linac 3 at CERN.jpg',
  cred: 'M. Brice/CERN · CC BY-SA 4.0',
  stats: [['Länge','~30 m'],['β-Bereich','0 → 9 % c'],['Seit','1994']],
  text: 'LINAC3 beschleunigt Blei-Ionen (Pb²⁹⁺) aus einer Elektronen-Zyklotron-Resonanz-Quelle (ECR) auf 4,2 MeV pro Nukleon – nur 9 % der Lichtgeschwindigkeit, da Blei-Kerne (A=208) viel schwerer sind als Protonen. Die Ionen werden danach in LEIR gestapelt und durch Elektronenkühlung komprimiert. LINAC3 ist seit 1994 in Betrieb.'
 },
 PSB: {
  title: 'Proton Synchrotron Booster',
  sub: 'Synchrotron · 4 übereinander gestapelte Ringe',
  color: '#58a6ff',
  img: 'The Proton Synchrotron Booster in its tunnel.jpg',
  cred: 'Loïez, Brice/CERN · CC BY 4.0',
  stats: [['Umfang','4 × 157 m'],['β-Bereich','52 → 95 % c'],['Gebaut','1972']],
  text: 'Der PSB besteht aus vier übereinandergestapelten Synchrotron-Ringen und beschleunigt Protonen von 160 MeV (52 % c) auf 2 GeV (95 % c). Nach dem LHC-Injector-Upgrade (LIU, 2020) liefert er doppelt so hohe Strahlintensitäten. Die vier Ringe erlauben das gleichzeitige Beschleunigen mehrerer Pakete mit unterschiedlichem Timing.'
 },
 LEIR: {
  title: 'Low Energy Ion Ring',
  sub: 'Ionen-Synchrotron · Elektronenkühlung',
  color: '#e377c2',
  img: 'Low Energy Ion Ring (LEIR).jpg',
  cred: 'F. Stollberger · CC BY-SA 4.0',
  stats: [['Umfang','78 m'],['β-Bereich','9 → 37 % c'],['Aus LEAR','2005']],
  text: 'LEIR (Low Energy Ion Ring) wurde 2005 aus dem Antiproton-Ring LEAR umgebaut. Er akkumuliert Blei-Ionen von LINAC3 (9 % c) und kühlt sie per Elektronenkühlung: Ein Elektronenstrahl gleicher Mittelsgeschwindigkeit reduziert die Impulsstreuung dramatisch. Danach werden die Ionen auf 72 MeV/u (37 % c) beschleunigt und an den PS übergeben.'
 },
 PS: {
  title: 'Proton Synchrotron',
  sub: 'Synchrotron · Ältester noch aktiver CERN-Beschleuniger',
  color: '#2ea44f',
  img: 'Aerial view of PS at CERN in 1965.jpg',
  cred: 'CERN · CC BY 4.0',
  stats: [['Umfang','628 m'],['β-Bereich','95 → 99,94 % c'],['Seit','1959']],
  text: 'Das Proton-Synchrotron (PS) ist seit 1959 ununterbrochen in Betrieb. Es beschleunigt Protonen von 2 GeV (95 % c) auf 26 GeV (99,94 % c) – ab hier ist der Geschwindigkeitsgewinn minimal, aber der Energiegewinn enorm (Relativität!). Hier entsteht die LHC-Bunch-Struktur: aus wenigen Paketen des PSB formt das PS per HF-Gymnastik (Bunch-Splitting) einen Batch von 72 Bunches mit 25 ns Abstand. Das SPS sammelt dann bis zu 4 dieser Batches und fügt sie zu einem Zug (288 Bunches) zusammen, der als Einheit in den LHC geschossen wird – ~12 Schüsse füllen einen Strahl (2808 Bunches).'
 },
 SPS: {
  title: 'Super Proton Synchrotron',
  sub: 'Synchrotron · Nobelpreis-Beschleuniger (1984)',
  color: '#ff7f0e',
  img: 'SPS 2015.JPG',
  cred: 'Nazgul02 · CC BY-SA 4.0',
  stats: [['Umfang','6,9 km'],['β-Bereich','99,94 → 99,9998 % c'],['Gebaut','1976']],
  text: 'Das SPS (1976) beschleunigt auf 450 GeV – die Geschwindigkeit steigt dabei von 99,94 % auf 99,9998 % c, ein scheinbar kleiner Unterschied mit riesiger Energiewirkung. Berühmt durch die Entdeckung der W- und Z-Bosonen 1983 (Nobelpreis 1984). Als letzter Vorbeschleuniger liefert es beide LHC-Strahlen über TI 2 und TI 8.'
 },
 LHC: {
  title: 'Large Hadron Collider',
  sub: 'Proton-Proton / Pb-Pb Kollider · Leistungsstärkster der Welt',
  color: '#58a6ff',
  img: 'LHC dipole magnets.jpg',
  cred: 'alpinethread · CC BY-SA 2.0',
  stats: [['Umfang','26 659 m'],['β bei 6,8 TeV','99,99999 % c'],['Temp.','1,9 K']],
  text: 'Im LHC sind Protonen mit 6,8 TeV nur noch 3 m/s langsamer als Licht (99,99999 % c). 1 232 supraleitende Dipolmagnete (8,33 T, NbTi bei 1,9 K) halten die Strahlen auf Kreisbahn. An vier Interaktionspunkten kollidieren Protonenpakete bei √s = 13,6 TeV – mehr Energie als je zuvor erreicht. 2012 führte der LHC zur Entdeckung des Higgs-Bosons.'
 },
 ATLAS: {
  title: 'ATLAS Detektor',
  sub: 'A Toroidal LHC Apparatus · IP1 · Allzweck-Detektor',
  color: '#58a6ff',
  img: 'CERN LHC ATLAS Detector.jpg',
  cred: 'S. Waldherr · CC BY-SA 4.0',
  stats: [['Maße','46 × 25 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Gewicht','7 000 t']],
  text: 'ATLAS ist der größte Detektor am LHC. Kollisionen bei bis zu 99,99999 % c erzeugen Teilchenschauer, die alle Schichten durchqueren: Silizium-Pixel-Tracker (ab 5 mm vom Strahl), LAr-Kalorimeter, Tile-Kalorimeter und das Toroid-Magnetsystem (8 Spulen je 25 m). 2012 co-Entdecker des Higgs-Bosons bei mH = 125 GeV.'
 },
 CMS: {
  title: 'CMS Detektor',
  sub: 'Compact Muon Solenoid · IP5 · Allzweck-Detektor',
  color: '#17becf',
  img: 'CMS detector 2.jpg',
  cred: 'T. Guignard · CC BY-SA 2.0',
  stats: [['Maße','21 × 15 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Gewicht','14 000 t']],
  text: 'CMS ist mit 14 000 t der schwerste Detektor am LHC. Herzstück ist ein 3,8-Tesla-Solenoid (100 000× stärker als das Erdfeld). Teilchen aus 99,99999 % c schnellen Kollisionen werden durch Silizium-Tracker (200 m², 75 Mio. Pixel) und Bleiwolframat-Kristall-Kalorimeter (ECAL) gemessen. 2012 co-Entdecker des Higgs-Bosons.'
 },
 ALICE: {
  title: 'ALICE Detektor',
  sub: 'A Large Ion Collider Experiment · IP2 · Schwerionen-Physik',
  color: '#e377c2',
  img: 'ALICE experiment at CERN.jpg',
  cred: 'Andres T · CC BY-SA 2.0',
  stats: [['Maße','26 × 16 m'],['Pb-Pb √s_NN','≤ 5,5 TeV'],['Gewicht','10 000 t']],
  text: 'ALICE untersucht Pb-Pb-Kollisionen, bei denen Pb-Kerne mit ~99,999 % c aufeinanderprallen. Dabei entsteht Quark-Gluon-Plasma (QGP) – der Zustand der Materie microsekunden nach dem Urknall. Die TPC (90 m³) identifiziert tausende Teilchen gleichzeitig; der ITS2-Tracker hat 12,5 Mrd. Pixel auf 10 m² – höchste Pixeldichte am LHC.'
 },
 LHCB: {
  title: 'LHCb Detektor',
  sub: 'LHC beauty Experiment · IP8 · Vorwärtsspektrometer',
  color: '#ff7f0e',
  img: 'The LHCb detector. Courtesy of Kathleen Yurkewicz. (10134715223).jpg',
  cred: 'STFC · CC BY-SA 2.0',
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
 squeeze: 'Nach dem Ramping werden die Strahlen am IP durch die innersten Quadrupol-Triplets (30 m vom Kollisionspunkt) von β* ≈ 11 m auf den Zielwert fokussiert. Bei β* = 0,3 m schrumpft der Strahldurchmesser von ~80 μm auf ~13 μm. Der Squeeze ist ein kritischer, langsamer Prozess: Zu schnelles Fokussieren überschreitet die dynamische Apertur – der Strahl geht verloren.',
 prePp: 'Der Standard-Physiklauf des LHC: Protonen gegen Protonen bei voller Energie (Run 3: 6,8 TeV/Strahl → 13,6 TeV). Auf DIESEM einen Strahl laufen in Wirklichkeit alle Experimente gleichzeitig: ATLAS & CMS suchen das Higgs-Boson (2012 bei 8 TeV entdeckt, Nobelpreis 2013) im „Goldkanal" H→ZZ*→4ℓ und vermessen das Z⁰ als Kalibrierung; LHCb untersucht parallel die CP-Verletzung an B-Mesonen (warum es mehr Materie als Antimaterie gibt). Higgs und CP-Verletzung brauchen also dieselbe Maschinen-Einstellung – wechsle einfach den Detektor-Tab. So fährt der LHC ~90 % der Zeit.',
 preQgp: 'Der Schwerionen-Lauf (~1 Monat pro Jahr, meist am Jahresende): Statt Protonen kollidieren ganze Blei-Kerne bei 2,68 TeV/Nukleon (√s_NN = 5,36 TeV in Run 3). In der Mini-Explosion entsteht für 10⁻²³ s das Quark-Gluon-Plasma: ein „Ur-Zustand" der Materie bei über 10¹² °C, in dem Quarks und Gluonen frei sind – wie wenige Millionstelsekunden nach dem Urknall. ALICE ist der Spezialdetektor dafür und löst die tausenden Teilchen einer einzigen Kollision auf. ATLAS/CMS messen hier das Z⁰ als „Standardkerze" (es koppelt nicht ans Plasma).',
 prePilot: 'Kein Physik-Experiment, sondern die Inbetriebnahme. Der Strahl läuft nur mit Injektionsenergie (0,45 TeV, kein Hochfahren) und wenigen Protonen. Bei so geringer Rate entsteht praktisch nichts Neues – das ist Absicht: Mit einem „leichten" Strahl prüfen die Operateure gefahrlos die Strahlführung, Optik und Steuerung. Erst wenn alles stabil läuft, wird auf volle Energie und Intensität hochgefahren. So beginnt real jeder LHC-Betriebszyklus.'
};

// Echtes Foto (Wikimedia Commons, CC) als Panel-Kopf — mit Farbverlauf-Tint,
// Quellen-Credit und Offline-Fallback (falls kein Internet, Gradient-Box).
function buildPhotoHdr(d){
 if(!d.img) return d.hdr || '';
 const src = 'https://commons.wikimedia.org/wiki/Special:FilePath/' + encodeURIComponent(d.img) + '?width=640';
 const fb = "this.style.display='none';this.parentNode.classList.add('cv4-hdr-noimg')";
 return `<div class="cv4-hdr-photo" style="--accent:${d.color}">`
  + `<img src="${src}" alt="${d.title}" loading="lazy" referrerpolicy="no-referrer" onerror="${fb}">`
  + `<div class="cv4-hdr-shade"></div>`
  + `<div class="cv4-hdr-cred">📷 ${d.cred}</div>`
  + `<div class="cv4-hdr-fbtxt">${d.title}</div>`
  + `</div>`;
}

function showInfo(key){
 const d = INFO_DB[key];
 if(!d) return;
 const panel = document.getElementById('info-panel');
 document.getElementById('info-hdr').innerHTML = buildPhotoHdr(d);
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

App.PARAM_INFO = PARAM_INFO;
App.showInfo = showInfo;
App.hideInfo = hideInfo;
App.toggleParamInfo = toggleParamInfo;
