// ═══════════════════════════════════════════════════════════════════════════
// make_qr.mjs — QR-Code für die gehostete Stellwerk-App erzeugen.
//
//   node scripts/make_qr.mjs "<URL>" [basis-pfad]
//
// Beispiel:
//   node scripts/make_qr.mjs "https://example.org/cern/" cern/CERN-Stellwerk-QR
//
// Schreibt <basis>.png UND <basis>.svg (Default-Basis: cern/CERN-Stellwerk-QR).
// Braucht das npm-Paket `qrcode` (devDependency): `npm i -D qrcode`.
// ═══════════════════════════════════════════════════════════════════════════
import { writeFileSync } from "node:fs";

const url = process.argv[2];
const base = process.argv[3] || "cern/CERN-Stellwerk-QR";
if (!url) {
  console.error('Aufruf: node scripts/make_qr.mjs "<URL>" [basis-pfad]');
  process.exit(1);
}

let QR;
try {
  QR = (await import("qrcode")).default;
} catch {
  console.error("Paket `qrcode` fehlt. Bitte einmalig:  npm i -D qrcode");
  process.exit(1);
}

// Fehlerkorrektur „M" (robust gegen Druckknicke/Display-Glanz), großzügiger Rand.
const opts = { errorCorrectionLevel: "M", margin: 2, scale: 12,
  color: { dark: "#0d1117ff", light: "#ffffffff" } };

const png = await QR.toBuffer(url, { ...opts, type: "png" });
writeFileSync(`${base}.png`, png);
const svg = await QR.toString(url, { ...opts, type: "svg" });
writeFileSync(`${base}.svg`, svg);

console.log(`QR erzeugt für ${url}`);
console.log(`  → ${base}.png`);
console.log(`  → ${base}.svg`);
