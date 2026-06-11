// ═══════════════════════════════════════════════════════════════════════════
// INFO PANELS — Wikipedia-Stil Overlay für Beschleuniger & Detektoren
// Einheitliche Stat-Struktur — Beschleuniger: [Länge/Umfang, Geschwindigkeit (% c),
// In Betrieb seit] · Detektoren: [Maße, Schwerpunktsenergie, Gewicht]
// Self-contained: greift den DOM zur Klick-Zeit per document.getElementById.
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

const INFO_DB = {
 LINAC4: {
  title: 'LINAC 4',
  sub: 'Linearbeschleuniger · Protonen-Quelle',
  color: '#58a6ff',
  img: 'Linac 4 at CERN.jpg',
  cred: 'M. Brice/CERN · CC BY-SA 4.0',
  stats: [['Länge','86 m'],['Geschwindigkeit','0 → 52 % c'],['In Betrieb seit','2020']],
  text: 'Der erste Schritt der Protonen-Kette: ein 86 m langer Linearbeschleuniger. Er bringt die Teilchen auf 160 MeV — schon 52 % der Lichtgeschwindigkeit. Trick an der Quelle: Gestartet wird nicht mit nackten Protonen, sondern mit H⁻-Ionen (ein Proton mit zwei zusätzlichen Elektronen), die sich leichter bündeln und einspeisen lassen. Beim Übergang zum nächsten Beschleuniger streift eine hauchdünne Folie beide Elektronen ab — übrig bleibt das reine Proton. Seit 2020 ersetzt LINAC4 den alten LINAC2 und ermöglicht doppelt so intensive Strahlen.'
 },
 LINAC3: {
  title: 'LINAC 3',
  sub: 'Linearbeschleuniger · Blei-Ionen-Quelle',
  color: '#e377c2',
  img: 'Linac 3 at CERN.jpg',
  cred: 'M. Brice/CERN · CC BY-SA 4.0',
  stats: [['Länge','~30 m'],['Geschwindigkeit','0 → 9 % c'],['In Betrieb seit','1994']],
  text: 'Das Gegenstück zu LINAC4 für den Schwerionen-Betrieb. In einer heißen Quelle werden Blei-Atome eines Teils ihrer Elektronen beraubt (Pb²⁹⁺) und auf 4,2 MeV/Nukleon beschleunigt — nur 9 % der Lichtgeschwindigkeit. Dass es so „langsam" bleibt, liegt an der Masse: Ein Blei-Kern besteht aus 208 Nukleonen und ist damit über 200-mal schwerer als ein Proton. Anschließend sammelt der LEIR-Ring die Ionen ein.'
 },
 PSB: {
  title: 'Proton Synchrotron Booster',
  sub: 'Synchrotron · vier gestapelte Ringe',
  color: '#58a6ff',
  img: 'The Proton Synchrotron Booster in its tunnel.jpg',
  cred: 'Loïez, Brice/CERN · CC BY 4.0',
  stats: [['Umfang','4 × 157 m'],['Geschwindigkeit','52 → 95 % c'],['In Betrieb seit','1972']],
  text: 'Der erste Ring-Beschleuniger (Synchrotron) der Kette — mit einer Besonderheit: vier exakt übereinander gestapelte Ringe, die parallel arbeiten. Der Booster hebt die Protonen von 160 MeV auf 2 GeV und damit von 52 % auf 95 % der Lichtgeschwindigkeit. Ab hier wächst das Tempo kaum noch: Fast die gesamte zugeführte Energie steckt jetzt in der Bewegungsenergie der Teilchen, nicht mehr in höherer Geschwindigkeit (das ist Relativität).'
 },
 LEIR: {
  title: 'Low Energy Ion Ring',
  sub: 'Ionen-Synchrotron · Sammeln & Kühlen',
  color: '#e377c2',
  img: 'Low Energy Ion Ring (LEIR).jpg',
  cred: 'F. Stollberger · CC BY-SA 4.0',
  stats: [['Umfang','78 m'],['Geschwindigkeit','9 → 37 % c'],['In Betrieb seit','2005']],
  text: 'Der Sammelring für Blei-Ionen, 2005 aus dem früheren Antiproton-Ring LEAR umgebaut. Er nimmt die noch dünnen Ionen-Portionen von LINAC3 auf und bündelt sie zu dichten Paketen. Das Werkzeug dazu ist die Elektronenkühlung: Ein paralleler Elektronenstrahl gleicher Geschwindigkeit „bremst" die Zappel-Bewegung der Ionen und macht den Strahl dadurch schärfer. Danach beschleunigt LEIR die Ionen auf 72 MeV/Nukleon (37 % c) und gibt sie an das PS weiter.'
 },
 PS: {
  title: 'Proton Synchrotron',
  sub: 'Synchrotron · ältester noch aktiver CERN-Ring',
  color: '#2ea44f',
  img: 'Aerial view of PS at CERN in 1965.jpg',
  cred: 'CERN · CC BY 4.0',
  stats: [['Umfang','628 m'],['Geschwindigkeit','95 → 99,94 % c'],['In Betrieb seit','1959']],
  text: 'Das Arbeitspferd des CERN, seit 1959 ununterbrochen in Betrieb. Das PS beschleunigt die Protonen auf 26 GeV — die Geschwindigkeit steigt dabei nur noch von 95 % auf 99,94 % c, die Energie aber um mehr als das Zehnfache. Hier bekommt der Strahl auch seine spätere Struktur: Das PS formt aus wenigen Paketen einen „Batch" von 72 Bunches im Abstand von je 25 ns. Diese Bunches sind die eigentlichen Geschosse, die später im LHC zur Kollision gebracht werden.'
 },
 SPS: {
  title: 'Super Proton Synchrotron',
  sub: 'Synchrotron · letzter Vorbeschleuniger',
  color: '#ff7f0e',
  img: 'SPS 2015.JPG',
  cred: 'Nazgul02 · CC BY-SA 4.0',
  stats: [['Umfang','6,9 km'],['Geschwindigkeit','99,94 → 99,9998 % c'],['In Betrieb seit','1976']],
  text: 'Die letzte Stufe vor dem LHC. Das SPS bringt die Protonen auf 450 GeV — die Geschwindigkeit kriecht dabei nur von 99,94 % auf 99,9998 % c, doch die Energie verzwanzigfacht sich. Von hier werden die fertigen Bunch-Züge über die Tunnel TI 2 und TI 8 in beide Richtungen in den LHC eingeschossen. Berühmt wurde das SPS 1983 mit der Entdeckung der W- und Z-Bosonen (Nobelpreis 1984).'
 },
 LHC: {
  title: 'Large Hadron Collider',
  sub: 'Protonen- & Blei-Ionen-Kollider · der stärkste der Welt',
  color: '#58a6ff',
  img: 'LHC dipole magnets.jpg',
  cred: 'alpinethread · CC BY-SA 2.0',
  stats: [['Umfang','26,7 km'],['Geschwindigkeit','99,9998 → 99,999999 % c'],['Temperatur','1,9 K']],
  text: 'Der Ring, in dem alles zusammenläuft: 27 km Umfang, 100 m unter der Erde. Bei 6,8 TeV sind die Protonen nur noch 3 m/s langsamer als das Licht. 1 232 supraleitende Dipolmagnete (8,3 Tesla, mit 1,9 K kälter als der Weltraum) zwingen die zwei Strahlen auf ihre Kreisbahn. An vier Punkten kreuzen sich die Strahlen und kollidieren mit einer Schwerpunktsenergie von √s = 13,6 TeV — mehr als je zuvor an einem Beschleuniger. 2012 führte das zur Entdeckung des Higgs-Bosons.'
 },
 ATLAS: {
  title: 'ATLAS Detektor',
  sub: 'A Toroidal LHC Apparatus · Punkt 1 (IP1) · Allzweck-Detektor',
  color: '#58a6ff',
  img: 'CERN LHC ATLAS Detector.jpg',
  cred: 'S. Waldherr · CC BY-SA 4.0',
  stats: [['Maße','46 × 25 m'],['Schwerpunktsenergie','√s ≤ 14 TeV'],['Gewicht','7 000 t']],
  text: 'Der größte der vier Detektoren — eine 25 m hohe „Zwiebel" aus Messschichten rund um den Kollisionspunkt. Sein Markenzeichen ist das gewaltige Toroid-Magnetsystem aus acht 25-m-Spulen, das den weit außen liegenden Myon-Spuren ihre Krümmung gibt. ATLAS ist ein Allzweck-Detektor: gebaut, um möglichst jede Teilchenart zu erfassen. 2012 war ATLAS einer der beiden Entdecker des Higgs-Bosons (Masse 125 GeV).'
 },
 CMS: {
  title: 'CMS Detektor',
  sub: 'Compact Muon Solenoid · Punkt 5 (IP5) · Allzweck-Detektor',
  color: '#17becf',
  img: 'CMS detector 2.jpg',
  cred: 'T. Guignard · CC BY-SA 2.0',
  stats: [['Maße','21 × 15 m'],['Schwerpunktsenergie','√s ≤ 14 TeV'],['Gewicht','14 000 t']],
  text: 'Kleiner als ATLAS, aber mit 14 000 t fast doppelt so schwer — schwerer als der Eiffelturm. Im Zentrum sitzt der stärkste Solenoid-Magnet der Welt (3,8 Tesla, rund 100 000-mal das Erdmagnetfeld). Sein Spurdetektor besitzt 124 Millionen Silizium-Pixel, das Kalorimeter besteht aus 76 000 glasklaren Kristallen. CMS verfolgt dasselbe Allzweck-Ziel wie ATLAS — und bestätigte 2012 unabhängig die Entdeckung des Higgs-Bosons.'
 },
 ALICE: {
  title: 'ALICE Detektor',
  sub: 'A Large Ion Collider Experiment · Punkt 2 (IP2) · Schwerionen',
  color: '#e377c2',
  img: 'ALICE experiment at CERN.jpg',
  cred: 'Andres T · CC BY-SA 2.0',
  stats: [['Maße','26 × 16 m'],['Schwerpunktsenergie','√s_NN ≤ 5,5 TeV'],['Gewicht','10 000 t']],
  text: 'Der Spezialist für Blei-Blei-Kollisionen. Prallen zwei Blei-Kerne aufeinander, entsteht für einen winzigen Moment das Quark-Gluon-Plasma — ein Urzustand der Materie wie wenige Millionstel-Sekunden nach dem Urknall: so heiß, dass Quarks und Gluonen nicht mehr in Teilchen gebunden, sondern frei sind. Eine solche Kollision erzeugt tausende Teilchen auf einmal. ALICEs Herzstück, eine 90 m³ große Gas-Kammer (TPC), kann sie alle einzeln auseinanderhalten.'
 },
 LHCB: {
  title: 'LHCb Detektor',
  sub: 'LHC beauty · Punkt 8 (IP8) · Vorwärts-Spektrometer',
  color: '#ff7f0e',
  img: 'The LHCb detector. Courtesy of Kathleen Yurkewicz. (10134715223).jpg',
  cred: 'STFC · CC BY-SA 2.0',
  stats: [['Länge','21 m'],['Schwerpunktsenergie','√s ≤ 14 TeV'],['Gewicht','5 600 t']],
  text: 'Anders gebaut als die übrigen drei: LHCb umschließt den Kollisionspunkt nicht von allen Seiten, sondern blickt wie eine Kamera nur in eine Richtung — genau dorthin, wo bevorzugt B-Mesonen entstehen (Teilchen mit einem b-Quark). Direkt am Strahl, nur 5 mm entfernt, sitzt der VELO-Detektor; er sieht, dass B-Mesonen erst ein Stück weit fliegen und dann zerfallen. Ziel ist die große Frage, warum das Universum aus Materie und fast keiner Antimaterie besteht (CP-Verletzung).'
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
 energy: 'Jeder der beiden Strahlen trägt bis zu 6,8 TeV. Weil sie frontal aufeinanderprallen, addieren sich die Energien zur Schwerpunktsenergie √s = 13,6 TeV. Mehr Energie bedeutet: Es können schwerere Teilchen entstehen (E = mc²). Die Grenze setzen die supraleitenden Dipolmagnete — bei maximal 8,3 Tesla lässt sich der Strahl gerade noch auf der Kreisbahn halten. Vom SPS kommt der Strahl immer mit 0,45 TeV an (Injektionsenergie) und wird dann hochgefahren.',
 intensity: 'Ein Bunch (Teilchenpaket) enthält rund 10¹¹ Protonen. Im Vollbetrieb kreisen bis zu 2 808 solcher Bunches pro Strahl, im Abstand von je 25 ns (7,5 m). Je dichter die Pakete, desto mehr Kollisionen — die Kollisionsrate (Luminosität) wächst sogar quadratisch mit der Intensität (L ∝ N²). Treibt man es zu weit, stören sich die Teilchen über ihre eigene Ladung gegenseitig und der Strahl wird instabil.',
 beta: 'β* (sprich „Beta-Stern") beschreibt, wie stark der Strahl am Kollisionspunkt gebündelt wird — angegeben in Metern: je kleiner β*, desto dünner der Strahl und desto mehr Kollisionen. Bei β* = 0,30 m ist der Strahl am Kollisionspunkt nur noch ~13 µm dick, rund fünfmal dünner als ein menschliches Haar. Erzeugt wird diese enge Bündelung von supraleitenden Quadrupol-Magneten rund 30 m vor jedem Detektor.',
 rampspeed: 'dB/dt ist das Tempo, mit dem das Magnetfeld beim Hochfahren ansteigt. Zu schnell ist gefährlich: In den Magneten entstehen Wirbelströme, die die Bahn stören. Real lässt sich der LHC dafür rund 22 Minuten Zeit (etwa 0,008 T/s). ⚠ Oberhalb von 0,10 T/s steigt hier das Risiko eines Quenchs — eines plötzlichen Zusammenbruchs der Supraleitung. Ein echter Quench legt den Betrieb für Stunden lahm.',
 ramp: 'Beim Hochfahren („Ramping") steigt der Strom in den Dipolmagneten von 760 A (bei 0,45 TeV) auf etwa 11 100 A (bei 6,8 TeV). Die 1 232 supraleitenden Magnete müssen dabei durchgehend auf 1,9 K gekühlt bleiben. Gleichzeitig drehen die Hochfrequenz-Resonatoren (400 MHz) ihre Spannung hoch, um die Bunches zusammenzuhalten. Steigt das Feld zu schnell, droht ein Quench — und der Strahl ist verloren.',
 squeeze: 'Nach dem Hochfahren werden die Strahlen an den Kollisionspunkten enggebündelt („Squeeze"): Quadrupol-Magnete rund 30 m vor jedem Detektor drücken β* von etwa 11 m auf den Zielwert herunter. Bei β* = 0,30 m schrumpft der Strahldurchmesser dabei von ~80 µm auf ~13 µm. Das muss langsam geschehen — geht es zu schnell, läuft der Strahl aus der stabilen Bahn und ist verloren.',
 prePp: 'Der Standard-Lauf des LHC, rund 90 % der Betriebszeit: Protonen gegen Protonen bei voller Energie (Run 3: 6,8 TeV pro Strahl, √s = 13,6 TeV). Auf demselben Strahl arbeiten in Wirklichkeit ALLE Experimente gleichzeitig: ATLAS und CMS suchen das Higgs-Boson (2012 entdeckt, Nobelpreis 2013) im „Goldkanal" H→ZZ*→4ℓ und vermessen das Z⁰ zur Eichung; LHCb untersucht parallel die CP-Verletzung an B-Mesonen (warum es mehr Materie als Antimaterie gibt). Higgs und CP-Verletzung brauchen also keine andere Maschinen-Einstellung — wechsle einfach den Detektor-Tab. — Datenbasis im Widget: echte CMS-Open-Data — die Dimuon-Massen (μ⁺μ⁻) und die 278 publizierten 4-Lepton-Higgs-Kandidaten von 2011/2012; darin sieht man den Z→4ℓ-Peak (91 GeV) UND den Higgs-Bump (125 GeV). Resonanzmassen hängen nicht von der Strahlenergie ab; die Produktionsraten sind modelliert und mit der Energie skaliert.',
 preQgp: 'Der Schwerionen-Lauf, etwa ein Monat pro Jahr: Statt Protonen kollidieren ganze Blei-Kerne bei 2,68 TeV/Nukleon (√s_NN = 5,36 TeV). In der Mini-Explosion entsteht für rund 10⁻²³ s das Quark-Gluon-Plasma — ein Urzustand der Materie bei über 10¹² °C, in dem Quarks und Gluonen frei sind, wie wenige Millionstel-Sekunden nach dem Urknall. ALICE löst die tausenden Teilchen auf und misst, wie das Plasma gebundene Quark-Paare (J/ψ, Υ) wieder „aufschmilzt"; CMS nutzt die Reihenfolge dieses Schmelzens (Υ(3S) vor Υ(2S) vor Υ(1S)) als Thermometer; ATLAS und CMS messen das Z⁰ als Vergleichsmaßstab, da es vom Plasma unberührt bleibt. — Datenbasis: Die Teilchenmassen sind echte CMS-Daten; die Plasma-Unterdrückung ist ein deklariertes Modell (es liegt kein echtes Pb-Pb-Open-Data vor). Die Spurzahl im Display ist didaktisch reduziert (real mehrere Tausend Spuren).',
 prePilot: 'Kein Physik-Experiment, sondern die Inbetriebnahme. Der Strahl läuft nur mit Injektionsenergie (0,45 TeV, kein Hochfahren) und wenigen Teilchen. Bei so geringer Rate entsteht praktisch nichts Neues — und genau das ist Absicht: Mit einem „leichten" Strahl prüfen die Operateure gefahrlos Strahlführung, Optik und Steuerung. Erst wenn alles stabil läuft, wird auf volle Energie und Intensität hochgefahren. So beginnt real jeder LHC-Betriebszyklus. — Im Spektrum erscheint deshalb nur Untergrund (echte CMS-Open-Data): Für schwere Teilchen wie Z⁰ oder Higgs fehlt bei 0,45 TeV schlicht die Energie.',

 // ── Laien-Einstieg (Elternabend) ────────────────────────────────────────────
 introCern: 'Das CERN bei Genf betreibt den größten Teilchenbeschleuniger der Welt, den LHC: einen 27 km langen Ringtunnel, 100 m unter der Erde. Darin werden zwei Strahlen aus winzigen Teilchen (meist Protonen) fast auf Lichtgeschwindigkeit gebracht und an vier Punkten frontal zur Kollision geführt. Aus der Energie der Kollision entstehen für Sekundenbruchteile neue Teilchen (E = mc²), die große Detektoren (ATLAS, CMS, ALICE, LHCb) vermessen. So wurde 2012 das Higgs-Boson entdeckt. Bevor ein Strahl seine volle Energie hat, durchläuft er eine ganze Kette von Vorbeschleunigern (LINAC → PSB/LEIR → PS → SPS → LHC) — genau diese Kette siehst du oben im Plan.',
 introUse: 'So bedienst du die Schaltzentrale: (1) Strahl wählen — Protonen oder Blei-Ionen. (2) Ein Experiment-Preset laden ODER von Hand vorgehen: Füllprotokoll → Energie-Ramping → Beam Squeeze. (3) „Auto-Datennahme" sammelt Kollisionen. Unten siehst du links eine einzelne Kollision (Event-Display) und rechts, wie sich daraus nach und nach das Massenspektrum aufbaut — erreicht ein Detektor 5 σ, gilt das Teilchen als entdeckt. Tipp: Ein Klick auf jeden Ring oder Detektor öffnet ein Info-Fenster mit Foto und echten Kennzahlen.',
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
 if(key.startsWith('L_') && App.setActiveLayer) App.setActiveLayer(key);
}

function hideInfo(){
 document.getElementById('info-panel').classList.remove('visible');
 if(App.setActiveLayer) App.setActiveLayer(null);
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
