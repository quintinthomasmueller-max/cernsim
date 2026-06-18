// ═══════════════════════════════════════════════════════════════════════════
// INFO PANELS — Overlay für Beschleuniger, Detektoren & Detektor-Schichten.
// EINHEITLICHE 3-Feld-Stat-Struktur je Kategorie (identische Labels → direkt
// vergleichbar):
//   Beschleuniger: [Länge/Umfang, Geschwindigkeit, In Betrieb seit]
//   Detektoren:    [Maße, Schwerpunktsenergie, Gewicht]
//   Schichten:     [Aufgabe, Prinzip, Detektor]
// Jeder Eintrag nennt zusätzlich den Bild-Credit (cred) und die Sachquelle (src).
// Self-contained: greift den DOM zur Klick-Zeit per document.getElementById.
// ═══════════════════════════════════════════════════════════════════════════
import { App } from './core.js';

const INFO_DB = {
 LINAC4: {
  title: 'LINAC 4',
  sub: 'Linearbeschleuniger · Protonen-Injektor',
  color: '#58a6ff',
  img: 'Linac 4 at CERN.jpg',
  cred: 'M. Brice/CERN · CC BY-SA 4.0',
  stats: [['Länge/Umfang','86 m'],['Geschwindigkeit','0 → 52 % c'],['In Betrieb seit','2020']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'LINAC4 ist der erste Beschleuniger der Protonenkette, 86 Meter lang. Er bringt die Teilchen auf 160 MeV, also etwa 52 Prozent der Lichtgeschwindigkeit. Beschleunigt werden zunächst nicht einzelne Protonen, sondern H⁻-Ionen: ein Wasserstoffatom (ein Proton mit einem Elektron) mit einem zusätzlichen zweiten Elektron, daher negativ geladen. In dieser Form lässt sich der Strahl leichter bündeln und einspeisen. Beim Übergang zum Booster streift eine dünne Folie die beiden Elektronen ab, sodass nur das Proton übrig bleibt. LINAC4 ist seit 2020 in Betrieb und ersetzte den älteren LINAC2; er liefert etwa doppelt so intensive Strahlen.'
 },
 LINAC3: {
  title: 'LINAC 3',
  sub: 'Linearbeschleuniger · Blei-Ionen-Injektor',
  color: '#e377c2',
  img: 'Linac 3 at CERN.jpg',
  cred: 'M. Brice/CERN · CC BY-SA 4.0',
  stats: [['Länge/Umfang','~30 m'],['Geschwindigkeit','0 → 9 % c'],['In Betrieb seit','1994']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'LINAC3 ist das Gegenstück zu LINAC4 für den Schwerionen-Betrieb. In einer heißen Quelle werden Bleiatome zunächst eines Teils ihrer Elektronen beraubt (Pb²⁹⁺) und auf 4,2 MeV pro Nukleon beschleunigt, etwa 9 Prozent der Lichtgeschwindigkeit. Dass die Ionen so langsam bleiben, liegt an ihrer Masse: Ein Bleikern besteht aus 208 Nukleonen und ist über 200-mal schwerer als ein Proton. Anschließend sammelt der Ring LEIR die Ionen ein.'
 },
 PSB: {
  title: 'Proton Synchrotron Booster',
  sub: 'Synchrotron · vier gestapelte Ringe',
  color: '#58a6ff',
  img: 'The Proton Synchrotron Booster in its tunnel.jpg',
  cred: 'Loïez, Brice/CERN · CC BY 4.0',
  stats: [['Länge/Umfang','4 × 157 m'],['Geschwindigkeit','52 → 95 % c'],['In Betrieb seit','1972']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Der Proton Synchrotron Booster ist der erste Ringbeschleuniger der Kette. Er besteht aus vier exakt übereinander gestapelten Ringen, die parallel arbeiten. Der Booster hebt die Protonen von 160 MeV auf 2 GeV und damit von 52 auf 95 Prozent der Lichtgeschwindigkeit. Ab hier wächst die Geschwindigkeit kaum noch: Fast die gesamte zugeführte Energie steckt nun in der Bewegungsenergie der Teilchen, nicht mehr in höherer Geschwindigkeit. Das ist eine Folge der Relativitätstheorie.'
 },
 LEIR: {
  title: 'Low Energy Ion Ring',
  sub: 'Ionen-Synchrotron · Sammeln & Kühlen',
  color: '#e377c2',
  img: 'Low Energy Ion Ring (LEIR).jpg',
  cred: 'F. Stollberger · CC BY-SA 4.0',
  stats: [['Länge/Umfang','78 m'],['Geschwindigkeit','9 → 37 % c'],['In Betrieb seit','2005']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Der Low Energy Ion Ring ist der Sammelring für Blei-Ionen, 2005 aus dem früheren Antiprotonen-Ring LEAR umgebaut. Er nimmt die noch dünnen Ionenportionen von LINAC3 auf und bündelt sie zu dichten Paketen. Dazu dient die Elektronenkühlung: Ein paralleler Elektronenstrahl gleicher Geschwindigkeit dämpft die ungeordnete Bewegung der Ionen und macht den Strahl dadurch schärfer. Danach beschleunigt LEIR die Ionen auf 72 MeV pro Nukleon (37 Prozent der Lichtgeschwindigkeit) und gibt sie an das PS weiter.'
 },
 PS: {
  title: 'Proton Synchrotron',
  sub: 'Synchrotron · ältester noch aktiver CERN-Ring',
  color: '#2ea44f',
  img: 'https://cds.cern.ch/images/CERN-PHOTO-201405-164-2/file?size=large',
  cred: 'CERN (home.cern) · CERN-PHOTO-201405-164-2',
  stats: [['Länge/Umfang','628 m'],['Geschwindigkeit','95 → 99,94 % c'],['In Betrieb seit','1959']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Das Proton Synchrotron ist seit 1959 ununterbrochen in Betrieb und damit der älteste noch aktive Ring am CERN. Es beschleunigt die Protonen auf 26 GeV. Die Geschwindigkeit steigt dabei nur von 95 auf 99,94 Prozent der Lichtgeschwindigkeit, die Energie aber um mehr als das Zehnfache. Hier erhält der Strahl auch seine spätere Struktur: Das PS formt aus wenigen Paketen einen Batch von 72 Bunches im Abstand von je 25 Nanosekunden. Diese Bunches sind die Pakete, die später im LHC zur Kollision gebracht werden.'
 },
 SPS: {
  title: 'Super Proton Synchrotron',
  sub: 'Synchrotron · letzter Vorbeschleuniger',
  color: '#ff7f0e',
  img: 'Beamfeedingams.JPG',
  cred: 'Gillis · CC BY 3.0',
  stats: [['Länge/Umfang','6,9 km'],['Geschwindigkeit','99,94 → 99,9998 % c'],['In Betrieb seit','1976']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Das Super Proton Synchrotron ist die letzte Stufe vor dem LHC. Es bringt die Protonen auf 450 GeV. Die Geschwindigkeit steigt dabei nur von 99,94 auf 99,9998 Prozent der Lichtgeschwindigkeit, die Energie aber auf das Zwanzigfache. Von hier werden die fertigen Bunch-Züge über die Transfertunnel TI 2 und TI 8 in beide Umlaufrichtungen in den LHC eingeschossen. 1983 gelang am SPS die Entdeckung der W- und Z-Bosonen, ausgezeichnet mit dem Nobelpreis 1984.'
 },
 LHC: {
  title: 'Large Hadron Collider',
  sub: 'Protonen- & Blei-Ionen-Kollider · der energiereichste der Welt',
  color: '#58a6ff',
  img: 'LHC dipole magnets.jpg',
  cred: 'alpinethread · CC BY-SA 2.0',
  stats: [['Länge/Umfang','26,7 km'],['Geschwindigkeit','99,9998 → 99,999999 % c'],['In Betrieb seit','2008']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Im Large Hadron Collider laufen alle Strahlen zusammen: 27 Kilometer Umfang, rund 100 Meter unter der Erde. Bei 6,8 TeV sind die Protonen nur noch etwa 3 Meter pro Sekunde langsamer als das Licht. 1 232 supraleitende Dipolmagnete mit 8,3 Tesla, gekühlt auf 1,9 Kelvin und damit kälter als der Weltraum, halten die zwei Strahlen auf ihrer Kreisbahn. Sie umrunden den Ring rund 11 245-mal pro Sekunde; die Animation zeigt das stark verlangsamt. An vier Punkten kreuzen sich die Strahlen und kollidieren mit einer Schwerpunktsenergie von √s = 13,6 TeV. 2012 führte das zur Entdeckung des Higgs-Bosons.'
 },
 FCC: {
  title: 'Future Circular Collider',
  sub: 'Geplanter LHC-Nachfolger · ~91-km-Ring',
  color: '#d278ff',
  stats: [['Länge/Umfang','~91 km (×3,4 LHC)'],['Schwerpunktsenergie','bis 100 TeV (FCC-hh)'],['Status','geplant, frühestens 2040er']],
  src: 'CERN · home.cern · FCC-Studie',
  text: 'Der Future Circular Collider ist das geplante Nachfolgeprojekt des LHC: ein Ringtunnel von rund 91 Kilometern Umfang, etwa 3,4-mal so groß wie der heutige LHC. In einer ersten Stufe (FCC-ee) sollen Elektronen und Positronen das Higgs- und das Z-Boson besonders präzise vermessen, in einer zweiten Stufe (FCC-hh) Protonen bei einer Schwerpunktsenergie von bis zu 100 TeV kollidieren, rund siebenmal mehr als am LHC. Damit ließen sich noch schwerere, bislang unentdeckte Teilchen erzeugen. Das Projekt steckt in der Planungs- und Machbarkeitsphase; ein Betrieb wäre frühestens in den 2040er-Jahren möglich.'
 },
 ATLAS: {
  title: 'ATLAS Detektor',
  sub: 'A Toroidal LHC Apparatus · Punkt 1 (IP1) · Allzweck-Detektor',
  color: '#58a6ff',
  img: 'CERN LHC ATLAS Detector.jpg',
  cred: 'S. Waldherr · CC BY-SA 4.0',
  stats: [['Maße','46 × 25 m'],['Schwerpunktsenergie','√s ≤ 14 TeV'],['Gewicht','7 000 t']],
  src: 'ATLAS / CERN · home.cern · Wikipedia',
  text: 'ATLAS ist der größte der vier Detektoren, eine etwa 25 Meter hohe Anordnung konzentrischer Messschichten um den Kollisionspunkt. Kennzeichnend ist sein großes Toroid-Magnetsystem aus acht 25 Meter langen Spulen, das die weit außen liegenden Myonspuren krümmt. ATLAS ist ein Allzweckdetektor, gebaut, um möglichst jede Teilchenart zu erfassen. 2012 war ATLAS einer der beiden Detektoren, die das Higgs-Boson nachwiesen (Masse 125 GeV).'
 },
 CMS: {
  title: 'CMS Detektor',
  sub: 'Compact Muon Solenoid · Punkt 5 (IP5) · Allzweck-Detektor',
  color: '#17becf',
  img: 'CMS detector 2.jpg',
  cred: 'T. Guignard · CC BY-SA 2.0',
  stats: [['Maße','21 × 15 m'],['Schwerpunktsenergie','√s ≤ 14 TeV'],['Gewicht','14 000 t']],
  src: 'CMS / CERN · home.cern · Wikipedia',
  text: 'CMS ist kleiner als ATLAS, mit 14 000 Tonnen aber rund doppelt so schwer und damit schwerer als der Eiffelturm. Im Zentrum sitzt der stärkste Solenoid-Magnet der Welt mit 3,8 Tesla, etwa dem 100 000-Fachen des Erdmagnetfelds. Der Spurdetektor enthält 124 Millionen Silizium-Pixel, das Kalorimeter besteht aus 76 000 glasklaren Kristallen. CMS verfolgt dasselbe Allzweck-Ziel wie ATLAS und bestätigte 2012 unabhängig die Entdeckung des Higgs-Bosons.'
 },
 ALICE: {
  title: 'ALICE Detektor',
  sub: 'A Large Ion Collider Experiment · Punkt 2 (IP2) · Schwerionen',
  color: '#e377c2',
  img: 'ALICE experiment at CERN.jpg',
  cred: 'Andres T · CC BY-SA 2.0',
  stats: [['Maße','26 × 16 m'],['Schwerpunktsenergie','√s_NN ≤ 5,5 TeV'],['Gewicht','10 000 t']],
  src: 'ALICE / CERN · home.cern · Wikipedia',
  text: 'ALICE ist der Spezialist für Blei-Blei-Kollisionen. Prallen zwei Bleikerne aufeinander, entsteht für einen winzigen Moment das Quark-Gluon-Plasma, ein Urzustand der Materie wie einige Mikrosekunden nach dem Urknall: so heiß, dass Quarks und Gluonen nicht mehr in Teilchen gebunden, sondern frei sind. Eine einzige solche Kollision erzeugt tausende Teilchen gleichzeitig. Das Herzstück von ALICE, eine 90 Kubikmeter große Gas-Kammer (TPC), kann sie einzeln auseinanderhalten.'
 },
 LHCB: {
  title: 'LHCb Detektor',
  sub: 'LHC beauty · Punkt 8 (IP8) · Vorwärts-Spektrometer',
  color: '#ff7f0e',
  img: 'The LHCb detector. Courtesy of Kathleen Yurkewicz. (10134715223).jpg',
  cred: 'STFC · CC BY-SA 2.0',
  stats: [['Maße','21 × 10 m'],['Schwerpunktsenergie','√s ≤ 14 TeV'],['Gewicht','5 600 t']],
  src: 'LHCb / CERN · home.cern · Wikipedia',
  text: 'LHCb ist anders gebaut als die übrigen drei Detektoren. Es umschließt den Kollisionspunkt nicht von allen Seiten, sondern blickt wie eine Kamera nur in eine Richtung, nämlich dorthin, wo bevorzugt B-Mesonen entstehen (Teilchen mit einem b-Quark). Direkt am Strahl, nur 5 Millimeter entfernt, sitzt der VELO-Detektor; er erkennt, dass B-Mesonen erst ein kurzes Stück fliegen und dann zerfallen. Ziel von LHCb ist die Frage, warum das Universum aus Materie und fast keiner Antimaterie besteht (CP-Verletzung).'
 },
 L_TRACK: {
  title: 'Spurdetektor (Tracker)',
  sub: 'Innerste Schicht · sieht geladene Teilchen',
  color: '#58a6ff',
  img: 'First half of the CMS inner tracking barrel. 2006, Courtesy of CERN. (10134648713).jpg',
  cred: 'STFC/CERN · CC BY-SA 2.0',
  stats: [['Aufgabe','Spuren geladener Teilchen'],['Prinzip','Silizium-Sensoren (Kamerachip-Technik)'],['Detektor','alle (innerste Schicht)']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Der Spurdetektor zeichnet die Bahnen geladener Teilchen auf. Dafür gibt es zwei Technologien:\n• Halbleiter-Tracker (CMS & ATLAS): Millionen winziger Silizium-Sensoren (CMS allein 124 Millionen Pixel) arbeiten wie der Bildsensor einer Digitalkamera und messen Treffer auf Bruchteile eines Millimeters genau (etwa 0,01 mm).\n• Gas-Driftkammer (ALICE TPC): geladene Teilchen ionisieren ein Gasgemisch; die freien Elektronen driften zum Rand und ergeben ein hochauflösendes 3D-Spurbild.\nDas Magnetfeld krümmt die Bahnen: je gerader die Spur, desto höher der Impuls. Neutrale Teilchen wie Photonen oder Neutronen bleiben im Tracker unsichtbar.'
 },
 L_EM: {
  title: 'Elektromagnetisches Kalorimeter (ECAL)',
  sub: 'Schicht 2 · stoppt Elektronen & Photonen',
  color: '#2ea44f',
  img: 'One Ecal Endcap Dee Installed (2681999640).jpg',
  cred: 'µµ (Flickr) · CC BY-SA 2.0',
  stats: [['Aufgabe','stoppt Elektronen & Photonen'],['Prinzip','Energie → Lichtblitz'],['Detektor','ATLAS, CMS']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Das elektromagnetische Kalorimeter (ECAL) stoppt Elektronen und Photonen vollständig und misst ihre Energie. Die Detektoren nutzen verschiedene Konzepte:\n• Kristalle (CMS): 76 000 extrem dichte, glasklare Bleiwolframat-Kristalle (schwerer als Eisen) wandeln die Energie direkt in Lichtblitze um.\n• Flüssigargon (ATLAS): wechselnde Lagen aus Blei und flüssigem Argon messen die Ladung der entstehenden Teilchenschauer.\n• Sandwich (LHCb & ALICE): abwechselnde Platten aus Blei und szintillierendem Kunststoff fangen die Energie auf.\nEin Photon erkennt man daran, dass es im ECAL Energie hinterlässt, ohne vorher eine Spur im Spurdetektor gezogen zu haben.'
 },
 L_HAD: {
  title: 'Hadron-Kalorimeter (HCAL)',
  sub: 'Schicht 3 · stoppt Protonen, Neutronen & Pionen',
  color: '#ff7f0e',
  img: 'CMS Hcal 26 01 2007.JPG',
  cred: 'Wikimedia Commons · CC BY-SA 3.0',
  stats: [['Aufgabe','stoppt Hadronen (Jets)'],['Prinzip','Teilchenschauer in Messing/Stahl'],['Detektor','ATLAS, CMS']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Das Hadron-Kalorimeter ist die dickste Bremsschicht: Platten aus Messing und Stahl, dazwischen Kunststoff, der beim Durchgang aufleuchtet. Hadronen, also Teilchen aus Quarks wie Protonen und Pionen, lösen hier ganze Teilchenschauer aus (Jets). Ein Teil des CMS-Messings stammt übrigens aus eingeschmolzenen Granathülsen der russischen Marine.'
 },
 L_COIL: {
  title: 'Die Magnetspule',
  sub: 'Solenoid (CMS) / Toroid (ATLAS) · krümmt alle Bahnen',
  color: '#8b949e',
  img: 'CERN toroid magnets and endcap.jpg',
  cred: 'M. Formento · CC BY-SA 2.0',
  stats: [['Aufgabe','krümmt alle Teilchenbahnen'],['Prinzip','supraleitende Spule (Solenoid/Toroid)'],['Detektor','CMS, ATLAS']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Die Magnetspule ist der Grund, warum alle Spuren gebogen sind: eine supraleitende Riesenspule. CMS hat den stärksten Solenoid-Magneten der Welt (3,8 Tesla), ATLAS das markante achtarmige Toroid-System (siehe Foto). Aus der Krümmung der Bahn berechnet der Computer den Impuls jedes Teilchens; ohne Magnetfeld wüsste man nur die Richtung, nicht den Impuls.'
 },
 L_MUON: {
  title: 'Myonkammern',
  sub: 'Äußerste Schicht · nur Myonen kommen so weit',
  color: '#f85149',
  img: 'CMS muon chambers.jpg',
  cred: 'zipckr (Flickr) · CC BY 2.0',
  stats: [['Aufgabe','weist Myonen nach'],['Prinzip','nur Myonen dringen so weit'],['Detektor','ATLAS, CMS']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Myonen sind extrem durchdringend und fliegen fast ungestört durch alle Kalorimeter; sie werden ganz außen in den Myonkammern registriert. Auch hier gibt es zwei Konzepte:\n• Mit Magnet-Rückflussjoch (CMS): die Kammern sind in ein massives, 12 500 Tonnen schweres Eisenjoch eingebettet, das das Magnetfeld zurückführt.\n• Luft-Toroid-System (ATLAS): die Kammern hängen frei zwischen gigantischen Magnetschleifen, was eine Spurmessung ohne störendes Eisen erlaubt.\nVier Myonspuren auf einmal sind eine besonders saubere Signatur für den Zerfall eines Higgs-Bosons. Das Myon steht sogar im Namen des CMS-Detektors: Compact Muon Solenoid.'
 },
 L_TPC: {
  title: 'TPC — Zeitprojektionskammer',
  sub: 'ALICE-Herzstück · 3D-Kamera für 20 000 Spuren',
  color: '#e377c2',
  img: 'ALICE TPC.jpg',
  cred: 'A. Saba/CERN · CC BY-SA 3.0',
  stats: [['Aufgabe','3D-Spurbild dichter Events'],['Prinzip','driftende Elektronen im Gas'],['Detektor','ALICE']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Die Zeitprojektionskammer ist die größte Gas-Kammer der Welt: ein Zylinder mit 90 Kubikmetern Gas. Fliegt ein geladenes Teilchen hindurch, schlägt es aus den Gasatomen Elektronen heraus; diese driften zu den Endplatten und ergeben ein dreidimensionales Bild der Bahn. Nur so kann ALICE die bis zu 20 000 Spuren einer einzigen Blei-Blei-Kollision entwirren.'
 },
 L_TOF: {
  title: 'TOF — Flugzeit-Detektor',
  sub: 'ALICE · Stoppuhr mit Pikosekunden-Genauigkeit',
  color: '#2ea44f',
  stats: [['Aufgabe','Teilchensorte (π/K/p)'],['Prinzip','Flugzeit-Messung (~10⁻¹² s)'],['Detektor','ALICE']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Der Flugzeit-Detektor ist eine sehr genaue Stoppuhr: Er misst auf Billionstelsekunden genau, wann ein Teilchen ankommt. Bei gleicher Bahn bedeutet eine spätere Ankunft ein schwereres Teilchen. So unterscheidet ALICE Pionen, Kaonen und Protonen und bestimmt die Zusammensetzung des Quark-Gluon-Plasmas.'
 },
 L_VTX: {
  title: 'VELO — Vertex Locator',
  sub: 'LHCb · nur 5 mm vom Strahl entfernt',
  color: '#ff7f0e',
  img: 'VELO.jpg',
  cred: 'LHCb Collaboration · CC BY-SA 4.0',
  stats: [['Aufgabe','Zerfalls-Vertices'],['Prinzip','Silizium, 5 mm vom Strahl'],['Detektor','LHCb']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Der VELO ist der Detektor, der dem Kollisionspunkt am nächsten kommt, nur 5 Millimeter. So erkennt LHCb, dass B-Mesonen erst einige Millimeter weit fliegen und dann zerfallen. Dieser Knick, der Sekundärvertex, ist ihr Erkennungsmerkmal und der Schlüssel zur Frage, warum es im Universum mehr Materie als Antimaterie gibt.'
 },
 L_RICH: {
  title: 'RICH — Cherenkov-Ring-Detektor',
  sub: 'LHCb · Teilchen-Ausweis per Lichtkegel',
  color: '#58a6ff',
  img: 'RICH-2.jpg',
  cred: 'LHCb Collaboration · CC BY-SA 4.0',
  stats: [['Aufgabe','Teilchensorte (π/K/p)'],['Prinzip','Cherenkov-Lichtkegel'],['Detektor','LHCb']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Ist ein Teilchen in einem Medium schneller als das Licht in eben diesem Medium, erzeugt es einen Lichtkegel, das optische Gegenstück zum Überschallknall. Aus dem Durchmesser des Lichtrings liest LHCb die Geschwindigkeit ab und bestimmt zusammen mit dem Impuls die Teilchensorte.'
 },
 L_MAGNET: {
  title: 'LHCb-Dipolmagnet',
  sub: 'LHCb · 1 600 t schwere Weiche für Teilchenbahnen',
  color: '#f1e05a',
  img: 'The LHCb magnet. 2008, Courtesy of CERN. (10134714863).jpg',
  cred: 'STFC/CERN · CC BY-SA 2.0',
  stats: [['Aufgabe','krümmt Bahnen (Impuls)'],['Prinzip','Dipolmagnet im Strahlengang'],['Detektor','LHCb']],
  src: 'CERN · home.cern · Wikipedia',
  text: 'Statt einer Spule um den ganzen Detektor nutzt LHCb einen großen Dipolmagneten mitten im Strahlengang (1 600 Tonnen, etwa 4 Tesla-Meter Biegekraft). Jede geladene Spur bekommt hier einen Knick. Je kleiner der Knick, desto größer der Impuls. Das ist dasselbe Prinzip wie bei den gekrümmten Spuren in den Ring-Detektoren, nur in Vorwärtsrichtung.'
 }
};

// ═══════════════════════════════════════════════════════════════════════════
// PARAM INFO TEXTE — Erklärungen für CCC-Betriebsparameter
// ═══════════════════════════════════════════════════════════════════════════
const PARAM_INFO = {
 energy: 'Jeder der beiden Strahlen trägt bis zu 6,8 TeV. Da die Teilchen frontal aufeinandertreffen, addieren sich die Energien zur Schwerpunktsenergie √s = 13,6 TeV. Mehr Energie bedeutet, dass schwerere Teilchen erzeugt werden können (E = mc²). Die Obergrenze wird durch die supraleitenden Dipolmagnete bestimmt, da bei maximal 8,3 Tesla der Strahl gerade noch auf der Kreisbahn gehalten werden kann. Vom SPS kommt der Strahl mit 0,45 TeV Injektionsenergie an und wird anschließend beschleunigt.',
 intensity: 'Ein Bunch (Teilchenpaket) enthält rund 10¹¹ Protonen. Im Vollbetrieb kreisen bis zu 2 808 solcher Bunches pro Strahl im Abstand von je 25 Nanosekunden (7,5 Meter). Je dichter die Pakete sind, desto höher ist die Kollisionsrate. Die Luminosität wächst quadratisch mit der Intensität (L ∝ N²). Bei zu hoher Intensität stören sich die Teilchen durch ihre eigene elektrische Ladung gegenseitig, was den Strahl instabil macht.',
 beta: 'β* (Beta-Stern) beschreibt die Bündelung des Strahls am Kollisionspunkt, angegeben in Metern. Je kleiner β* ist, desto enger ist der Strahl fokussiert und desto mehr Kollisionen finden statt. Bei einem Wert von 0,30 Metern ist der Strahl am Kollisionspunkt nur noch etwa 13 Mikrometer dick, rund fünfmal dünner als ein menschliches Haar. Die Bündelung wird durch supraleitende Quadrupol-Magnete kurz vor den Detektoren erreicht.',
 rampspeed: 'dB/dt ist das Tempo, mit dem das Magnetfeld beim Hochfahren ansteigt. In den Magneten dürfen keine zu starken Wirbelströme entstehen, um die Teilchenbahn nicht zu stören. Real lässt sich der LHC dafür rund 20 Minuten Zeit, was im Mittel etwa 0,006 Tesla pro Sekunde entspricht. Ein Quench, also ein plötzlicher Zusammenbruch der Supraleitung, würde den Betrieb für Stunden lahmlegen.',
 ramp: 'Beim Hochfahren (Ramping) steigt der Strom in den Dipolmagneten von 760 Ampere bei 0,45 TeV auf etwa 11 500 Ampere bei 6,8 TeV. Die 1 232 supraleitenden Magnete müssen durchgehend auf 1,9 Kelvin gekühlt bleiben. Gleichzeitig erhöhen die Hochfrequenz-Resonatoren (400 MHz) ihre Spannung, um die Teilchenpakete zusammenzuhalten. Die Dauer der Rampe ist physikalisch berechnet: Dauer = Feldhub ΔB geteilt durch die Ramp-Rate. Bei einer Fahrt auf eine geringere Zielenergie ist die Rampe entsprechend schneller abgeschlossen.',
 squeeze: 'Nach dem Hochfahren werden die Strahlen an den Kollisionspunkten eng gebündelt. Quadrupol-Magnete rund 30 Meter vor jedem Detektor verringern β* vom Injektionswert (real rund 11 Meter, in dieser Anzeige vereinfacht 1,50 Meter) auf den Zielwert von beispielsweise 0,30 Meter. Der Strahldurchmesser schrumpft dabei auf etwa 13 Mikrometer, um eine hohe Kollisionsrate zu ermöglichen. Das muss langsam geschehen, damit der Strahl stabil bleibt.',
 prePp: 'Der Standardlauf des LHC macht rund 90 Prozent der Betriebszeit aus. Hier kollidieren Protonen bei voller Energie (Run 3: 6,8 TeV pro Strahl, √s = 13,6 TeV). An diesem Strahl arbeiten in Wirklichkeit alle vier Detektoren gleichzeitig. ATLAS und CMS suchen das Higgs-Boson im Zerfallskanal H→ZZ*→4ℓ und vermessen das Z-Boson zur Kalibrierung. LHCb untersucht die CP-Verletzung an B-Mesonen, um den Materie-Antimaterie-Unterschied im Universum zu ergründen. Da alle Experimente denselben Strahl nutzen, genügt im Widget ein Wechsel des Detektor-Reiters. Die Datenbasis des Widgets nutzt CMS-Open-Data: die Dimuon-Massen (μ⁺μ⁻) sowie die 278 veröffentlichten 4-Lepton-Higgs-Kandidaten von 2011 und 2012. Darin ist der Z-Peak bei 91 GeV und der Higgs-Anstieg bei 125 GeV zu sehen. Die Massen der Resonanzen sind physikalisch konstant; die Produktionsraten sind an die Strahlenergie angepasst.',
 preQgp: 'Der Schwerionenlauf findet etwa einen Monat pro Jahr statt. Dabei kollidieren Bleikerne bei 2,68 TeV pro Nukleon (√s_NN = 5,36 TeV). In der Kollision entsteht für einen winzigen Moment das Quark-Gluon-Plasma. Dies ist ein Urzustand der Materie, in dem Quarks und Gluonen frei beweglich sind, ähnlich wie einige Mikrosekunden nach dem Urknall. ALICE rekonstruiert die Spuren und misst, wie das Plasma gebundene Quark-Antiquark-Paare (die Mesonen J/ψ und Υ) aufschmilzt. CMS nutzt die Reihenfolge dieses Aufschmelzens als Thermometer. ATLAS und CMS vermessen das Z-Boson als Referenz, da es das Plasma unbeeinflusst durchdringt. Die Teilchenmassen basieren auf CMS-Daten. Die Effekte der Plasma-Unterdrückung sind didaktisch modelliert, da für Blei-Blei-Kollisionen keine freien Open-Data-Sätze vorliegen. Die Spurzahl im Display ist aus Gründen der Übersichtlichkeit reduziert.',
 prePilot: 'Dieser Modus dient der Inbetriebnahme und dem Testbetrieb. Der Strahl kreist mit der Injektionsenergie von 0,45 TeV ohne weiteres Hochfahren und mit geringer Intensität. Bei dieser Energie entstehen keine schweren Teilchen, was für Tests der Strahlführung und Steuerung beabsichtigt ist. Erst wenn alle Systeme stabil arbeiten, wird die Energie erhöht. So beginnt jeder Betriebszyklus des LHC. Im Massenspektrum ist daher nur der kontinuierliche Untergrund zu sehen, da die Energie für die Erzeugung schwerer Teilchen wie Z-Bosonen oder des Higgs-Bosons nicht ausreicht.',

 // ── Laien-Einstieg (Elternabend) ────────────────────────────────────────────
 introCern: 'Das CERN bei Genf betreibt den Large Hadron Collider (LHC) in einem 27 Kilometer langen Ringtunnel etwa 100 Meter unter der Erde. Darin werden zwei Strahlen aus Teilchen fast auf Lichtgeschwindigkeit beschleunigt und an vier Punkten zur Kollision gebracht. Bei den Zusammenstößen wandelt sich Energie in neue Teilchen um (nach E = mc²), die von den Detektoren ATLAS, CMS, ALICE und LHCb vermessen werden. So wurde 2012 das Higgs-Boson nachgewiesen. Vor dem LHC durchlaufen die Teilchen eine Kette von Vorbeschleunigern (LINAC, PSB/LEIR, PS und SPS), die oben im Schema dargestellt ist.',
 introUse: 'So bedienst du die Schaltzentrale. Die Schritte folgen der Reihenfolge im echten LHC-Betrieb.\n\n(1) Preset wählen: Oben stehen drei reale Betriebsmodi (Protonen-Physik, Schwerionen und Pilot-Strahl). Das gewählte Preset stellt alle Strahl-Parameter automatisch ein. Sie erscheinen links unter „LHC-Messwerte und Strahl-Parameter“. Über das Feld „Teilchen“ kann zwischen Protonen und Blei-Ionen gewechselt werden.\n\n(2) Strahl füllen: Der Knopf „Füllprotokoll starten“ schickt die Teilchenpakete durch die Vorbeschleuniger in den LHC. Das PS formt die Pakete zu Gruppen aus 72 Bunches, das SPS bündelt bis zu vier Gruppen zu einem Zug. Der Tempo-Knopf wechselt zwischen zwei Zeitmaßstäben. Füllen und Hochfahren laufen im Zeitraffer (1 Sekunde entspricht 15 Sekunden real), die spätere Datennahme läuft langsamer, da ein realer Fill viele Stunden dauert.\n\n(3) Energie-Ramping: Dieser Schritt gilt für Protonen-Physik und Schwerionen. Magnetfeld und Hochfrequenz werden hochgefahren, bis der Strahl seine Zielenergie erreicht. Beim Pilot-Strahl entfällt dieser Schritt, da die Injektionsenergie von 0,45 TeV bereits der Betriebsenergie entspricht.\n\n(4) Beam Squeeze: Quadrupol-Magnete fokussieren die beiden Strahlen an den Kollisionspunkten enger zusammen, um die Kollisionsrate für die Messungen zu erhöhen.\n\n(5) Datennahme: „Auto-Datennahme“ sammelt fortlaufend Kollisionen und füllt das Massenspektrum. Über die Detektor-Reiter (ATLAS, CMS, ALICE, LHCb) wird die Anzeige des jeweiligen Experiments ausgewählt.\n\nUnter dem Schema zeigt das Event-Display links eine einzelne Kollision. Ein Klick auf eine Schicht öffnet Erklärungen, die „Signaturen-Tour“ führt durch die Teilchenarten. Rechts wächst das Massenspektrum der gemessenen Teilchen. Ein Klick auf einen Beschleuniger oder Detektor im Plan öffnet Details und Kennzahlen.',
 evRead: 'Je nach Detektortyp liest man das Bild anders:\n• ATLAS, CMS und ALICE: der runde Querschnitt (Zwiebelschalen) — die Teilchen fliegen vom Zentrum radial nach außen.\n• LHCb (Vorwärts-Spektrometer): die Teilchen fliegen kegelförmig nach rechts durch flache, hintereinander aufgereihte Detektor-Stationen.\nIn beiden Fällen zeigt jede Linie die Spur eines Teilchens, und verschiedene Arten werden unterschiedlich gestoppt: Myonen (grün) durchqueren alles und werden ganz außen registriert, Elektronen (blau) stoppen im elektromagnetischen Kalorimeter, Photonen (gelb) hinterlassen dort Energie ohne Spur im Tracker, Hadronen (orange) erzeugen Schauer im Hadron-Kalorimeter, Neutrinos (grau gestrichelt) entweichen unbemerkt. Das Magnetfeld krümmt die Spuren geladener Teilchen zur Impulsmessung. Die Visualisierung basiert auf CMS-Open-Data. Ein Klick auf eine Detektor-Komponente zeigt Details; die Signaturen-Tour führt Schritt für Schritt durch die Teilchenarten.',
 spRead: 'Wie wiegt man Teilchen, die man nicht einmal sehen kann? In diesem Diagramm wird die Masse von instabilen Elementarteilchen bestimmt. Aus den gemessenen Spuren der Zerfallsprodukte berechnet der Computer die sogenannte invariante Masse (die Ruhemasse des ursprünglichen Mutterteilchens) und erfasst sie im Histogramm. Ein Teilchen mit einer exakt definierten Masse (eine sogenannte „Resonanz“, wie das Z-Boson bei 91 GeV) bildet dabei einen scharfen Peak über dem kontinuierlichen Untergrund. Die Signifikanz in Standardabweichungen (σ, gesprochen „Sigma“) gibt an, wie unwahrscheinlich eine zufällige Fluktuation des Untergrunds ist. Ab 5 σ gilt eine Entdeckung in der Physik als statistisch gesichert – die Wahrscheinlichkeit für einen reinen Zufall liegt dann bei unter 1 zu 3,5 Millionen. Mit genau diesem Kriterium wurde 2012 auch das Higgs-Boson nachgewiesen. Mit steigender Anzahl an Kollisionen wächst diese Signifikanz proportional zur Wurzel der gesammelten Datenmenge.'
};

// Figuren für Param-Info-Akkordeons: echtes Vorbild-Bild unter dem Text.
const PARAM_INFO_FIG = {
 evRead: {
  img: 'Candidate Higgs Events in ATLAS and CMS.png',
  cred: 'CERN, ATLAS/CMS · CC BY-SA 3.0',
  cap: 'Das Original: zwei echte Higgs-Kandidaten von 2012. Oben CMS (H→γγ: zwei grüne Energiebündel im Kristall-Kalorimeter), unten ATLAS (H→4μ: rote Spuren bis ganz nach außen). Unser Display zeichnet diese Art Bild vereinfacht nach.'
 }
};

// Echtes Foto (Wikimedia Commons, CC) als Panel-Kopf — mit Farbverlauf-Tint,
// Quellen-Credit und Offline-Fallback (falls kein Internet, Gradient-Box).
function buildPhotoHdr(d){
 if(!d.img) return d.hdr || '';
 // Voll-URL (z. B. CERN-Foto-Archiv) direkt nutzen; sonst Wikimedia-Commons-Dateiname.
 const src = /^https?:\/\//.test(d.img) ? d.img
   : 'https://commons.wikimedia.org/wiki/Special:FilePath/' + encodeURIComponent(d.img) + '?width=640';
 const fb = "this.style.display='none';this.parentNode.classList.add('cv4-hdr-noimg')";
 return `<div class="cv4-hdr-photo" style="--accent:${d.color}">`
  + `<img src="${src}" alt="${d.title}" loading="lazy" referrerpolicy="no-referrer" onerror="${fb}">`
  + `<div class="cv4-hdr-shade"></div>`
  + `<div class="cv4-hdr-cred">Foto: ${d.cred}</div>`
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
 const srcEl = document.getElementById('info-src');
 if(srcEl) srcEl.textContent = d.src ? 'Quelle: ' + d.src : '';
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
