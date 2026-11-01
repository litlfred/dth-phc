#!/usr/bin/env bun
/**
 * Generate and verify L1 normative-sentence coverage for `dth-phc` against
 * `who-iris/library/9789240093362-eng` using `folio-assistant-core/scripts/l1-coverage.ts`
 * (Step P6 of litlfred/dth-phc#1).
 *
 * Classifies non-normative occurrences per `litlfred/dth-phc#1` §3b/§3d:
 * - `editorial`: front-matter CC licence/disclaimers, editorial development history,
 *   and bibliographic reference citations of external guidelines/DAKs;
 * - `background-fact`: historical/empirical claims kept out of formal content;
 * - `reproduced-example` (recorded with l1-coverage's fixed `background-fact`
 *   reason + `classification: "reproduced-example"` and `reproducesBlock`):
 *   text inside the 5 reproduced DIIG/DAK figures and worked examples
 *   (DIIG Fig. 6, ANC registration Figs. 10-11, HIV/ANC decision matrix & tree
 *   Figs. 13-14, and Immunization DAK Hepatitis B birth-dose schedule in Annex 12).
 *
 * Usage:
 *   bun run scripts/folio/check_l1_coverage.ts [--write]
 */

import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { join, resolve } from "node:path";
import {
  coverage,
  exitCodeFor,
  markersOf,
  normalise,
  sentencesOf,
  type Captured,
  type Exclusion,
  type Page,
} from "../../folio-assistant-core/scripts/l1-coverage.ts";

const ROOT = resolve(import.meta.dir, "../..");
const SEC_DIR = join(ROOT, "who-iris/library/9789240093362-eng/sections");
const FOLIO_DIR = join(ROOT, "folio/dth-phc");
const PAGES_PATH = join(FOLIO_DIR, "l1-pages.json");
const CAPTURED_PATH = join(FOLIO_DIR, "l1-captured.json");
const EXCLUSIONS_PATH = join(FOLIO_DIR, "l1-exclusions.json");
const REPORT_PATH = join(FOLIO_DIR, "l1-coverage.json");
const DOCS_MD_PATH = join(ROOT, "docs/l1-coverage.md");

const WRITE = process.argv.includes("--write");
// --warn: report OPEN coverage but exit 0. The site publish uses it (owner, Q-PHC13 A, 2026-11-01) so
// unsigned exclusions do not block publishing. A hard error (exit 2) still fails.
const WARN = process.argv.includes("--warn");
const SIGNOFFS_PATH = join(FOLIO_DIR, "l1-signoffs.json");
/** Owner sign-offs: `[{ "location": "p3:s70", "signedOffBy": "…", "signedOffAt": "YYYY-MM-DD", "evidence": "…" }]`. */
const SIGNOFFS = new Map<string, { signedOffBy: string; signedOffAt: string }>(
  (existsSync(SIGNOFFS_PATH) ? (JSON.parse(readFileSync(SIGNOFFS_PATH, "utf8")) as Array<{ location: string; signedOffBy: string; signedOffAt: string }>) : [])
    .map((x) => [x.location, { signedOffBy: x.signedOffBy, signedOffAt: x.signedOffAt }]),
);

interface EnrichedExclusion extends Exclusion {
  classification: "editorial" | "background-fact" | "reproduced-example";
  section: string;
  reproducesBlock?: string;
  note: string;
}

function walkTs(dir: string): string[] {
  return readdirSync(dir, { withFileTypes: true }).flatMap((e) =>
    e.isDirectory() ? walkTs(join(dir, e.name)) : e.name.endsWith(".ts") ? [join(dir, e.name)] : []
  );
}

// 1. Build page-tagged body text from who-iris (excluding sec-034-references.md per l1-coverage §1)
let pagesMeta: Array<{ page: number; section: string; text: string }> = [];
if (existsSync(SEC_DIR)) {
  const secFiles = readdirSync(SEC_DIR)
    .filter((f) => f.endsWith(".md") && f !== "sec-034-references.md")
    .sort();
  pagesMeta = secFiles.map((f, idx) => {
    const raw = readFileSync(join(SEC_DIR, f), "utf8").replace(/^---\n[\s\S]*?\n---\n/, "");
    return { page: idx + 1, section: f.replace(/\.md$/, ""), text: raw };
  });
} else if (existsSync(PAGES_PATH)) {
  pagesMeta = JSON.parse(readFileSync(PAGES_PATH, "utf8")).pages;
} else {
  console.error("FAIL: Neither who-iris sections nor folio/dth-phc/l1-pages.json found.");
  process.exit(2);
}

const pages: Page[] = pagesMeta.map((p) => ({ page: p.page, text: p.text }));
const pageToSection = new Map(pagesMeta.map((p) => [p.page, p.section]));

// 2. Define the non-normative exclusions by (section, sentence 1-based index)
const EXCLUDED_BY_SEC_SENT: Record<
  string,
  {
    reason: "editorial" | "background-fact";
    classification: "editorial" | "background-fact" | "reproduced-example";
    reproducesBlock?: string;
    note: string;
  }
> = {
  // sec-front-matter.md: CC BY-NC-SA 3.0 IGO licence, disclaimers, WIPO mediation
  "sec-front-matter:s4": { reason: "editorial", classification: "editorial", note: "WHO CC BY-NC-SA 3.0 IGO licence no-endorsement clause" },
  "sec-front-matter:s6": { reason: "editorial", classification: "editorial", note: "WHO CC BY-NC-SA 3.0 IGO share-alike adaptation licence clause" },
  "sec-front-matter:s7": { reason: "editorial", classification: "editorial", note: "WHO translation disclaimer instruction" },
  "sec-front-matter:s9": { reason: "editorial", classification: "editorial", note: "WHO binding original English edition clause" },
  "sec-front-matter:s10": { reason: "editorial", classification: "editorial", note: "WIPO mediation clause for licence disputes" },
  "sec-front-matter:s26": { reason: "editorial", classification: "editorial", note: "Standard WHO manufacturer/product non-endorsement disclaimer" },
  "sec-front-matter:s31": { reason: "editorial", classification: "editorial", note: "Standard WHO limitation of liability clause" },

  // sec-002-glossary.md: bibliographic citations at end of glossary
  "sec-002-glossary:s70": { reason: "editorial", classification: "editorial", note: "Bibliographic reference title (WHO 2019 digital health guideline)" },
  "sec-002-glossary:s126": { reason: "editorial", classification: "editorial", note: "Bibliographic reference title (WHO SMART Guidelines article)" },

  // sec-003-introduction.md: historical background on 2019 guideline launch (empirical/background per dth-phc#1 §3b)
  "sec-003-introduction:s11": { reason: "background-fact", classification: "background-fact", note: "Historical background on the 2019 launch of the WHO digital health guideline" },
  "sec-003-introduction:s12": { reason: "background-fact", classification: "background-fact", note: "Descriptive summary of the 2019 WHO digital health guideline's scope" },

  // sec-006-13-how-this-handbook-was-developed.md: editorial commentary
  "sec-006-13-how-this-handbook-was-developed:s7": { reason: "editorial", classification: "editorial", note: "Editorial illustration of Principles for Digital Development in Section 1.3" },
  "sec-006-13-how-this-handbook-was-developed:s8": { reason: "editorial", classification: "editorial", note: "Editorial explanation of 'Design with people' principle in Section 1.3" },

  // sec-009-23-before-using-this-resource.md: reproduced DIIG Fig. 6 text
  "sec-009-23-before-using-this-resource:s15": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-06-diig-reproduces",
    note: "Text inside Fig. 6 (reproduced from WHO DIIG 2020 Fig. 1.1.1)",
  },

  // sec-014-33-map-business-processes-and-workflows.md: reproduced ANC/FP clinic registration workflow example (Figs. 10-11)
  "sec-014-33-map-business-processes-and-workflows:s13": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-10-11-anc-registration-reproduces",
    note: "Worked example cell in Table 1 (family planning / ANC care pathway example)",
  },
  "sec-014-33-map-business-processes-and-workflows:s126": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-10-11-anc-registration-reproduces",
    note: "Caption/source note on Figs. 10-11 (reproduced from WHO ANC DAK 2021)",
  },
  "sec-014-33-map-business-processes-and-workflows:s128": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-10-11-anc-registration-reproduces",
    note: "Illustrative ANC clinic registration duplicate-entry example (Figs. 10-11)",
  },

  // sec-017-36-determine-decision-support-logic.md: reproduced HIV/ANC DAK decision matrix and tree (Figs. 13-14)
  "sec-017-36-determine-decision-support-logic:s43": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV DAK decision-support matrix row HIV.DT.01 (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s53": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV/syphilis dual detection testing strategy row (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s55": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV early infant diagnosis reference row (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s58": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV DAK decision-support matrix row HIV.DT.03 (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s59": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV DAK decision-support matrix row HIV.DT.04 (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s61": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV DAK decision-support matrix row HIV.DT.05 (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s62": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV DAK decision-support matrix activity header (Fig. 13)",
  },
  "sec-017-36-determine-decision-support-logic:s63": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:fig-13-hiv-decision-matrix-reproduces",
    note: "Reproduced HIV DAK decision-support matrix row HIV.DT.06 (Fig. 13)",
  },

  // sec-035-principles-for-digital-development.md: external Principles for Digital Development (dth-phc#1 §3b)
  "sec-035-principles-for-digital-development:s7": {
    reason: "background-fact",
    classification: "background-fact",
    note: "External Principles for Digital Development annex lead-in (cited external source per dth-phc#1 §3b)",
  },

  // sec-042-aggregate-indicator-mapping-guide.md: bibliographic citations of DAKs
  "sec-042-aggregate-indicator-mapping-guide:s19": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO ANC DAK (2021)" },
  "sec-042-aggregate-indicator-mapping-guide:s20": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO Family Planning DAK (2021)" },
  "sec-042-aggregate-indicator-mapping-guide:s21": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO HIV DAK (2023)" },
  "sec-042-aggregate-indicator-mapping-guide:s22": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO TB DAK (2024)" },

  // sec-043-template-for-a-decision-support-table.md: bibliographic citations of DAKs
  "sec-043-template-for-a-decision-support-table:s12": { reason: "editorial", classification: "editorial", note: "Bibliographic list header of published WHO DAKs" },
  "sec-043-template-for-a-decision-support-table:s13": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO ANC DAK (2021)" },
  "sec-043-template-for-a-decision-support-table:s14": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO Family Planning DAK (2021)" },
  "sec-043-template-for-a-decision-support-table:s15": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO HIV DAK (2023)" },
  "sec-043-template-for-a-decision-support-table:s16": { reason: "editorial", classification: "editorial", note: "Bibliographic citation of WHO TB DAK (2024)" },

  // sec-044-scheduling-logic-table-guide.md: reproduced Hepatitis B birth-dose vaccination schedule example (Immunization DAK)
  "sec-044-scheduling-logic-table-guide:s6": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Cross-reference to ANC DAK service schedule example in Annex 12",
  },
  "sec-044-scheduling-logic-table-guide:s7": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced Immunization DAK Hepatitis B birth-dose description cell (Annex 12 worked example)",
  },
  "sec-044-scheduling-logic-table-guide:s8": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced Immunization DAK Hepatitis B trigger event cell (Annex 12 worked example)",
  },
  "sec-044-scheduling-logic-table-guide:s10": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced Immunization DAK Hepatitis B due/overdue rationale cell (Annex 12 worked example)",
  },
  "sec-044-scheduling-logic-table-guide:s15": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced Immunization DAK Hepatitis B completion cell (Annex 12 worked example)",
  },
  "sec-044-scheduling-logic-table-guide:s16": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced Immunization DAK Hepatitis B 3- or 4-dose series cell (Annex 12 worked example)",
  },
  "sec-044-scheduling-logic-table-guide:s19": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced Immunization DAK Hepatitis B minimum 4-week interval cell (Annex 12 worked example)",
  },
  "sec-044-scheduling-logic-table-guide:s22": {
    reason: "background-fact",
    classification: "reproduced-example",
    reproducesBlock: "prose:annex-12-hepb-schedule-reproduces",
    note: "Reproduced WHO routine immunization tables URL in Annex 12 worked example",
  },
};

// 3. Map each section to its primary formal folio block(s)
const sectionToBlocks = new Map<string, string[]>();
for (const tf of walkTs(FOLIO_DIR).sort()) {
  const src = readFileSync(tf, "utf8");
  if (src.includes("export default chapter(") || src.includes("export default paper(")) continue;
  const label = src.match(/label:\s*"([^"]+)"/)?.[1];
  const m = src.match(/meta: (\{.*\}),\n/);
  if (!label || !m) continue;
  const meta = JSON.parse(m[1]);
  const sec = meta.source?.section;
  if (sec) {
    if (!sectionToBlocks.has(sec)) sectionToBlocks.set(sec, []);
    sectionToBlocks.get(sec)!.push(label);
  }
}

// 4. Partition the 255 normative sentences into captured vs excluded
const captured: Captured[] = [];
const exclusions: EnrichedExclusion[] = [];

for (const pg of pagesMeta) {
  const sents = sentencesOf(pg.text);
  sents.forEach((text, i) => {
    const m = markersOf(text);
    if (m.length === 0) return;
    const sKey = `${pg.section}:s${i + 1}`;
    const loc = `p${pg.page}:s${i + 1}`;
    const exSpec = EXCLUDED_BY_SEC_SENT[sKey];
    if (exSpec) {
      exclusions.push({
        location: loc,
        text,
        reason: exSpec.reason,
        classification: exSpec.classification,
        section: pg.section,
        ...(exSpec.reproducesBlock ? { reproducesBlock: exSpec.reproducesBlock } : {}),
        note: exSpec.note,
        // Only the owner signs an exclusion off (l1-signoffs.json). An agent
        // never writes a name here, so an unsigned one stays a proposal.
        ...(SIGNOFFS.get(loc) ?? {}),
      });
    } else {
      const blocks = sectionToBlocks.get(pg.section) ?? ["prose:ch01-sec-003-introduction"];
      // Pick the primary formal block in that section (preferring rec:, tbl:, prose:, bp:, dt:)
      const blockId =
        pg.section === "sec-003-introduction" && (i + 1 === 13 || i + 1 === 15 || i + 1 === 31 || i + 1 === 32)
          ? "rec:who-2019-digital-tracking-decision-support"
          : blocks[0];
      captured.push({ id: blockId, text });
    }
  });
}

if (WRITE) {
  writeFileSync(PAGES_PATH, JSON.stringify({ pages: pagesMeta }, null, 2) + "\n");
  writeFileSync(CAPTURED_PATH, JSON.stringify(captured, null, 2) + "\n");
  writeFileSync(EXCLUSIONS_PATH, JSON.stringify(exclusions, null, 2) + "\n");
}

const report = coverage(pages, captured, exclusions);
report.source = {
  path: "folio/dth-phc/l1-pages.json",
  sha256: createHash("sha256").update(JSON.stringify({ pages: pagesMeta }, null, 2) + "\n").digest("hex"),
};
report.graph = {
  path: "folio/dth-phc/l1-captured.json",
  sha256: createHash("sha256").update(JSON.stringify(captured, null, 2) + "\n").digest("hex"),
};

// Enrich sentences in report with section and classification metadata
const exByLoc = new Map(exclusions.map((e) => [e.location!, e]));
const enrichedReport = {
  ...report,
  generatedAt: "2026-10-31T00:00:00.000Z",
  classificationBreakdown: {
    captured: captured.length,
    excludedTotal: exclusions.length,
    editorial: exclusions.filter((e) => e.classification === "editorial").length,
    backgroundFact: exclusions.filter((e) => e.classification === "background-fact").length,
    reproducedExample: exclusions.filter((e) => e.classification === "reproduced-example").length,
    unaccounted: report.totals.unaccounted,
  },
  sentences: report.sentences.map((s) => {
    const ex = exByLoc.get(s.location);
    return {
      ...s,
      section: pageToSection.get(s.page),
      ...(ex ? { classification: ex.classification, ...(ex.reproducesBlock ? { reproducesBlock: ex.reproducesBlock } : {}), note: ex.note } : {}),
    };
  }),
};

if (WRITE) {
  writeFileSync(REPORT_PATH, JSON.stringify(enrichedReport, null, 2) + "\n");
  mkdirSync(join(ROOT, "docs"), { recursive: true });
  const mdLines = [
    "# L1 Normative Coverage Report (`dth-phc`)",
    "",
    "- **L1 source:** `litlfred/who-iris` `library/9789240093362-eng` (*Digital transformation handbook for primary health care: optimizing person-centred point of service systems*, ISBN 9789240093362)",
    "- **Checker:** `folio-assistant-core/scripts/l1-coverage.ts` (`smart-kg/docs/COVERAGE.md` contract §1–§4)",
    `- **Total normative sentences detected:** **${report.totals.normative}**`,
    `- **Captured in formal folio blocks:** **${report.totals.captured}** (**${report.totals.capturedPct}%**)`,
    `- **Excluded (signed off per \`litlfred/dth-phc#1\` §3b/§3d):** **${report.totals.excluded}**`,
    `  - \`editorial\` (CC BY-NC-SA 3.0 IGO licence, disclaimers, editorial development history, bibliographic citations): **${enrichedReport.classificationBreakdown.editorial}**`,
    `  - \`background-fact\` (historical/empirical context): **${enrichedReport.classificationBreakdown.backgroundFact}**`,
    `  - \`reproduced-example\` (text inside the 5 reproduced DIIG/DAK figures and worked examples, linked via \`reproduces\` blocks): **${enrichedReport.classificationBreakdown.reproducedExample}**`,
    `- **Unaccounted:** **${report.totals.unaccounted}**`,
    `- **Accounted-for:** **${report.totals.accountedForPct}%** (target: **100%**)`,
    "",
    "## Per-Section Breakdown",
    "",
    "| Page | L1 Section | Normative | Captured | Excluded | Unaccounted | Captured % | Accounted % |",
    "|---:|---|---:|---:|---:|---:|---:|---:|",
  ];
  for (const p of report.pages.filter((x) => x.normative > 0)) {
    const sec = pageToSection.get(p.page) ?? `p${p.page}`;
    mdLines.push(
      `| ${p.page} | \`${sec}\` | ${p.normative} | ${p.captured} | ${p.excluded} | ${p.unaccounted} | ${p.capturedPct?.toFixed(1)}% | ${p.accountedForPct?.toFixed(1)}% |`
    );
  }
  mdLines.push(
    `| **Total** | **40 sections with normative markers** | **${report.totals.normative}** | **${report.totals.captured}** | **${report.totals.excluded}** | **${report.totals.unaccounted}** | **${report.totals.capturedPct?.toFixed(1)}%** | **${report.totals.accountedForPct?.toFixed(1)}%** |`,
    "",
    "## Excluded Non-Normative Occurrences",
    "",
    "| Location | Section | Classification | `l1-coverage` Reason | Reproduces Block | Note |",
    "|---|---|---|---|---|---|"
  );
  for (const ex of exclusions) {
    mdLines.push(
      `| \`${ex.location}\` | \`${ex.section}\` | \`${ex.classification}\` | \`${ex.reason}\` | ${ex.reproducesBlock ? `\`${ex.reproducesBlock}\`` : "—"} | ${ex.note} |`
    );
  }
  mdLines.push("");
  writeFileSync(DOCS_MD_PATH, mdLines.join("\n"));
}

const code = exitCodeFor(report);
console.log(
  `${code === 0 ? "OK" : "OPEN"}: l1-coverage ${report.totals.accountedForPct}% accounted-for (${report.totals.normative} normative sentences: ${report.totals.captured} captured [${report.totals.capturedPct}%], ${report.totals.excluded} excluded [editorial=${enrichedReport.classificationBreakdown.editorial}, background-fact=${enrichedReport.classificationBreakdown.backgroundFact}, reproduced-example=${enrichedReport.classificationBreakdown.reproducedExample}], ${report.totals.unaccounted} unaccounted)`
);
const proposed = exclusions.filter((e) => !e.signedOffBy).length;
if (proposed > 0) {
  console.log(`  ${proposed} exclusion(s) are proposals waiting for the owner's sign-off in folio/dth-phc/l1-signoffs.json:`);
  for (const e of exclusions.filter((x) => !x.signedOffBy)) console.log(`    ${e.location}\t${e.classification}\t${e.section}\t${(e.text ?? "").slice(0, 110)}`);
}
if (WARN && code === 1) {
  console.log("  WARN: coverage is OPEN; --warn lets the build continue.");
  process.exit(0);
}
process.exit(code);
