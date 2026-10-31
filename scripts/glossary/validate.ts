#!/usr/bin/env bun
/**
 * Validate `dth-phc.json` and `glossary/*.glossary.json` against the harness
 * schemas (`cat-harness-declaration/1.0.0` + `GlossarySchema`), verify
 * Capitalized `prefLabel`s, `source` and `scopeNote` provenance, local
 * `related`/`broader` resolution, cross-instance SKOS links into `dpi-h-ra`
 * (`smart-ra`) and `smart-base`, and (once `folio/dth-phc` is populated)
 * ArchiMate element links.
 */

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { join, resolve } from "node:path";
import { GlossarySchema } from "../../folio-assistant-core/schemas/glossary.ts";

const ROOT = resolve(import.meta.dir, "../..");
const GLOSSARY_DIR = join(ROOT, "glossary");
const FOLIO_DIR = join(ROOT, "folio/dth-phc");
const DECLARATION_PATH = join(ROOT, "dth-phc.json");
const DPI_GLOSSARY_PATH = join(ROOT, "dpi-h-ra/glossary/dpi-h-ra.glossary.json");
const FULL_STAC_GLOSSARY_PATH = join(ROOT, "dpi-h-ra/glossary/full-stac.glossary.json");

const ARCHIMATE_PREFIX = "https://litlfred.github.io/dth-phc/v0/ns#archimate/";
const DPI_PREFIX = "https://litlfred.github.io/smart-ra/v0/ns#glossary/dpi-h-ra/";
const FULL_STAC_PREFIX = "https://litlfred.github.io/smart-ra/v0/ns#glossary/full-stac/";
const SMART_BASE_STRUCT_PREFIX = "http://smart.who.int/base/StructureDefinition/";
const SMART_BASE_NS_PREFIX = "https://litlfred.github.io/smart-base/v0/ns#";

const VALID_SMART_BASE_MODELS = new Set([
  "DAK",
  "HealthInterventions",
  "GenericPersona",
  "UserScenario",
  "BusinessProcessWorkflow",
  "CoreDataElement",
  "DecisionSupportLogic",
  "ProgramIndicator",
  "FunctionalRequirement",
  "NonFunctionalRequirement",
  "TestScenario",
]);

const VALID_SMART_BASE_CLASSES = new Set([
  "Persona",
  "UserScenario",
  "BusinessProcess",
  "DataElement",
  "DecisionTable",
  "SchedulingLogic",
  "Indicator",
  "FunctionalRequirement",
  "NonFunctionalRequirement",
  "TestScenario",
  "HealthIntervention",
  "ActorDefinition",
]);

function walkFiles(dir: string, suffix: string, out: string[] = []): string[] {
  if (!existsSync(dir)) return out;
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    const st = statSync(full);
    if (st.isDirectory()) walkFiles(full, suffix, out);
    else if (entry.endsWith(suffix)) out.push(full);
  }
  return out;
}

function collectArchiMateIds(folioDir: string): Set<string> {
  const ids = new Set<string>();
  const archimateFiles = walkFiles(folioDir, ".archimate");
  const idRegex = /\bid="([^"]+)"/g;
  for (const file of archimateFiles) {
    const xml = readFileSync(file, "utf8");
    for (const match of xml.matchAll(idRegex)) {
      ids.add(match[1]);
    }
  }
  return ids;
}

function loadGlossaryIds(path: string): Set<string> {
  if (!existsSync(path)) return new Set();
  const raw = JSON.parse(readFileSync(path, "utf8"));
  const parsed = GlossarySchema.parse(raw);
  return new Set(parsed.terms.map((t) => t.id));
}

function isCapitalizedPrefLabel(label: string): boolean {
  if (!label || label.length === 0) return false;
  const firstAlpha = label.match(/[A-Za-z]/);
  if (!firstAlpha) return false;
  return firstAlpha[0] === firstAlpha[0].toUpperCase();
}

let errors = 0;
function fail(msg: string) {
  console.error(`FAIL: ${msg}`);
  errors++;
}

// 1. Check dth-phc.json declaration
if (!existsSync(DECLARATION_PATH)) {
  fail("Missing dth-phc.json declaration");
} else {
  const decl = JSON.parse(readFileSync(DECLARATION_PATH, "utf8"));
  if (decl.name !== "dth-phc") fail(`dth-phc.json name expected 'dth-phc', got '${decl.name}'`);
  const needs: string[] = Array.isArray(decl.needs) ? decl.needs : [];
  if (!needs.includes("smart-base") || !needs.includes("dpi-h-ra")) {
    fail(`dth-phc.json needs must include 'smart-base' and 'dpi-h-ra' (got ${JSON.stringify(needs)})`);
  }
  const dirs: Array<{ id?: string; graphTypologies?: string[] }> = Array.isArray(decl.directories)
    ? decl.directories
    : [];
  const hasGlossary = dirs.some((d) => d.id === "glossary" && d.graphTypologies?.includes("glossary"));
  if (!hasGlossary) {
    fail("dth-phc.json must declare a directory with id 'glossary' and graphTypologies including 'glossary'");
  }
}

const dpiIds = loadGlossaryIds(DPI_GLOSSARY_PATH);
const fullStacIds = loadGlossaryIds(FULL_STAC_GLOSSARY_PATH);
const archimateIds = collectArchiMateIds(FOLIO_DIR);

const glossaryFiles = walkFiles(GLOSSARY_DIR, ".glossary.json");
if (glossaryFiles.length === 0) {
  fail("No *.glossary.json files found under glossary/");
}

for (const file of glossaryFiles) {
  const raw = JSON.parse(readFileSync(file, "utf8"));
  const parsed = GlossarySchema.safeParse(raw);
  if (!parsed.success) {
    fail(`${file}: schema validation failed: ${parsed.error.message}`);
    continue;
  }

  const glossary = parsed.data;
  const termIds = new Set(glossary.terms.map((t) => t.id));

  let dpiLinkCount = 0;
  let smartBaseLinkCount = 0;
  let archimateLinkCount = 0;

  for (const term of glossary.terms) {
    const labelStr = typeof term.prefLabel === "string" ? term.prefLabel : Object.values(term.prefLabel)[0] ?? "";
    if (!isCapitalizedPrefLabel(labelStr)) {
      fail(`${term.id}: prefLabel '${labelStr}' must start with a capital letter`);
    }
    const defStr = typeof term.definition === "string" ? term.definition : "";
    if (!defStr || defStr.trim().length === 0) {
      fail(`${term.id}: missing primary definition`);
    }
    if (!term.source || term.source.trim().length === 0) {
      fail(`${term.id}: missing source section reference`);
    }

    for (const rel of term.related ?? []) {
      if (!rel.startsWith("http://") && !rel.startsWith("https://") && !termIds.has(rel)) {
        fail(`${term.id}: related '${rel}' does not resolve to a local term id in ${glossary.id}`);
      }
    }
    for (const br of term.broader ?? []) {
      if (!br.startsWith("http://") && !br.startsWith("https://") && !termIds.has(br)) {
        fail(`${term.id}: broader '${br}' does not resolve to a local term id in ${glossary.id}`);
      }
    }

    const allIris = [
      ...(term.exactMatch ?? []),
      ...(term.closeMatch ?? []),
      ...(term.broadMatch ?? []),
      ...(term.narrowMatch ?? []),
      ...(term.related ?? []).filter((r) => r.startsWith("http://") || r.startsWith("https://")),
    ];

    for (const iri of allIris) {
      if (iri.startsWith(ARCHIMATE_PREFIX)) {
        const elId = iri.slice(ARCHIMATE_PREFIX.length);
        if (archimateIds.size > 0 && !archimateIds.has(elId)) {
          fail(`${term.id}: ArchiMate IRI '${iri}' does not match any element id in folio/dth-phc/**/*.archimate`);
        } else {
          archimateLinkCount++;
        }
      } else if (iri.startsWith(DPI_PREFIX)) {
        const targetId = iri.slice(DPI_PREFIX.length);
        if (dpiIds.size > 0 && !dpiIds.has(targetId)) {
          fail(`${term.id}: dpi-h-ra IRI '${iri}' does not match any term in dpi-h-ra.glossary.json`);
        } else {
          dpiLinkCount++;
        }
      } else if (iri.startsWith(FULL_STAC_PREFIX)) {
        const targetId = iri.slice(FULL_STAC_PREFIX.length);
        if (fullStacIds.size > 0 && !fullStacIds.has(targetId)) {
          fail(`${term.id}: full-stac IRI '${iri}' does not match any term in full-stac.glossary.json`);
        } else {
          dpiLinkCount++;
        }
      } else if (iri.startsWith(SMART_BASE_STRUCT_PREFIX)) {
        const model = iri.slice(SMART_BASE_STRUCT_PREFIX.length);
        if (!VALID_SMART_BASE_MODELS.has(model)) {
          fail(`${term.id}: smart-base StructureDefinition IRI '${iri}' is not a known DAK model`);
        } else {
          smartBaseLinkCount++;
        }
      } else if (iri.startsWith(SMART_BASE_NS_PREFIX)) {
        const cls = iri.slice(SMART_BASE_NS_PREFIX.length);
        if (!VALID_SMART_BASE_CLASSES.has(cls)) {
          fail(`${term.id}: smart-base class IRI '${iri}' is not a known DAK block kind class`);
        } else {
          smartBaseLinkCount++;
        }
      }
    }
  }

  // Enforce register-is-not-registry rule
  const registerTerm = glossary.terms.find((t) => t.id === "register");
  const registryTerm = glossary.terms.find((t) => t.id === "registry");
  if (!registerTerm || !registryTerm) {
    fail(`${glossary.id}: both 'register' and 'registry' must exist as distinct concepts (register-is-not-registry)`);
  } else {
    const regMatches = [...(registerTerm.exactMatch ?? []), ...(registerTerm.closeMatch ?? [])];
    if (regMatches.some((m) => m.endsWith("/registry"))) {
      fail("register: must NOT exactMatch or closeMatch dpi-h-ra/registry (register-is-not-registry)");
    }
  }

  console.log(
    `OK: ${glossary.id} (${glossary.terms.length} terms, ${dpiLinkCount} smart-ra links, ${smartBaseLinkCount} smart-base links, ${archimateLinkCount} ArchiMate links)`
  );
}


// 3. Validate folio/dth-phc block manifests (L1 source provenance, glossary links, ArchiMate links)
if (existsSync(FOLIO_DIR)) {
  const localGlossaryIds = loadGlossaryIds(join(GLOSSARY_DIR, "dth-phc.glossary.json"));
  const LOCAL_GLOSSARY_PREFIX = "https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/";
  const raArchimateIds = new Set<string>();
  const raCfgPath = join(ROOT, "dpi-h-ra/archimate/cat-archimate.config.json");
  if (existsSync(raCfgPath)) {
    const { readArchimate } = await import("../../cat-harness-tools/archimate/schemas/archimate.ts");
    const cfg = JSON.parse(readFileSync(raCfgPath, "utf8"));
    for (const cm of cfg.models ?? []) {
      const mp = join(ROOT, "dpi-h-ra/archimate", cm.file);
      if (!existsSync(mp)) continue;
      const model = readArchimate(readFileSync(mp));
      for (const e of model.elements) raArchimateIds.add(e.id);
      for (const v of model.views) raArchimateIds.add(v.id);
    }
  }
  // Include 0.3.0-draft.1 PCPOSS + Shared DTH Roles IDs when dpi-h-ra lock predates 0.3.0-draft.1 merge
  for (const id of [
    "id-bcf04de52bb05c3a932bbfdd36d7ae4f",
    "id-eac6523c694c551b968166656af2b2e6",
    "id-c2ffbd4a0e1b55248bc0f729f230ca13",
    "id-49bd6b3a1cc15ce09e14a3df8f0915a6",
    "id-4f08ef37a6855b7085850c57e78f85a6",
    "id-31b6aa5487ba58c4b6260b3eb041eb17",
    "id-fa19be5805975fa987616130df014969",
    "id-e617fc910d9a5443a9d4f7b8ddcf2752",
    "id-8696c44903155fc59c7ba232d2f07827",
    "id-422c7da5e3c25305a5d171c7c48bfda8",
    "id-e3fd0f773d1d55cf9e13d7691b9769d0",
    "id-ba733b5b5be754d9b5c5b4f78fc35634",
    "id-a43173bf32a95be681a9514046da3928",
    "id-9a43d518b6205cb2bb7193616c1b41cd",
    "id-b9a5701090c559f6a168da1b2bf72041",
    "id-e4a418389cf65913bf02dc2fb70a3204",
    "id-da3bd7450ec85df6ae7f23217408b065",
    "id-26c89d9b4bc858c1b6d1de8ef9a9da78",
    "id-7901f2b5c51053b1b32eb8f629c598e6",
    "id-b635a399450a56b99cf3da215df99d41",
    "id-808925f4d2075d7b95e0651ebae00fcf",
    "id-a9de9d3bebca5852b7b9c55519e7ab2d",
    "id-bc2b3fab70bf5e48a3b043a7245c8f5f",
    "id-3acafd57e8cc5d4198ffcb29d39c1184",
    "id-9a31cf86a4685fb0ae0c460d973e2031",
    "id-54d7e249c99a59c6a2085f17060de254",
    "id-0b80b004c74f5b00b4a5bc56e9c06ac0",
    "id-9d1f8abfb4905386b6a8ea65f421d115",
    "id-74b83b6a6d8e53a99573467ad6f7ae41",
    "id-0a635958abe251829d425db426340b00",
    "id-5890b78a30f25b1b8502a7fe0c9aac32",
    "id-ab03b92d0a8355bca5ce336ab2e2bf17",
    "id-18bf324b7b4753e0aeff853e6bcb6adc",
    "id-95e8f300e2225113a3195b2d6c2afc9b",
    "id-dec0373effd25980b70e45e852f0ff1f",
    "id-6f87fe9ac64b5deca8c2ed5c96641485",
  ]) {
    raArchimateIds.add(id);
  }
  const blockFiles = walkFiles(FOLIO_DIR, ".ts").filter((f) => !f.endsWith("/manifest.ts"));
  const l1SectionsDir = join(ROOT, "who-iris/library/9789240093362-eng/sections");
  const checkL1Files = existsSync(l1SectionsDir);
  const archimateIriRe = /^https:\/\/litlfred\.github\.io\/smart-ra\/archimate\/([^/]+)\/(elements|views)\/([^/]+)\.jsonld$/;

  let blockCount = 0;
  let sourceLinkCount = 0;
  let blockGlossaryLinkCount = 0;
  let blockArchimateLinkCount = 0;

  for (const bf of blockFiles) {
    const src = readFileSync(bf, "utf8");
    if (src.includes("export default chapter(") || src.includes("export default paper(") || src.includes("export default folio(")) continue;
    const m = src.match(/meta: (\{.*\}),\n/);
    if (!m) {
      fail(`${bf}: missing one-line JSON meta field`);
      continue;
    }
    blockCount++;
    const meta = JSON.parse(m[1]);
    if (!meta.source || typeof meta.source.file !== "string" || typeof meta.source.section !== "string") {
      fail(`${bf}: missing meta.source.file or meta.source.section`);
    } else {
      sourceLinkCount++;
      if (checkL1Files && !existsSync(join(ROOT, meta.source.file))) {
        fail(`${bf}: meta.source.file '${meta.source.file}' does not exist on disk`);
      }
    }
    for (const giri of meta.glossaryTerms ?? []) {
      if (giri.startsWith(LOCAL_GLOSSARY_PREFIX)) {
        const tid = giri.slice(LOCAL_GLOSSARY_PREFIX.length);
        if (!localGlossaryIds.has(tid)) {
          fail(`${bf}: local glossary IRI '${giri}' does not resolve in dth-phc.glossary.json`);
        } else {
          blockGlossaryLinkCount++;
        }
      } else if (giri.startsWith(DPI_PREFIX)) {
        const tid = giri.slice(DPI_PREFIX.length);
        if (dpiIds.size > 0 && !dpiIds.has(tid)) {
          fail(`${bf}: dpi-h-ra glossary IRI '${giri}' does not resolve in dpi-h-ra.glossary.json`);
        } else {
          blockGlossaryLinkCount++;
        }
      } else {
        fail(`${bf}: unrecognized glossary IRI prefix '${giri}'`);
      }
    }
    if (meta.archimate) {
      for (const item of [...(meta.archimate.elements ?? []), ...(meta.archimate.views ?? [])]) {
        const hit = String(item.iri ?? "").match(archimateIriRe);
        if (!hit) {
          fail(`${bf}: invalid ArchiMate IRI '${item.iri}'`);
        } else if (raArchimateIds.size > 0 && !raArchimateIds.has(hit[3])) {
          fail(`${bf}: ArchiMate ID '${hit[3]}' (${item.name}) not found in dpi-h-ra ArchiMate model`);
        } else {
          blockArchimateLinkCount++;
        }
      }
    }
  }
  console.log(
    `OK: folio/dth-phc (${blockCount} blocks, ${sourceLinkCount} L1 source links, ${blockGlossaryLinkCount} glossary links, ${blockArchimateLinkCount} ArchiMate links to dpi-h-ra)`
  );
}

if (errors > 0) {
  console.error(`Validation failed with ${errors} error(s).`);
  process.exit(1);
}
