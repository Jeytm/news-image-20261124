// Entry point: copies the poster (entry.png) to /output/entry.png.
// Deterministic: no network, no clock, no randomness. The image is
// pre-rendered by render.py (1024x1024 PNG, 423,509 bytes).
import { createHash } from "node:crypto";
import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
const outDir = "/output";
const out = join(outDir, "entry.png");

const MAX_BYTES = 1024 * 1024; // 1 MiB cap from the brief

if (!existsSync(src)) {
  throw new Error(`missing entry.png next to main.ts (${src})`);
}

const buf = readFileSync(src);

// Validate PNG magic bytes (89 50 4E 47 0D 0A 1A 0A).
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);
if (!buf.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error("entry.png is not a valid PNG (bad magic bytes)");
}

if (buf.length > MAX_BYTES) {
  throw new Error(`entry.png is ${buf.length} bytes, over the 1 MiB cap`);
}

mkdirSync(outDir, { recursive: true });
copyFileSync(src, out);

const written = statSync(out);
if (written.size !== buf.length) {
  throw new Error(`copy mismatch: wrote ${written.size} bytes, expected ${buf.length}`);
}

// Verify the copy is byte-identical by comparing SHA-256 hashes.
const hash = (p: string) =>
  createHash("sha256").update(readFileSync(p)).digest("hex");
if (hash(src) !== hash(out)) {
  throw new Error("output hash does not match entry.png");
}

console.log(`wrote ${out} (${written.size} bytes, sha256 ${hash(out)})`);
