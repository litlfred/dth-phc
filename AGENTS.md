# AGENTS.md — dth-phc

This repository is the **L2 document folio** for the WHO *Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems* (Geneva: World Health Organization; 2024; ISBN 978-92-4-009336-2; IRIS handle [`10665/379452`](https://iris.who.int/handle/10665/379452)).

## Instance graph and dependencies

`dth-phc.json` declares `needs: ["smart-base", "dpi-h-ra"]`:

- **`smart-base`** provides the DAK artefact schemas (`dak-artifacts`), block kinds (`Persona`, `UserScenario`, `BusinessProcess`, `DataElement`, `DecisionTable`, `SchedulingLogic`, `Indicator`, `FunctionalRequirement`, `NonFunctionalRequirement`, `TestScenario`, `HealthIntervention`, `ActorDefinition`), and DTH authoring skills (`dth-authoring`, `dth-l1-to-l2-ingest`, `dth-archimate-patterns`, `dth-workplan`).
- **`dpi-h-ra`** (`litlfred/smart-ra`) provides the WHO/ITU DPI-H Reference Architecture glossary (`dpi-h-ra` and `full-stac` concept schemes), ArchiMate business/application/technology building blocks, and HIE/POS reference patterns.
- **`who-iris`** is mounted whole via `index.config.json` and supplies the normalized L1 source at `who-iris/library/9789240093362-eng/` (plus the cross-referenced Annex 1 sources `9789240081888-eng` Core Clinical Data Guide and `9789240020306-eng` Digital Adaptation Kits).

See [`docs/l2-wiring.md`](docs/l2-wiring.md) for the S4 repo wiring contract and [`litlfred/dth-phc#1`](https://github.com/litlfred/dth-phc/issues/1) for the approved workplan.

## Key rules for this folio

1. **Mount before validating:** Run `bun run cat-harness-tools/scripts/remote-mount.ts` (or `.claude/hooks/session-start.sh`) to materialize mounted upstream instances on disk before running checks or site generators.
2. **Glossary discipline (`glossary/dth-phc.glossary.json`):**
   - Every term must carry a Capitalized `prefLabel`, a verbatim definition from `who-iris/library/9789240093362-eng/sections/sec-002-glossary.md` (or `sec-001-abbreviations.md`), and a `candidate` entry citing the L1 section.
   - Keep **`Register`** (`register`, PHC longitudinal tracking log of a cohort) distinct from **`Registry`** (`registry`, `exactMatch` `dpi-h-ra/registry`, HIE/Infrastructure master index) — rule `register-is-not-registry`.
   - Validate with `bun run check:dth-glossary`.
3. **L1 source fidelity:** Cite `who-iris/library/9789240093362-eng/sections/sec-*.md` in block provenance and glossary candidates; do not invent narrative prose or re-ingest PDFs into this repo.
