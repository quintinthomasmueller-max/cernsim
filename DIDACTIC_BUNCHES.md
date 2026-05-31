# ⚛️ Didaktisches Konzept: Reelle Teilchenbewegung & Bunch-Spacing (DIDACTIC_BUNCHES.md)

Dieses Dokument liefert den theoretischen und didaktischen Blueprint, um das manuelle Versenden von Teilchenpaketen durch ein physikalisch korrektes, phase-gelocktes **Bunch-Spacing-Modell** zu ersetzen. Ziel ist es, Schülern des P-Seminars die Notwendigkeit von Hochfrequenz-Synchronisation und symmetrischer Strahlfüllung spielerisch und visuell begreifbar zu machen.

---

## 1. Die physikalischen Gesetze der LHC-Befüllung

Im echten Large Hadron Collider reisen Teilchen nicht im kontinuierlichen Strom, sondern in präzise paketierten Bunches.

### A. Das RF-Bucket-Gitter (Die Potentialtöpfe)
Die Beschleunigung und Fokussierung der Teilchen in longitudinaler Richtung erfolgt durch Radiofrequenz-Kavitäten (RF Cavities) bei $400\text{ MHz}$. Diese erzeugen elektromagnetische Wellen, in denen sich stabile Phasenbereiche bilden – die sogenannten **RF-Buckets** (Potentialtöpfe).
*   Ein Teilchenpaket kann sich **nur** in einem solchen Bucket befinden. Es gibt im LHC genau **35.640 Buckets** entlang des $26,659\text{ km}$ langen Rings.
*   Der physische Abstand zwischen zwei Buckets entspricht der RF-Wellenlänge von $\lambda \approx 75\text{ cm}$ (oder $2,5\text{ ns}$ Zeitabstand).

### B. Das Bunch-Spacing (Paket-Abstand)
Aus technischen Gründen (z. B. um Kollisionen außerhalb der Detektoren zu vermeiden) wird nicht jedes Bucket befüllt. Das Standard-Bunch-Spacing beträgt **$25\text{ ns}$** (entspricht 10 Buckets Abstand oder **$7,5\text{ Metern}$** physischer Distanz).
*   Die maximale Anzahl von Bunches pro Strahl liegt bei **2.808**.
*   Zwischen den Bunch-Paketen müssen Lücken (Gaps) gelassen werden, damit die schnellen Ablenkmagnete (Kicker) Zeit haben, die Strahlen ein- und auszuschießen, ohne die kreisenden Teilchen zu zerstören.

### C. Kollisions-Symmetrie
Damit die Teilchenpakete von Strahl 1 (im Uhrzeigersinn, CW) und Strahl 2 (gegen den Uhrzeigersinn, CCW) exakt in den vier Detektoren kollidieren, müssen:
1.  Beide Strahlen die **exakt gleiche Anzahl** an Bunches enthalten.
2.  Die Bunches in einem **symmetrischen Füllschema** angeordnet sein.
3.  Die Phasenlage so synchronisiert sein, dass sich die entgegenkommenden Pakete *präzise* im Zentrum der Detektoren (Interaktionspunkte IP 1, 2, 5, 8) kreuzen.

---

## 2. Das didaktische Visualisierungs-Konzept

Um diese hochkomplexen Konzepte für Schüler anschaulich darzustellen, skalieren wir das Modell didaktisch herunter (z. B. auf **12 Buckets** für den LHC-Ring) und führen interaktive, spielerische Elemente ein:

### Phase 1: Sichtbar machen der RF-Buckets (Das „Zahnrad“-Modell)
*   **Visualisierung**: Der LHC-Ring wird nicht als leere Linie dargestellt, sondern als ein schwach glimmendes, kreisförmiges Band mit **12 markierten Slots (Buckets)** (jeweils bei $0^\circ, 30^\circ, 60^\circ, \dots, 330^\circ$).
*   **Didaktischer Effekt**: Die Schüler verstehen sofort, dass der LHC wie ein riesiges, unsichtbares Zahnrad funktioniert. Ein Bunch kann nicht frei platziert werden, sondern muss in einen dieser Slots einrasten (Phase Locking).

```
          [CMS Detektor] (Top, 90°)
             /  |  \
   Slot 11  O   O   O  Slot 1
  Slot 10  O         O  Slot 2
[ALICE] --O     +     O-- [LHCb Detektor]
  Slot 8   O         O  Slot 4
   Slot 7   O   O   O  Slot 5
             \  |  \
         [ATLAS Detektor] (Bottom, 270°)
```

### Phase 2: Phasen-gelockte Injektion (Bunch Trains)
*   Anstatt einzelne Klicks willkürliche Punkte erzeugen zu lassen, simuliert das Stellwerk die Injektion von **Bunch Trains** (Paketketten):
    *   Klick auf **Inject Beam 1**: Ein Zug aus z. B. 4 im Abstand von $60^\circ$ synchronisierten blauen Bunches wandert von der Quelle durch das SPS-System und füllt die Slots 1, 3, 5 und 7 im LHC.
    *   Klick auf **Inject Beam 2**: Ein entsprechender Zug aus 4 orangefarbenen Bunches wird über TI 8 in die entgegengesetzte Richtung injiziert und füllt symmetrisch die Slots 11, 9, 7 und 5.
*   **Didaktischer Effekt**: Schüler sehen, wie die Vorbeschleuniger (PS/SPS) wie „Paketdienste“ arbeiten, die die Teilchen bereits vor-paketieren und im richtigen Abstand in den LHC einspeisen.

### Phase 3: Die Entdeckung der Kollisions-Kreuzung
*   Sobald beide Strahlen rotieren, passiert das visuelle Wunder:
    *   Da die Geschwindigkeiten exakt gleich groß sind ($c$) und die Injektion symmetrisch war, **kreuzen sich die blauen und orangefarbenen Punkte bei jeder Umdrehung exakt in den Detektoren (ATLAS, CMS, ALICE, LHCb)!**
    *   Die Detektoren blitzen im Moment der Kreuzung kurz auf.
*   **Didaktischer Effekt**: Schülern wird sofort klar: *„Ah! Wenn die Abstände nicht absolut gleichmäßig wären, würden die Pakete mitten im Tunnel aneinander vorbeilaufen, anstatt im Detektor zu kollidieren!“*

---

## 3. Implementierungs-Blueprint für den JS-Code

Hier ist der mathematische Ansatz für die Umsetzung im JavaScript-Kernel der `create_notebook.py`:

```javascript
// Didaktische LHC-Konfiguration
const TOTAL_BUCKETS = 12; // Didaktisch reduzierte Anzahl für perfekte Sichtbarkeit
const BUCKET_ANGLES = []; // Array der 12 Winkel: 0, pi/6, 2pi/6, ...
for (let i = 0; i < TOTAL_BUCKETS; i++) {
  BUCKET_ANGLES.push((i * 2 * Math.PI) / TOTAL_BUCKETS);
}

// Detektor-Positionen im LHC-Winkelraum
const DETECTORS = {
  LHCB:  0 * Math.PI,    // 0° (rechts)
  CMS:   0.5 * Math.PI,  // 90° (oben)
  ALICE: 1 * Math.PI,    // 180° (links)
  ATLAS: 1.5 * Math.PI   // 270° (unten)
};

// Zustand der Strahlen (Belegung der 12 Buckets)
let beam1_buckets = new Array(TOTAL_BUCKETS).fill(false); // Uhrzeigersinn (CW)
let beam2_buckets = new Array(TOTAL_BUCKETS).fill(false); // Gegen-Uhrzeigersinn (CCW)

// Funktion zur symmetrischen Injektion eines Bunch-Trains
function injectBunchTrain(beam) {
  // Beispiel: Injiziere 4 gleichmäßig verteilte Pakete
  const train_indices = [0, 3, 6, 9]; 
  train_indices.forEach(idx => {
    if (beam === 1) {
      beam1_buckets[idx] = true;
    } else {
      // Symmetrisch gespiegelt für Beam 2
      beam2_buckets[(TOTAL_BUCKETS - idx) % TOTAL_BUCKETS] = true;
    }
  });
  updateVisualBunches();
}

// In der Render-Schleife (Orbit-Animation):
// Winkel von Beam 1: theta_1 = angle_offset
// Winkel von Beam 2: theta_2 = -angle_offset
// Wenn (theta_1 + d_1) === (theta_2 + d_2) an einer Detektorposition -> KOLLISION!
```

---

## 4. Didaktische Fragestellungen für Schüler im P-Seminar

Mit diesem neuen System können Lehrer und Schüler folgende physikalische Experimente direkt im Jupyter-Notebook durchführen:

1.  **Das Asymmetrie-Experiment**: 
    Was passiert, wenn wir Beam 1 mit 4 Bunches befüllen, Beam 2 aber mit 5 Bunches? 
    *Antwort*: Schüler sehen, dass einer der Bunches keinen Kollisionspartner findet, ungenutzt durch die Detektoren kreist und das Signal-Rausch-Verhältnis verschlechtert.
2.  **Das Phasenverschiebungs-Experiment**: 
    Verschiebe den Injektionszeitpunkt von Beam 2 um einen halben Bucket (Phasenfehler). Wo kollidieren die Teilchen jetzt?
    *Antwort*: Sie kreuzen sich mitten im Tunnel zwischen den Detektoren. Es gibt **keine** Kollisionsdaten in ATLAS/CMS!
