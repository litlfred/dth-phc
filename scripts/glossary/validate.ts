#!/usr/bin/env bun
/**
 * Validate `dth-phc.json`, `glossary/*.glossary.json`, and all 123 blocks in
 * `folio/dth-phc` (Step P6 of litlfred/dth-phc#1):
 *
 * - `dth-phc.json` declaration (`needs: ["smart-base", "dpi-h-ra"]`, `glossary`,
 *   `processes`, `decisions`, `folio`);
 * - `glossary/dth-phc.glossary.json` against `GlossarySchema`, Capitalized
 *   `prefLabel`s, `source` and `scopeNote` provenance, local `related`/`broader`
 *   resolution, and cross-instance SKOS links into `dpi-h-ra` (`smart-ra`) and
 *   `smart-base`;
 * - every block in `folio/dth-phc` is registered in `folio/dth-phc/dth-phc.ts`'s
 *   9 chapters with zero duplicate block labels;
 * - every block's `meta.source.file` and `meta.source.section` resolve against
 *   `who-iris/library/9789240093362-eng/sections/`;
 * - every `meta.glossaryTerms` IRI resolves in `dth-phc.glossary.json` or
 *   `dpi-h-ra.glossary.json`;
 * - every `meta.archimate` element and view IRI (`check:archimate-links`)
 *   resolves in the mounted `dpi-h-ra` ArchiMate model (`0.3.0-draft.2`);
 * - swimlane-to-persona check: every `persona` block (19) links to its BPMN
 *   lanes (`meta.bpmnLanes`), ArchiMate elements (`meta.archimate.elements`),
 *   and glossary terms (`meta.glossaryTerms`), and every `<bpmn:lane>` in all
 *   5 BPMN processes binds `partitionElementRef` to a declared `persona` block
 *   and `<bpmn:resource>`;
 * - every `business-process` block (5) passes `dak-companion-present` and
 *   `dak-bpmn-has-process` and has rendered SVGs in `processes/` and
 *   `folio/dth-phc/media/`;
 * - every `decision-table` block (5) passes `dak-companion-present` and
 *   `dak-dmn-has-decision-table`, and loads via `loadDecisionTable` with zero
 *   `unreadableExpressions`.
 */

import { existsSync, readdirSync, readFileSync, statSync } from "node:fs";
import { dirname, join, resolve } from "node:path";
import { GlossarySchema } from "../../folio-assistant-core/schemas/glossary.ts";
import {
  checkDakBpmnHasProcess,
  checkDakCompanionPresent,
  checkDakDmnHasDecisionTable,
} from "../../smart-base/pipeline/qa-checkers-dak.ts";
import {
  loadDecisionTable,
  unreadableExpressions,
} from "../../cat-harness-tools/src/workflow/decision-table.ts";

const ROOT = resolve(import.meta.dir, "../..");
const GLOSSARY_DIR = join(ROOT, "glossary");
const FOLIO_DIR = join(ROOT, "folio/dth-phc");
const DECLARATION_PATH = join(ROOT, "dth-phc.json");
const DPI_GLOSSARY_PATH = join(ROOT, "dpi-h-ra/glossary/dpi-h-ra.glossary.json");
const FULL_STAC_GLOSSARY_PATH = join(ROOT, "dpi-h-ra/glossary/full-stac.glossary.json");

const ARCHIMATE_PREFIX = "https://litlfred.github.io/dth-phc/v0/ns#archimate/";
const DPI_PREFIX = "https://litlfred.github.io/smart-ra/v0/ns#glossary/dpi-h-ra/";
const FULL_STAC_PREFIX = "https://litlfred.github.io/smart-ra/v0/ns#glossary/full-stac/";
const LOCAL_GLOSSARY_PREFIX = "https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/";
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
    fail(`${file}: failed GlossarySchema validation:\n${parsed.error.message}`);
    continue;
  }

  const g = parsed.data;
  const schemePrefix = `https://litlfred.github.io/dth-phc/v0/ns#glossary/${g.id}/`;
  const localIds = new Set(g.terms.map((t) => t.id));
  const localIris = new Set(g.terms.map((t) => `${schemePrefix}${t.id}`));

  let exactCount = 0;
  let closeCount = 0;
  let broadCount = 0;
  let narrowCount = 0;

  for (const term of g.terms) {
    if (!isCapitalizedPrefLabel(term.prefLabel)) {
      fail(`${g.id}/${term.id}: prefLabel '${term.prefLabel}' must start with a capital letter`);
    }
    if (!term.source || term.source.trim().length === 0) {
      fail(`${g.id}/${term.id}: missing 'source' citation`);
    }
    if (!term.scopeNote || term.scopeNote.trim().length === 0) {
      fail(`${g.id}/${term.id}: missing 'scopeNote' provenance`);
    }

    for (const rel of [...(term.related ?? []), ...(term.broader ?? [])]) {
      if (rel.startsWith(schemePrefix)) {
        if (!localIris.has(rel)) {
          fail(`${g.id}/${term.id}: unresolved local glossary IRI '${rel}'`);
        }
      } else if (!localIds.has(rel) && !rel.startsWith("http://") && !rel.startsWith("https://")) {
        fail(`${g.id}/${term.id}: unresolved local term id '${rel}'`);
      }
    }

    const matchLists: Array<[string, string[] | undefined]> = [
      ["exactMatch", term.exactMatch],
      ["closeMatch", term.closeMatch],
      ["broadMatch", term.broadMatch],
      ["narrowMatch", term.narrowMatch],
    ];

    for (const [kind, list] of matchLists) {
      for (const iri of list ?? []) {
        if (kind === "exactMatch") exactCount++;
        if (kind === "closeMatch") closeCount++;
        if (kind === "broadMatch") broadCount++;
        if (kind === "narrowMatch") narrowCount++;

        if (iri.startsWith(DPI_PREFIX)) {
          const targetId = iri.slice(DPI_PREFIX.length);
          if (dpiIds.size > 0 && !dpiIds.has(targetId)) {
            fail(`${g.id}/${term.id}: ${kind} '${iri}' not found in dpi-h-ra.glossary.json`);
          }
        } else if (iri.startsWith(FULL_STAC_PREFIX)) {
          const targetId = iri.slice(FULL_STAC_PREFIX.length);
          if (fullStacIds.size > 0 && !fullStacIds.has(targetId)) {
            fail(`${g.id}/${term.id}: ${kind} '${iri}' not found in full-stac.glossary.json`);
          }
        } else if (iri.startsWith(SMART_BASE_STRUCT_PREFIX)) {
          const modelId = iri.slice(SMART_BASE_STRUCT_PREFIX.length);
          if (!VALID_SMART_BASE_MODELS.has(modelId)) {
            fail(`${g.id}/${term.id}: ${kind} '${iri}' is not a known smart-base logical model`);
          }
        } else if (iri.startsWith(SMART_BASE_NS_PREFIX)) {
          const cls = iri.slice(SMART_BASE_NS_PREFIX.length);
          if (!VALID_SMART_BASE_CLASSES.has(cls)) {
            fail(`${g.id}/${term.id}: ${kind} '${iri}' is not a known smart-base DAK class`);
          }
        } else if (iri.startsWith(ARCHIMATE_PREFIX)) {
          const archId = iri.slice(ARCHIMATE_PREFIX.length);
          if (archimateIds.size > 0 && !archimateIds.has(archId)) {
            fail(`${g.id}/${term.id}: ${kind} ArchiMate id '${archId}' not found in ${FOLIO_DIR}`);
          }
        }
      }
    }
  }

  console.log(
    `OK: ${g.id} (${g.terms.length} terms; exactMatch=${exactCount}, closeMatch=${closeCount}, broadMatch=${broadCount}, narrowMatch=${narrowCount})`
  );
}

// 2. Validate folio/dth-phc blocks, ArchiMate links, personas/lanes, BPMN, DMN
if (existsSync(FOLIO_DIR)) {
  const localGlossaryIds = loadGlossaryIds(join(GLOSSARY_DIR, "dth-phc.glossary.json"));
  const raArchimatePath = join(ROOT, "dpi-h-ra/archimate/cat-archimate.config.json");
  const raArchimateByModel = new Map<string, Set<string>>();
  if (existsSync(raArchimatePath)) {
    const { readArchimate } = await import("../../cat-harness-tools/archimate/schemas/archimate.ts");
    const cfg = JSON.parse(readFileSync(raArchimatePath, "utf8"));
    for (const cm of cfg.models ?? []) {
      const p = join(ROOT, "dpi-h-ra/archimate", cm.file);
      if (!existsSync(p)) continue;
      const model = readArchimate(readFileSync(p));
      const ids = new Set<string>();
      for (const e of model.elements) ids.add(e.id);
      for (const v of model.views) ids.add(v.id);
      raArchimateByModel.set(cm.id, ids);
    }
  }

  const allTsFiles = walkFiles(FOLIO_DIR, ".ts").filter((f) => !f.endsWith("/manifest.ts"));
  const l1SectionsDir = join(ROOT, "who-iris/library/9789240093362-eng/sections");
  const checkL1Files = existsSync(l1SectionsDir);
  const archimateIriRe = /^https:\/\/litlfred\.github\.io\/smart-ra\/archimate\/([^/]+)\/(elements|views)\/([^/]+)\.jsonld$/;

  let blockCount = 0;
  let sourceLinkCount = 0;
  let blockGlossaryLinkCount = 0;
  let blockArchimateLinkCount = 0;
  let archimateBlockCount = 0;
  let reproducesCount = 0;
  const blockLabels = new Map<string, string>();
  const personaRoleIds = new Map<string, string>();
  let personaCount = 0;

  for (const bf of allTsFiles) {
    const src = readFileSync(bf, "utf8");
    if (src.includes("export default chapter(") || src.includes("export default paper(") || src.includes("export default folio(")) continue;

    const labelMatch = src.match(/label:\s*"([^"]+)"/);
    const label = labelMatch?.[1];
    if (!label) {
      fail(`${bf}: missing block label`);
    } else if (blockLabels.has(label)) {
      fail(`${bf}: duplicate block label '${label}' (already in ${blockLabels.get(label)})`);
    } else {
      blockLabels.set(label, bf);
    }

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
      archimateBlockCount++;
      for (const item of [...(meta.archimate.elements ?? []), ...(meta.archimate.views ?? [])]) {
        const hit = String(item.iri ?? "").match(archimateIriRe);
        if (!hit) {
          fail(`${bf}: invalid ArchiMate IRI '${item.iri}'`);
        } else if (raArchimateByModel.has(hit[1]) && !raArchimateByModel.get(hit[1])!.has(hit[3])) {
          fail(`${bf}: ArchiMate ID '${hit[3]}' (${item.name}) not found in dpi-h-ra ArchiMate model`);
        } else {
          blockArchimateLinkCount++;
        }
      }
    }
    if (meta.reproduces) {
      reproducesCount++;
      if (!meta.reproduces.upstreamDocument && !meta.reproduces.source && !meta.reproduces.example) {
        fail(`${bf}: reproduces block missing upstreamDocument or upstreamComponent`);
      }
    }

    if (src.includes("export default persona(")) {
      personaCount++;
      if (!meta.roleId || !meta.bpmnRoleId || !Array.isArray(meta.bpmnLanes) || meta.bpmnLanes.length === 0) {
        fail(`${bf}: persona is missing roleId, bpmnRoleId, or bpmnLanes`);
      } else {
        personaRoleIds.set(meta.bpmnRoleId, label ?? bf);
      }
      if (!Array.isArray(meta.archimate?.elements) || meta.archimate.elements.length === 0) {
        fail(`${bf}: persona is missing meta.archimate.elements`);
      }
      if (!Array.isArray(meta.glossaryTerms) || meta.glossaryTerms.length === 0) {
        fail(`${bf}: persona is missing meta.glossaryTerms`);
      }
      for (const lane of meta.bpmnLanes ?? []) {
        const bpmnRel = typeof lane === "string" ? lane.split("#")[0] : lane.bpmnFile;
        const laneId = typeof lane === "string" ? lane.split("#")[1] : lane.laneId;
        const bpmnFull = join(ROOT, bpmnRel);
        if (!existsSync(bpmnFull)) {
          fail(`${bf}: bpmnFile '${bpmnRel}' does not exist`);
          continue;
        }
        const bpmnXml = readFileSync(bpmnFull, "utf8");
        if (!bpmnXml.includes(`id="${laneId}"`)) {
          fail(`${bf}: lane '${laneId}' not found in ${bpmnRel}`);
        }
        if (!bpmnXml.includes(`<bpmn:resource id="${meta.bpmnRoleId}"`)) {
          fail(`${bf}: <bpmn:resource id="${meta.bpmnRoleId}"> not declared in ${bpmnRel}`);
        }
      }
    }
  }

  let bpCount = 0;
  let laneCount = 0;
  let dtCount = 0;
  let dtRuleCount = 0;

  for (const bf of allTsFiles) {
    const src = readFileSync(bf, "utf8");
    if (src.includes("export default businessProcess(")) {
      bpCount++;
      const bpmnPath = bf.replace(/\.ts$/, ".bpmn");
      const c1 = checkDakCompanionPresent({ ts: bf, bpmn: existsSync(bpmnPath) ? bpmnPath : undefined });
      const c2 = checkDakBpmnHasProcess({ ts: bf, bpmn: existsSync(bpmnPath) ? bpmnPath : undefined });
      for (const [cid, c] of [["dak-companion-present", c1], ["dak-bpmn-has-process", c2]] as const) {
        if (c.result !== "pass") {
          fail(`${bf} (${cid}): ${JSON.stringify(c.hits)}`);
        }
      }
      const bpmnXml = readFileSync(bpmnPath, "utf8");
      const lanes = [...bpmnXml.matchAll(/<bpmn:lane\s+([^>]+)>/g)];
      if (lanes.length === 0) {
        fail(`${bpmnPath}: has no <bpmn:lane> elements`);
      }
      for (const l of lanes) {
        laneCount++;
        const roleRef = l[1].match(/partitionElementRef="([^"]+)"/)?.[1];
        if (!roleRef || !personaRoleIds.has(roleRef)) {
          fail(`${bpmnPath}: lane missing partitionElementRef or persona role "${roleRef}" not declared among persona blocks`);
        }
      }
      const m = src.match(/meta: (\{.*\}),\n/);
      const meta = m ? JSON.parse(m[1]) : {};
      const mediaSvg = meta.svgFile ? join(FOLIO_DIR, meta.svgFile) : "";
      const canonSvg = meta.canonicalSvg ? join(ROOT, meta.canonicalSvg) : "";
      if (!mediaSvg || !existsSync(mediaSvg)) {
        fail(`${bf}: media SVG '${mediaSvg}' is missing`);
      }
      if (!canonSvg || !existsSync(canonSvg)) {
        fail(`${bf}: canonical SVG '${canonSvg}' is missing`);
      }
    }

    if (src.includes("export default decisionTable(")) {
      dtCount++;
      const dmnPath = bf.replace(/\.ts$/, ".dmn");
      const c1 = checkDakCompanionPresent({ ts: bf, dmn: existsSync(dmnPath) ? dmnPath : undefined });
      const c2 = checkDakDmnHasDecisionTable({ ts: bf, dmn: existsSync(dmnPath) ? dmnPath : undefined });
      for (const [cid, c] of [["dak-companion-present", c1], ["dak-dmn-has-decision-table", c2]] as const) {
        if (c.result !== "pass") {
          fail(`${bf} (${cid}): ${JSON.stringify(c.hits)}`);
        }
      }
      // The platform wants two copies: the companion next to the block (smart-base)
      // and processes/decisions/ for BPMN gateway refs (cat-harness kg-audit).
      // Until one copy can serve both, they must stay byte-identical (dth-phc#1 R3).
      const dtMeta = JSON.parse(src.match(/meta: (\{.*\}),\n/)?.[1] ?? "{}");
      if (dtMeta.canonicalDmn && existsSync(dmnPath)) {
        const canon = join(ROOT, dtMeta.canonicalDmn);
        if (!existsSync(canon)) {
          fail(`${bf}: canonicalDmn '${dtMeta.canonicalDmn}' is missing`);
        } else if (readFileSync(canon, "utf8") !== readFileSync(dmnPath, "utf8")) {
          fail(`${dmnPath}: differs from canonicalDmn '${dtMeta.canonicalDmn}'; copy one over the other`);
        }
      }
      const decisionId = src.match(/decisionId:\s*"([^"]+)"/)?.[1];
      if (!decisionId) {
        fail(`${bf}: missing top-level decisionId`);
      } else {
        try {
          const table = await loadDecisionTable(dmnPath, decisionId);
          dtRuleCount += table.rules.length;
          const unreadable = unreadableExpressions(table);
          if (unreadable.length > 0) {
            fail(`${dmnPath}: ${unreadable.length} unreadable FEEL expression(s): ${JSON.stringify(unreadable)}`);
          }
        } catch (e) {
          fail(`${dmnPath}: failed to load decision table: ${e}`);
        }
      }
    }
  }

  console.log(
    `OK: folio/dth-phc (${blockCount} blocks, ${sourceLinkCount} L1 source links, ${blockGlossaryLinkCount} glossary links, ${blockArchimateLinkCount} ArchiMate links across ${archimateBlockCount} blocks to dpi-h-ra)`
  );
  console.log(
    `OK: structured DTH content (${personaCount} personas, ${bpCount} BPMN processes with ${laneCount} role-bound swimlanes, ${dtCount} DMN decision tables with ${dtRuleCount} FEEL rules, ${reproducesCount} reproduces links)`
  );
}

if (errors > 0) {
  console.error(`Validation failed with ${errors} error(s).`);
  process.exit(1);
}
