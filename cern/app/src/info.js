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
  text: 'Das Proton-Synchrotron (PS) ist seit 1959 ununterbrochen in Betrieb. Es beschleunigt Protonen von 2 GeV (95 % c) auf 26 GeV (99,94 % c) – ab hier ist der Geschwindigkeitsgewinn minimal, aber der Energiegewinn enorm (Relativität!). Hier entsteht die LHC-Bunch-Struktur: aus wenigen Paketen des PSB formt das PS per HF-Gymnastik (Bunch-Splitting) einen Batch von 72 Bunches mit 25 ns Abstand. Das SPS sammelt dann bis zu 4 dieser Batches und fügt sie zu einem Zug (288 Bunches) zusammen, der als Einheit in den LHC geschossen wird – ~10 solcher Züge füllen einen Strahl (2808 Bunches).'
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
  text: 'ATLAS ist der größte Detektor am LHC. Kollisionen bei bis zu 99,99999 % c erzeugen Teilchenschauer, die alle Schichten durchqueren: Silizium-Pixel-Tracker (innerste Lage ~33 mm vom Strahl), LAr-Kalorimeter, Tile-Kalorimeter und das Toroid-Magnetsystem (8 Spulen je 25 m). 2012 co-Entdecker des Higgs-Bosons bei mH = 125 GeV.'
 },
 CMS: {
  title: 'CMS Detektor',
  sub: 'Compact Muon Solenoid · IP5 · Allzweck-Detektor',
  color: '#17becf',
  img: 'CMS detector 2.jpg',
  cred: 'T. Guignard · CC BY-SA 2.0',
  stats: [['Maße','21 × 15 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Gewicht','14 000 t']],
  text: 'CMS ist mit 14 000 t der schwerste Detektor am LHC. Herzstück ist ein 3,8-Tesla-Solenoid (100 000× stärker als das Erdfeld). Teilchen aus 99,99999 % c schnellen Kollisionen werden durch Silizium-Tracker (200 m² Streifen + 124 Mio. Pixel) und Bleiwolframat-Kristall-Kalorimeter (ECAL) gemessen. 2012 co-Entdecker des Higgs-Bosons.'
 },
 ALICE: {
  title: 'ALICE Detektor',
  sub: 'A Large Ion Collider Experiment · IP2 · Schwerionen-Physik',
  color: '#e377c2',
  img: 'ALICE experiment at CERN.jpg',
  cred: 'Andres T · CC BY-SA 2.0',
  stats: [['Maße','26 × 16 m'],['Pb-Pb √s_NN','≤ 5,5 TeV'],['Gewicht','10 000 t']],
  text: 'ALICE untersucht Pb-Pb-Kollisionen, bei denen Pb-Kerne mit ~99,999 % c aufeinanderprallen. Dabei entsteht Quark-Gluon-Plasma (QGP) – der Zustand der Materie Mikrosekunden nach dem Urknall. Die TPC (90 m³) identifiziert tausende Teilchen gleichzeitig; der ITS2-Tracker hat 12,5 Mrd. Pixel auf 10 m² – höchste Pixeldichte am LHC.'
 },
 LHCB: {
  title: 'LHCb Detektor',
  sub: 'LHC beauty Experiment · IP8 · Vorwärtsspektrometer',
  color: '#ff7f0e',
  img: 'The LHCb detector. Courtesy of Kathleen Yurkewicz. (10134715223).jpg',
  cred: 'STFC · CC BY-SA 2.0',
  stats: [['Länge','21 m'],['Kollisions-E.','√s ≤ 14 TeV'],['Akzeptanz','η = 2–5']],
  text: 'LHCb misst bei p-p-Kollisionen (99,99999 % c) nur in einem engen Vorwärtskegel, wo B-Mesonen bevorzugt entstehen. Der VELO-Detektor nähert sich dem Kollisionspunkt bis auf 5,1 mm. RICH-Detektoren identifizieren Teilchen über Cherenkov-Strahlung. Ziel: die CP-Verletzung und die Asymmetrie zwischen Materie und Antimaterie im Universum verstehen.'
 },

 // ── Detektor-SCHICHTEN (Event-Display: Klick auf einen Ring / eine Station) ──
 L_TRACK: {
  title: 'Spurdetektor (Tracker)',
  sub: 'Innerste Schicht · sieht geladene Teilchen',
  color: '#58a6ff',
  img: 'First half of the CMS inner tracking barrel. 2006, Courtesy of CERN. (10134648713).jpg',
  cred: 'STFC/CERN · CC BY-SA 2.0',
  stats: [['Material','Silizium (wie Kamerachips)'],['CMS-Pixel','124 Millionen'],['Präzision','~0,01 mm']],
  text: 'Die innerste Zwiebelschale: Millionen Silizium-Sensoren — im Kern dieselbe Technik wie der Chip einer Handykamera. Jedes elektrisch geladene Teilchen hinterlässt eine Kette von Treffern, aus der der Computer seine Bahn rekonstruiert. Das Magnetfeld krümmt die Bahn: je gerader die Spur, desto höher der Impuls. Neutrale Teilchen (Photonen, Neutronen) bleiben hier unsichtbar.'
 },
 L_EM: {
  title: 'Elektromagnetisches Kalorimeter (ECAL)',
  sub: 'Schicht 2 · stoppt Elektronen & Photonen',
  color: '#2ea44f',
  img: 'One Ecal Endcap Dee Installed (2681999640).jpg',
  cred: 'µµ (Flickr) · CC BY-SA 2.0',
  stats: [['CMS-Kristalle','76 000 × PbWO₄'],['Stoppt','e⁻, e⁺, γ'],['Prinzip','Energie → Lichtblitz']],
  text: 'Hier endet die Reise für Elektronen und Photonen: 76 000 Bleiwolframat-Kristalle (CMS) — glasklar, aber schwerer als Eisen. Schlägt ein Teilchen ein, erzeugt es einen winzigen Lichtblitz, dessen Helligkeit die Energie verrät. Ein Photon erkennt man genau daran, dass es hier Energie hinterlässt, OHNE vorher eine Spur im Tracker zu ziehen.'
 },
 L_HAD: {
  title: 'Hadron-Kalorimeter (HCAL)',
  sub: 'Schicht 3 · stoppt Protonen, Neutronen & Pionen',
  color: '#ff7f0e',
  img: 'CMS Hcal 26 01 2007.JPG',
  cred: 'Wikimedia Commons · CC BY-SA 3.0',
  stats: [['Material','Messing + Szintillator'],['Stoppt','p, n, π — ganze „Jets"'],['Kuriosum','Messing aus Marine-Granathülsen']],
  text: 'Die dickste Bremsschicht: Platten aus Messing und Stahl, dazwischen Kunststoff, der beim Durchschuss aufleuchtet. Hadronen — Teilchen aus Quarks, wie Protonen und Pionen — zerplatzen hier zu ganzen Teilchen-Schauern („Jets"). Kuriosum: Ein Teil des CMS-Messings wurde aus eingeschmolzenen Granathülsen der russischen Marine gefertigt.'
 },
 L_COIL: {
  title: 'Die Magnetspule',
  sub: 'Solenoid (CMS) / Toroid (ATLAS) · krümmt alle Bahnen',
  color: '#8b949e',
  img: 'CERN toroid magnets and endcap.jpg',
  cred: 'M. Formento · CC BY-SA 2.0',
  stats: [['CMS-Solenoid','3,8 T ≈ 100 000 × Erdfeld'],['ATLAS-Toroide','8 Spulen à 25 m'],['Betrieb','supraleitend (−269 °C)']],
  text: 'Der Grund, warum alle Spuren gebogen sind: eine supraleitende Riesenspule. CMS hat den stärksten Solenoid-Magneten der Welt (3,8 Tesla), ATLAS das markante achtarmige Toroid-System (Foto). Aus der Krümmung der Bahn berechnet der Computer den Impuls jedes Teilchens — ohne Magnet wüsste man nur die Richtung, nicht die „Wucht".'
 },
 L_MUON: {
  title: 'Myonkammern',
  sub: 'Äußerste Schicht · nur Myonen kommen so weit',
  color: '#f85149',
  img: 'CMS muon chambers.jpg',
  cred: 'zipckr (Flickr) · CC BY 2.0',
  stats: [['Position','äußerste Schale'],['CMS-Eisenjoch','12 500 t'],['Goldene Signatur','H→ZZ*→4μ']],
  text: 'Alles andere ist längst steckengeblieben — was hier noch ankommt, MUSS ein Myon sein. Deshalb bilden die Myonkammern die äußerste und größte Schale (bei CMS ins 12 500-Tonnen-Eisenjoch eingebaut, das rote „Riesenrad" auf den Fotos). Vier Myonen gleichzeitig sind die goldene Higgs-Signatur — das Myon steht sogar im Namen: Compact MUON Solenoid.'
 },
 L_TPC: {
  title: 'TPC — Zeitprojektionskammer',
  sub: 'ALICE-Herzstück · 3D-Kamera für 20 000 Spuren',
  color: '#e377c2',
  img: 'ALICE TPC.jpg',
  cred: 'A. Saba/CERN · CC BY-SA 3.0',
  stats: [['Volumen','90 m³ Gas'],['Spuren pro Pb-Pb-Event','bis ~20 000'],['Prinzip','driftende Elektronen → 3D-Bild']],
  text: 'Die größte „Gas-Kamera" der Welt: ein Zylinder mit 90 Kubikmetern Gas. Fliegt ein geladenes Teilchen hindurch, schlägt es aus den Gasatomen Elektronen heraus; die driften zu den Endplatten und ergeben ein dreidimensionales Bild der Bahn. Nur so kann ALICE die bis zu 20 000 Spuren einer einzigen Blei-Blei-Kollision entwirren.'
 },
 L_TOF: {
  title: 'TOF — Flugzeit-Detektor',
  sub: 'ALICE · Stoppuhr mit Pikosekunden-Genauigkeit',
  color: '#2ea44f',
  stats: [['Misst','Ankunftszeit (~10⁻¹² s genau)'],['Verrät','Teilchensorte (π/K/p)'],['Fläche','141 m²']],
  text: 'Eine gigantische Stoppuhr: Der TOF misst auf Billionstel Sekunden genau, WANN ein Teilchen ankommt. Gleiche Bahn, aber später angekommen = schwereres Teilchen. So unterscheidet ALICE Pionen, Kaonen und Protonen — die „Volkszählung" im Quark-Gluon-Plasma.'
 },
 L_VTX: {
  title: 'VELO — Vertex Locator',
  sub: 'LHCb · nur 5 mm vom Strahl entfernt',
  color: '#ff7f0e',
  img: 'VELO.jpg',
  cred: 'LHCb Collaboration · CC BY-SA 4.0',
  stats: [['Abstand zum Strahl','5 mm'],['Sieht','Zerfalls-Vertices'],['B-Mesonen-Flugstrecke','mm bis cm']],
  text: 'Der Detektor, der dem Kollisionspunkt am nächsten kommt: nur 5 Millimeter. So sieht LHCb, dass B-Mesonen erst ein paar Millimeter weit fliegen und DANN zerfallen — dieser Knick (Sekundär-Vertex) ist ihr Fingerabdruck und der Schlüssel zur Frage, warum es im Universum mehr Materie als Antimaterie gibt.'
 },
 L_RICH: {
  title: 'RICH — Cherenkov-Ring-Detektor',
  sub: 'LHCb · Teilchen-Ausweis per Lichtkegel',
  color: '#58a6ff',
  img: 'RICH-2.jpg',
  cred: 'LHCb Collaboration · CC BY-SA 4.0',
  stats: [['Prinzip','Cherenkov-Licht'],['Misst','Geschwindigkeit'],['Unterscheidet','π / K / p']],
  text: 'Ist ein Teilchen in einem Medium schneller als das Licht dort, erzeugt es einen Lichtkegel — das optische Gegenstück zum Überschallknall. Aus dem Durchmesser des Lichtrings liest LHCb die Geschwindigkeit ab und bestimmt zusammen mit dem Impuls die Teilchensorte.'
 },
 L_MAGNET: {
  title: 'LHCb-Dipolmagnet',
  sub: 'LHCb · 1 600 t schwere Weiche für Teilchenbahnen',
  color: '#f1e05a',
  img: 'The LHCb magnet. 2008, Courtesy of CERN. (10134714863).jpg',
  cred: 'STFC/CERN · CC BY-SA 2.0',
  stats: [['Gewicht','1 600 t'],['Biegekraft','4 Tm'],['Zweck','Knick → Impulsmessung']],
  text: 'Statt einer Spule um alles herum nutzt LHCb einen riesigen Dipolmagneten mitten im Strahlengang: Jede geladene Spur bekommt hier einen Knick. Je kleiner der Knick, desto größer der Impuls — dasselbe Prinzip wie die gekrümmten Spuren in den Ring-Detektoren, nur in Vorwärtsrichtung.'
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
 ramp: 'Beim Ramping steigt der Dipolstrom von 763 A (0,45 TeV) auf ~11 100 A bei 6,8 TeV (Design: 11 850 A für 7 TeV). Die 1 232 supraleitenden NbTi-Magnete müssen dabei bei 1,9 K (unter dem λ-Punkt von ⁴He) bleiben. Gleichzeitig erhöhen die 400-MHz-HF-Hohlraumresonatoren ihre Spannung, um die Bunches per Phasenfokussierung synchron zu halten. Ein Quench erfordert Stunden der Regeneration.',
 squeeze: 'Nach dem Ramping werden die Strahlen am IP durch die innersten Quadrupol-Triplets (30 m vom Kollisionspunkt) von β* ≈ 11 m auf den Zielwert fokussiert. Bei β* = 0,3 m schrumpft der Strahldurchmesser von ~80 μm auf ~13 μm. Der Squeeze ist ein kritischer, langsamer Prozess: Zu schnelles Fokussieren überschreitet die dynamische Apertur – der Strahl geht verloren.',
 prePp: 'Der Standard-Physiklauf des LHC: Protonen gegen Protonen bei voller Energie (Run 3: 6,8 TeV/Strahl → 13,6 TeV). Auf DIESEM einen Strahl laufen in Wirklichkeit alle Experimente gleichzeitig: ATLAS & CMS suchen das Higgs-Boson (2012 bei 8 TeV entdeckt, Nobelpreis 2013) im „Goldkanal" H→ZZ*→4ℓ und vermessen das Z⁰ als Kalibrierung; LHCb untersucht parallel die CP-Verletzung an B-Mesonen (warum es mehr Materie als Antimaterie gibt). Higgs und CP-Verletzung brauchen also dieselbe Maschinen-Einstellung – wechsle einfach den Detektor-Tab. So fährt der LHC ~90 % der Zeit. — Datenbasis im Widget: ECHTE CMS-Open-Data (μ⁺μ⁻, √s = 7 TeV; Resonanzmassen sind energieunabhängig, daher didaktisch auf Run 3 übertragbar – Produktionsraten skalieren mit der Energie und sind modelliert). Auch der Higgs-Goldkanal H→ZZ*→4ℓ nutzt jetzt ECHTE CMS-Open-Data: die 278 publizierten 4-Lepton-Higgs-Kandidaten von 2011/2012 (Record 5200) – darin sieht man den Z→4ℓ-Peak (91 GeV) UND den Higgs-Bump (125 GeV). In der Datennahme nehmen alle Detektoren denselben Fill GLEICHZEITIG auf.',
 preQgp: 'Der Schwerionen-Lauf (~1 Monat pro Jahr, meist am Jahresende): Statt Protonen kollidieren ganze Blei-Kerne bei 2,68 TeV/Nukleon (√s_NN = 5,36 TeV in Run 3). In der Mini-Explosion entsteht für 10⁻²³ s das Quark-Gluon-Plasma: ein „Ur-Zustand" der Materie bei über 10¹² °C, in dem Quarks und Gluonen frei sind – wie wenige Millionstelsekunden nach dem Urknall. ALICE löst die tausenden Teilchen auf und misst die J/ψ-Unterdrückung; CMS misst die sequentielle Υ-Unterdrückung (Υ(3S)>Υ(2S)>Υ(1S)) als QGP-Thermometer; ATLAS/CMS messen das Z⁰ als „Standardkerze" (es koppelt nicht ans Plasma). — Datenbasis: die Quarkonia-Massen sind ECHTE CMS-p-p-Daten; die QGP-Unterdrückung (R_AA<1) ist ein DEKLARIERTES Modell, da kein echtes Pb-Pb-Open-Data vorliegt. Die Spurmultiplizität im Event-Display ist didaktisch reduziert (real mehrere Tausend Spuren).',
 prePilot: 'Kein Physik-Experiment, sondern die Inbetriebnahme. Der Strahl läuft nur mit Injektionsenergie (0,45 TeV, kein Hochfahren) und wenigen Protonen. Bei so geringer Rate entsteht praktisch nichts Neues – das ist Absicht: Mit einem „leichten" Strahl prüfen die Operateure gefahrlos die Strahlführung, Optik und Steuerung. Erst wenn alles stabil läuft, wird auf volle Energie und Intensität hochgefahren. So beginnt real jeder LHC-Betriebszyklus. — Bei 0,45 TeV ist die Produktionsrate für schwere Teilchen (Z⁰, Higgs …) praktisch null → das Spektrum zeigt nur Untergrund-Kontinuum aus echten CMS-Open-Data.',

 // ── Laien-Einstieg (Elternabend) ────────────────────────────────────────────
 introCern: 'Das CERN bei Genf betreibt den größten Teilchenbeschleuniger der Welt, den LHC: einen 27 km langen Ringtunnel 100 m unter der Erde. Darin werden zwei Strahlen winziger Teilchen (Protonen) fast auf Lichtgeschwindigkeit gebracht und an vier Punkten frontal zur Kollision gebracht. Aus der Energie der Kollision entstehen kurzlebig neue Teilchen (E = mc²) – große Detektoren (ATLAS, CMS, ALICE, LHCb) fotografieren sie. So wurde 2012 das Higgs-Boson entdeckt. Bis ein Strahl Energie hat, durchläuft er eine Kette von Vorbeschleunigern (LINAC → PSB/LEIR → PS → SPS → LHC) – genau diese Kette siehst du oben.',
 introUse: 'So bedienst du die Schaltzentrale: (1) Strahl wählen (Protonen oder Blei-Ionen). (2) Ein Experiment-Preset laden ODER von Hand: Füllprotokoll starten → Energie-Ramping → Beam Squeeze. (3) „Auto-Datennahme" sammelt Kollisionen. Unten siehst du links eine einzelne Kollision (Event-Display) und rechts, wie sich daraus das Massenspektrum aufbaut – findet ein Detektor 5 σ, gilt das Teilchen als entdeckt. Tipp: Auf jeden Ring/Detektor klicken zeigt ein Info-Fenster mit Foto und echten Kennzahlen.',
 evRead: 'Der Detektor ist eine ZWIEBEL aus Materialschichten — die farbigen Ringe sind ihr Querschnitt. Jede Linie ist die Spur EINES Teilchens, das aus einer einzigen Kollision im Zentrum nach außen fliegt, und jede Teilchenart bleibt in „ihrer" Schicht stecken: grün = Myon (durchquert alle Schichten), blau = Elektron (stoppt im EM-Kalorimeter), gelb = Photon (EM-Kalorimeter, aber OHNE Spur), orange = Hadron-Schauer (Hadron-Kalorimeter), grau gestrichelt = fehlende Energie (ein Neutrino ist unsichtbar entkommen). Die Krümmung der Spur kommt vom Magnetfeld – je gerader, desto höher der Impuls. Aus diesem Muster rekonstruiert man, welches Teilchen zerfallen ist. (Spuren & Untergrund: echte CMS-Open-Data.) Tipp: Klicke im Bild auf eine Schicht für Foto & Erklärung — oder starte die ▶ Signaturen-Tour.',
 spRead: 'Hier „wiegen" wir Teilchen: Aus den Spuren jeder Kollision berechnen wir die invariante Masse des zerfallenen Teilchens und tragen sie ins Histogramm ein (x-Achse = Masse in GeV, y-Achse = Häufigkeit). Ein echtes Teilchen (z. B. das Z⁰ bei 91 GeV) erscheint als scharfer „Berg" über dem glatten Untergrund. Die Signifikanz (in σ) misst, wie sicher der Berg echt und kein Zufall ist – ab 5 σ spricht man von einer Entdeckung (so wurde 2012 das Higgs gefunden). Je mehr Kollisionen, desto deutlicher der Berg: die Signifikanz wächst mit der Wurzel der Datenmenge (∝ √N).'
};

// Figuren für Param-Info-Akkordeons: echtes Vorbild-Bild unter dem Text.
// evRead = die berühmten Higgs-Kandidaten von 2012 (CMS H→γγ oben, ATLAS H→4μ
// unten) — „so sieht das Original der Physiker aus".
const PARAM_INFO_FIG = {
 evRead: {
  img: 'Candidate Higgs Events in ATLAS and CMS.png',
  cred: 'CERN, ATLAS/CMS · CC BY-SA 3.0',
  cap: 'Das Original: zwei ECHTE Higgs-Kandidaten von 2012 — oben CMS (H→γγ: zwei grüne Energie-Bündel im Kristall-Kalorimeter), unten ATLAS (H→4μ: rote Spuren bis ganz nach außen). Unser Display zeichnet genau diese Art Bild vereinfacht nach.'
 }
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
App.PARAM_INFO_FIG = PARAM_INFO_FIG;
App.showInfo = showInfo;
App.hideInfo = hideInfo;
App.toggleParamInfo = toggleParamInfo;
