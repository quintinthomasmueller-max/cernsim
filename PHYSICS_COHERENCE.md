# ⚛️ Physikalische Kohärenz in der CERN-Visualisierung (PHYSICS_COHERENCE.md)

Dieses Dokument analysiert die Diskrepanz zwischen der realen Beschleunigerphysik und der grafischen Darstellung im CERN-Stellwerk und liefert konkrete mathematische Formeln und Implementierungs-Blueprints, um die Simulation **sowohl physikalisch exakt als auch visuell spektakulär** zu gestalten.

---

## 1. Das relativistische Geschwindigkeits-Paradoxon

### Das Problem
Im aktuellen Stellwerk erhöht das Ramping die Umlaufgeschwindigkeit der LHC-Punkte um das **4,6-Fache** (von `0.0015` auf `0.007` rad/ms). 
*   **Physikalische Realität**: Ein Proton hat bei der Injektion ($450\text{ GeV}$) bereits eine Geschwindigkeit von $99,99989\% c$. Bei der Kollisionsenergie ($6,8\text{ TeV}$) beträgt sie $99,999999\% c$. Die physische Geschwindigkeit erhöht sich also nur um **0,0001%**!
*   **Visualisierungs-Dilemma**: Wenn wir die Punkte physikalisch korrekt mit konstanter Geschwindigkeit laufen lassen, sieht der Benutzer keinen Unterschied zwischen Injektion und Kollision.

### Die physikalisch kohärente Lösung
Wir entkoppeln die **Umlaufgeschwindigkeit (Orbit)** von der **Teilchengeschwindigkeit ($v$)** und nutzen stattdessen andere physikalische Effekte zur Visualisierung der Energie:

#### A. Relativistische Frequenzskalierung ($\omega = v/R$)
Die Umlaufzeit $T$ in einem Ring ist durch den Umfang $L = 2\pi R$ und die Geschwindigkeit $v = \beta c$ gegeben. Die Winkelgeschwindigkeit beträgt:
$$\omega = \frac{\beta c}{R}$$

Da die Radien der Ringe im SVG-Layout stark variieren, müssen die Animationsgeschwindigkeiten der Ringe exakt an ihre Geometrie und die physikalischen $\beta$-Werte angepasst werden:

| Stufe | Energie ($E_{\text{kin}}$) | Lorentz $\gamma$ | Rel. Geschwindigkeit $\beta$ | SVG Radius ($R$) | Phys. Winkelgeschwindigkeit $\omega$ (relativ) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PSB (Start)** | $160\text{ MeV}$ | $1,17$ | **$0,520$** | $18\text{ px}$ | $\approx 0,0289$ (langsam, beschleunigend) |
| **PSB (Ende)** | $2\text{ GeV}$ | $3,13$ | **$0,947$** | $18\text{ px}$ | $\approx 0,0526$ (schnell pulsierend) |
| **PS (Start)** | $2\text{ GeV}$ | $3,13$ | **$0,947$** | $38\text{ px}$ | $\approx 0,0249$ |
| **PS (Ende)** | $26\text{ GeV}$ | $28,7$ | **$0,9994$** | $38\text{ px}$ | $\approx 0,0263$ |
| **SPS** | $450\text{ GeV}$ | $480$ | **$0,9999989$** | $65\text{ px}$ | $\approx 0,0153$ |
| **LHC** | $450\text{ GeV} \to 6,8\text{ TeV}$ | $480 \to 7250$ | **$0,9999989 \to 1,0$** | $180\text{ px}$ | $\approx 0,0055$ (konstant!) |

**Implementierung**: Die Punkte im LHC verändern beim Ramping ihre Umlaufgeschwindigkeit fast gar nicht ($\beta \approx 1$). Die kleineren Vorbeschleuniger (PSB, LEIR) hingegen zeigen eine **sichtbare Beschleunigung** der Bunches während ihres kurzen Aufenthalts (von $\beta = 0.52$ auf $0.95$).

---

## 2. Visualisierung der Synchrotronstrahlung

Da die Geschwindigkeit im LHC konstant bleibt, visualisieren wir die Energie über die **Synchrotronstrahlung**. 

### Die Physik
Ein geladenes Teilchen auf einer Kreisbahn strahlt elektromagnetische Energie ab. Die abgestrahlte Leistung $P$ pro Proton ist:
$$P_{\text{synch}} = \frac{e^2 c}{6\pi \epsilon_0 R^2} \gamma^4$$

Die Strahlungsleistung ist proportional zur **vierten Potenz des Lorentz-Faktors ($\gamma^4$)**!
*   Bei Injektion ($450\text{ GeV}$, $\gamma \approx 480$): $P_{\text{synch}} \propto 5,3 \times 10^{10}$ (kaum Strahlung).
*   Bei Kollision ($6,8\text{ TeV}$, $\gamma \approx 7250$): $P_{\text{synch}} \propto 2,76 \times 10^{15}$ (enorm hohe Strahlungsdichte!).
*   Die Leistung steigt um das **52.000-Fache**!

### Die Visualisierung (Vibe Upgrade)
Wir koppeln den CSS-Glow des LHC-Rings und der umlaufenden Bunches an $\gamma^4$ (über eine logarithmische Stauchung, damit der Bildschirm nicht explodiert):

```javascript
// Logarithmische Skalierung für den visuellen Glow-Effekt
let gamma = lhcEnergy / 0.938272; // Protonenmasse
let synchPower = Math.pow(gamma, 4);
let maxSynch = Math.pow(7250, 4);
let intensity = Math.log(synchPower) / Math.log(maxSynch); // Wert zwischen 0.5 und 1.0

// Dynamische CSS-Filtersteuerung
lhcRingSVG.style.filter = `drop-shadow(0 0 ${intensity * 12}px rgba(88,166,255, ${intensity}))`;
lhcRingSVG.style.strokeWidth = `${2.5 + intensity * 2}px`;
```

#### Farbverschiebung (Spektrum)
Mit steigender Energie verschiebt sich das Spektrum der Synchrotronstrahlung von Infrarot/Rot (niedrige Energie) über sichtbares blaues Licht bis hin zu harter Röntgenstrahlung (hochfrequent, violett/weiß).
*   **Start des Rampings**: Sanftes, tiefes Orange-Rot der Dipolmagnete (Aufwärmen).
*   **Zwischenstufe**: Helles Cyan/Blau des Strahls.
*   **Kollisionsbereitschaft**: Gleißendes, fast weißes Violett-Glow, das eine immense Energiedichte signalisiert.

---

## 3. Magnetfeldkopplung ($B \propto p$)

### Die Physik
Die Dipolmagnete müssen ein Magnetfeld $B$ aufbauen, das exakt proportional zum Impuls $p$ der Teilchen ist, um sie auf der Kreisbahn zu halten ($p = q B R$):
$$B = \frac{p}{q R_{\text{bend}}}$$
*   Für Protonen ($q = 1e$) bei $6,8\text{ TeV}$ und einem effektiven Ablenkradius von $R_{\text{bend}} = 2803,95\text{ m}$ ergibt sich:
    $$B = \frac{6800\text{ GeV}}{0,29979 \times 2803,95} \approx 8,1\text{ Tesla}$$
*   Die supraleitenden Magnete werden mit flüssigem Helium auf $1,9\text{ Kelvin}$ gekühlt.

### Die Visualisierung
Wir platzieren kleine, stilisierte Spulen/Rechtecke entlang des LHC-Rings (die 1232 Dipolmagnete).
*   Während des Rampings leuchtet eine **"Kühlanzeige" (Liquid Helium)** in eisigem Cyan auf, während die Magnetsegmente selbst synchron mit der berechneten Tesla-Zahl von einem matten Grau in ein **pulsierendes Elektromagnet-Violett** übergehen.

---

## 4. Blei-Ionen Kinematik ($^{208}\text{Pb}^{82+}$)

### Die Physik
Ein Blei-Ion besteht aus $Z = 82$ Protonen (Ladung $q = 82e$) und $A = 208$ Nukleonen (Masse $m \approx 208\text{ GeV/c}^2$). 
In denselben LHC-Ablenkmagneten ($B_{\text{max}} = 8,33\text{ T}$) ist der maximal erreichbare Impuls pro Nukleon durch das Verhältnis von Ladung zu Masse begrenzt:
$$p_{\text{nucleon}} = \frac{Z}{A} \cdot e \cdot B \cdot R_{\text{bend}} \approx 0,394 \cdot p_{\text{proton}}$$
*   Die maximale Kollisionsenergie für Blei-Ionen beträgt daher ca. $2,56\text{ TeV}$ pro Nukleon (im Vergleich zu $7\text{ TeV}$ bei Protonen).

### Die Visualisierung
*   **Blei-Ionen-Strahl**: Deutlich massivere, dickere Punkte (da ein Bleikern ein riesiges Paket aus 208 Hadronen ist) in Ionen-Pink (`#e377c2`), die sich aufgrund der geringeren Energie pro Nukleon optisch wuchtiger, aber träger anfühlen.
*   **Kollisionsmultiplizität (ALICE)**: 
    Während ATLAS/CMS bei p-p-Kollisionen punktuelle, scharf gebündelte Leptonen-Spuren und vereinzelte Jets zeigen, erzeugt die Pb-Pb-Kollision in ALICE eine **Partikel-Explosion (Quark-Gluon-Plasma)** mit extrem hoher Spurdichte (hohe Multiplizität). Das Canvas-Event-Display muss hier ein regelrechtes Feuerwerk aus Hunderten feinen, rosafarbenen Spuren zeichnen, um das Aufschmelzen der Hadronen visuell korrekt darzustellen.
