// Fail when a block carries PDF page furniture as narrative: a printed table
// of contents (dot leaders ending in a page number). The site builds its own
// contents from the document structure, and the L1 entry keeps the printed one
// in structure.json, so a printed TOC in a block is always an ingestion error.
// See scripts/folio/seed_from_l1.py clean_front_matter().
import { readdirSync, readFileSync, statSync } from "node:fs";
import { join, relative } from "node:path";

const ROOT = join(import.meta.dir, "..", "..");
const FOLIO = join(ROOT, "folio");
const DOT_LEADER = /(?:\.\s{0,2}){6,}\s*[0-9ivxlc]*\s*$/;
const MAX_LEADER_LINES = 2;

function* walk(dir: string): Generator<string> {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    if (statSync(p).isDirectory()) yield* walk(p);
    else if (name.endsWith(".md")) yield p;
  }
}

const bad: string[] = [];
for (const file of walk(FOLIO)) {
  const lines = readFileSync(file, "utf-8").split("\n");
  const hits = lines.filter((l) => DOT_LEADER.test(l)).length;
  if (hits > MAX_LEADER_LINES) bad.push(`${relative(ROOT, file)}: ${hits} dot-leader lines (a printed table of contents)`);
}
if (bad.length) {
  console.error("✗ page furniture in block narrative:");
  for (const b of bad) console.error(`  ${b}`);
  process.exit(1);
}
console.log("✓ no printed table of contents in any block");
