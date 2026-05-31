# ⚛️ CERN CCC Simulator: Abweichungs-Analyse & Didaktisches Upgrade (CERN_DEVIATIONS.md)

Dieses Dokument vergleicht unsere aktuelle Jupyter-Simulation detailliert mit der echten Kontrollwarte des CERN (CERN Control Centre, CCC) und liefert ein konkretes Konzept für ein didaktisches Upgrade. Ziel ist es, den Schülern die realen Betriebsparameter der LHC-Operatoren zugänglich zu machen.

---

## 1. Abweichungs-Analyse: Simulation vs. Reales CERN

Unsere aktuelle Simulation stellt den Injektionsweg und die Ringgeometrie bereits sehr gut dar. Im Vergleich zum echten LHC-Betrieb fehlen jedoch entscheidende Stellschrauben (Parameter), die Operators im CCC täglich konfigurieren müssen:

| Parameter | Unsere Simulation | Reales CERN (CCC) | Didaktische Abweichung & Auswirkung |
| :--- | :--- | :--- | :--- |
| **Teilchen-Intensität** | Fest (1 Punkt = 1 Bunch) | $1,15 \times 10^{11}$ Protonen pro Bunch | Ohne Intensität gibt es keinen Begriff von **Luminosität** (Kollisionsrate). Höhere Intensität bedeutet schnellere Statistik! |
| **Fokussierungs-Phase (Squeeze $\beta^*$)** | Nicht vorhanden | Reduzierung der Strahlbreite $\beta^*$ an den IPs von $1,5\text{ m}$ auf $30\text{ cm}$ | Nach dem Ramping müssen Quadrupol-Magnete den Strahl extrem stauchen. Ohne "Squeeze" ist die Kollisionswahrscheinlichkeit im echten LHC nahe Null! |
| **Ziel-Energie** | Fest ($6,8\text{ TeV}$) | Variabel ($1,0\text{ TeV}$ bis $7,0\text{ TeV}$ pro Strahl) | Die Entdeckungswahrscheinlichkeit (Wirkungsquerschnitt) schwerer Teilchen (z. B. Higgs) hängt extrem von der Schwerpunktsenergie $\sqrt{s}$ ab. |
| **Kühlsystem & Quench-Risiko** | Nicht vorhanden | Supraleitung bei $1,9\text{ K}$ mit flüssigem Helium | Wenn Magnete zu schnell gerampt werden ($dB/dt$) oder Strahlverluste auftreten, verlieren sie ihre Supraleitfähigkeit (**Quench**). Dies ist das größte Betriebsrisiko des LHC! |
| **Bunch-Abstand (Spacing)** | Fest ($60^\circ$ didaktisch) | $25\text{ ns}$ oder $50\text{ ns}$ | Bestimmt die maximale Anzahl an Packets und das Risiko von parasitären Kollisionen. |

---

## 2. Konzept für das didaktische Kontrollraum-Upgrade

Wir fügen dem Stellwerk ein neues Steuerpanel hinzu: **„📡 CCC OPERATOR TERMINAL“**. Dieses Terminal bietet Schülern interaktive Slider, die direkt an die physikalischen Gesetze gekoppelt sind.

```
+-------------------------------------------------------------------+
|                   📡 CCC OPERATOR PANEL (LHC-v5)                  |
+-------------------------------------------------------------------+
|                                                                   |
|  [ Teilchenart ]    🔵 Protonen        🟣 Blei-Ionen               |
|                                                                   |
|  [ Impuls/Energie ]  [=== Slider: Target Energy ===]  6.8 TeV     |
|                      Bestimmt Magnetfeld B und Kollisions-Physik  |
|                                                                   |
|  [ Intensität ]      [=== Slider: Bunch Intensity ==]  1.15e11 p  |
|                      Direkter Einfluss auf Luminosität & Rauschen |
|                                                                   |
|  [ Squeeze beta* ]   [=== Slider: Beam Focus ======]  30 cm       |
|                      Muss vor Kollision auf < 40cm gepresst werden|
|                                                                   |
|  [ Ramp-Speed ]      [=== Slider: dB/dt ===========]  0.06 T/s    |
|                      Achtung: > 0.12 T/s löst Magnet-Quench aus!  |
|                                                                   |
+-------------------------------------------------------------------+
```

---

## 3. Die physikalischen Formeln hinter den neuen Stellwerten

Jeder Slider im Operator-Terminal verändert die HTML5-Canvas-Kollisionsdarstellung und das Massenspektrum (Histogramm) über exakte physikalische Beziehungen:

### A. Der Squeeze-Faktor ($\beta^*$) und die Luminosität
Die Luminosität $\mathcal{L}$ (Maß für die Kollisionsrate) ist umgekehrt proportional zur Strahlquerschnittsfläche an den Kollisionspunkten, welche durch den Parameter $\beta^*$ (Beta-Star in Metern) bestimmt wird:
$$\mathcal{L} \propto \frac{N_{\text{bunch}}^2 \cdot f_{\text{rev}}}{\beta^*}$$
*   **Didaktische Kopplung**: 
    Wenn der Schüler den **Beam Focus Slider ($\beta^*$)** auf dem Standardwert $1,5\text{ m}$ (unfokussiert) lässt und kollidiert, flasht der Detektor zwar, aber im Massenspektrum erscheinen fast keine Datenpunkte (Luminosität zu gering). 
    Erst wenn er den Strahl auf $\beta^* < 40\text{ cm}$ "squeezed" (zusammenpresst), explodiert die Datenrate, und die Resonanzkurven von Z0 und Higgs zeichnen sich im Histogramm sauber ab!

### B. Das Quench-Risiko ($dB/dt$)
Die supraleitenden Dipolmagnete induzieren bei schneller Stromänderung Wärme. Überschreitet die Ramprate des Magnetfeldes $dB/dt$ ein Limit von $0,10\text{ T/s}$, bricht die Supraleitung zusammen (Quench):
$$\Delta T \propto \left(\frac{dB}{dt}\right)^2 \implies \text{Quench wenn } T > 1,9\text{ K}$$
*   **Didaktische Kopplung (Gamification)**:
    Setzt der Schüler die **Ramping-Geschwindigkeit** zu hoch an ($> 0.10\text{ T/s}$), bricht das Ramping nach 2 Sekunden ab. Eine rote Warnmeldung **"💥 MAGNET QUENCH DETECTED!"** erscheint, die Strahlen werden kontrolliert in den Beam Dump geschossen (Stellwerk-Reset) und das Kühlsystem (Liquid Helium) braucht 5 Sekunden visuelle "Erholungszeit". Die Schüler lernen spielerisch, wie sensibel die kryogenen Systeme des CERN sind!

### C. Kollisionsenergie und Entdeckungshürden ($\sqrt{s}$)
Der Wirkungsquerschnitt $\sigma$ (die Erzeugungswahrscheinlichkeit) für das Higgs-Boson fällt bei geringeren Schwerpunktenergien extrem stark ab:
$$\sigma_{\text{Higgs}}(\sqrt{s}) \propto \ln\left(\frac{\sqrt{s}}{m_H}\right) \cdot (\dots)$$
*   **Didaktische Kopplung**:
    Rampen die Schüler den LHC nur auf eine geringe Energie (z. B. $2\text{ TeV}$ statt $6,8\text{ TeV}$), können sie zwar kollidieren und das leichtere $Z^0$-Boson ($91\text{ GeV}$) problemlos im Histogramm nachweisen. Das schwerere **Higgs-Boson ($125\text{ GeV}$)** wird jedoch im Rauschen untergehen, da seine Erzeugungsrate bei geringer Energie physikalisch gegen Null geht! Sie lernen: Höhere Energien sind zwingend nötig, um schwerere Teilchen zu erschaffen.

---

## 4. Konkreter JS-Implementierungs-Code (Blueprint)

Hier ist das mathematische Grundgerüst, das wir in den JavaScript-Code einbetten können, um diese Parameter miteinander zu verknüpfen:

```javascript
// Neue Operator-Zustände im Dashboard
let paramEnergy = 6.8;      // Target Energy (TeV)
let paramIntensity = 1.15;  // Bunch-Intensität (in 10^11 Protonen)
let paramBetaStar = 1.5;    // Fokussierung (Meter, Startwert 1.5m)
let paramRampSpeed = 0.05;  // Magnetfeld-Änderungsrate dB/dt (T/s)

// Berechnet die tatsächliche Luminosität (Datenrate pro Kollision)
function berechneLuminositaet() {
  if (paramBetaStar > 1.4) return 0.05; // Fast keine Kollisionen
  // Skaliert quadratisch mit Intensität und umgekehrt proportional zu beta*
  let L = (Math.pow(paramIntensity, 2) / paramBetaStar) * 2.5;
  return L; // Faktor für die Anzahl der erzeugten Datenpunkte im Histogramm
}

// Prüft beim Ramping auf Quenches
function checkQuench(currentRampRate) {
  if (currentRampRate > 0.10) {
    triggerQuenchAlarm();
    return true;
  }
  return false;
}
```
