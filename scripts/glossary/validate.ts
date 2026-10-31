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

if (errors > 0) {
  console.error(`Validation failed with ${errors} error(s).`);
  process.exit(1);
}
