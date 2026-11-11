# Wiring a DTH to smart-ra (L2 pilot)

dth-hrh is the pilot for Digital Transformation Handbooks that depend on
[smart-ra](https://github.com/litlfred/smart-ra) (owner decision 2026-10-31,
option A; dth-hrh#47). dth-phc, dth-sc, dth-pc and dth-sfp copy these steps.
The general skill for this is smart-base's `dth-l1-to-l2-ingest`
(smart-base#249); this page is the worked example it can point to.

## 1. Mount smart-ra, two directories only

smart-ra's instance is named **`dpi-h-ra`**, not smart-ra. Mount only its
`glossary` and `archimate` directories, and skip the layers it shares with
the DTH, so the DTH's own pins win:

```sh
echo "<where the owner said yes>" | bun run cat mount:remote \
  --seed dpi-h-ra=litlfred/smart-ra@<40-char sha> --consent-by <owner>
bun run cat mount:remote --choose dpi-h-ra --directories glossary,archimate
```

Then, in `index.config.json`, add `"<layer>": { "skip": true }` under the
`dpi-h-ra` entry's `overrides` for every layer the DTH already mounts
(who-iris, smart-base, fhir-harness, folio-assistant-core, cat-harness,
cat-harness-tools, bootstrap, bootstrap-tools). Without the skips the plan
mounts nothing. Then `bun run cat mount:remote` writes `index.lock.json`, and
`dpi-h-ra/` is gitignored.

## 2. Declare the dependency

In `<dth>.json`, `needs` becomes `["smart-base", "dpi-h-ra"]`. Keep
smart-base: the DAK block kinds (persona, user scenario, requirements, data
elements) reach a DTH through smart-base's `content-adapters/dak.json`.

## 3. Glossary links

A DTH term links to a smart-ra concept with a SKOS match on the term in the
DTH's consolidated scheme, never by copying a definition:

```json
"broadMatch": ["https://litlfred.github.io/smart-ra/v0/ns/glossary/dpi-h-ra/registry"]
```

The namespace is `instanceNs` of the mounted declaration. Use `broadMatch`
when the smart-ra concept is wider (the RA's Registry covers facility,
product and workforce registries), `exactMatch` only when both definitions
are adopted and the same. Both sides are still candidates, so a match is a
proposal for the working group. If the scheme is generated (dth-hrh's
`build_glossary.py`), the generator must keep the matches on a re-run.

## 4. ArchiMate links

A narrative or requirement block that names an architecture element carries
the element's IRI in its manifest's `meta.archimate`:

```json
"archimate": {
  "model": "smart-ra 0.2.0",
  "basis": "agent-proposed by name, for working-group review (dth-hrh#47)",
  "elements": [{ "iri": "https://litlfred.github.io/smart-ra/archimate/0.2.0/elements/id-….jsonld", "name": "…" }],
  "views": [{ "iri": "https://litlfred.github.io/smart-ra/archimate/0.2.0/views/id-….jsonld", "name": "…" }]
}
```

IRIs use Archi's own ids, which stay stable across model versions. Then
`bun run kg:blocks` so the block JSON-LD carries the links.

## 5. Check

`bun run check:dth-glossary` checks the glossary schema, every `related`
link, every SKOS match into dpi-h-ra, and every `meta.archimate` IRI against
the mounted model. This is a stopgap in the DTH repo; the general checks are
smart-base#242 (cross-instance glossary validator, ArchiMate-link check).

## Not part of the wiring

BPMN per business process, persona links to lanes and roles, and DMN tables
(dth-hrh#47, structured content) wait for the structured-authoring work
(smart-base#244, #246 and the step-table schema in smart-base#242).
The folio's `level` stays `L1` until the L2 DTH document kind exists
(smart-base#242).

## 6. `dth-phc` L2 Verification Summary (`litlfred/dth-phc#1` Step P6)

| Check / Artefact | Command | Verified Result |
|---|---|---|
| **Glossary & SKOS matches** | `bun run check:dth-glossary` | `111` terms (`exactMatch=34`, `closeMatch=110`, `broadMatch=16`, `narrowMatch=4`), 0 unlinked terms |
| **Folio blocks & ArchiMate wiring** | `bun run check:archimate-links` | `123` blocks across 9 chapters (`88` narrative/table/figure/checklist blocks + `35` structured P4b blocks), `123` L1 source links (`9789240093362-eng`), `689` glossary links, `692` ArchiMate links across `119` blocks (`smart-ra 0.3.0-draft.1`, including `id-view-pcposs-phc-001`) |
| **Structured DTH content (`dak-*`)** | `bun run check:dth-glossary` | `19` `persona` blocks (`PHC-R-01`..`PHC-R-19`), `5` `business-process` BPMN 2.0 workflows (`PHC-BP-01`..`PHC-BP-05`) with `24` role-bound swimlanes, `5` `decision-table` DMN 1.5 tables (`PHC-DT-01`..`PHC-DT-05`) with `19` FEEL rules (`dak-dmn-has-decision-table`), `1` `scheduling-logic` block (`PHC-SCHED-01`), `13` `reproduces` links |
| **Block JSON-LD companions** | `bun run check:kg-blocks` | `123` `.jsonld` companions up to date |
| **L1 normative sentence coverage** | `bun run check:l1-coverage` | **100.00 % accounted-for** across `255` normative sentences (`213` captured `[83.53%]`, `42` excluded with rationale `[16.47%]`, `0` unaccounted) — report in [`docs/l1-coverage.md`](l1-coverage.md) and [`folio/dth-phc/l1-coverage.json`](../folio/dth-phc/l1-coverage.json) |
| **Document site build** | `bun run site:document <out>` | Renders `en/dth-phc/index.html` (`123` blocks) cleanly |
