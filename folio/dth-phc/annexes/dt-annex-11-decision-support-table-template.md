# Annex 11: Decision-support table template and DMN 1.5 column mapping

Formal mapping of the handbook's **Annex 11 Decision-support table template** (`sec-043`, section 3.6 `sec-017`) onto `smart-base:DecisionTable` and the OMG DMN 1.5 specification (`omg-2024-dmn-1-5`).

## Column-by-column mapping from Annex 11 to `smart-base:DecisionTable` & DMN 1.5

| Annex 11 Template Field / Column (`sec-043`) | Handbook Rule / Convention | `smart-base:DecisionTable` / DMN 1.5 (`omg-2024-dmn-1-5`) Mapping |
|---|---|---|
| **Decision-support table ID** | Unique identifier of the decision table (e.g. `HIV.DT.01`) | `<decision id="...">` and `label: "dt:<slug>"` |
| **Business process ID** | Identifier of the BPMN workflow containing the decision | Process `id` in `<bpmn:process id="...">` |
| **Activity ID** | Identifier of the BPMN task/gateway invoking the table | Gateway/task `id` with `<cat-harness.processes:decision ref="..."/>` |
| **Decision-support table title** | Human-readable title of the clinical or operational decision | `<decision name="...">` and `title` on `smart-base:DecisionTable` |
| **Description** | Clinical/operational scope and trigger of the decision | `<decision><description>...</description></decision>` |
| **Hit policy (`U`, `R`, `F`)** | `U` = Unique (no overlap, all rules mutually exclusive); `R` = Rule order (overlapping rules return multiple outputs in rule order); `F` = First (first matching rule in top-to-bottom order wins) | `<decisionTable hitPolicy="UNIQUE" \| "RULE ORDER" \| "FIRST">` (formalized in companion [`dt-annex-11-decision-support-table-template.dmn`](dt-annex-11-decision-support-table-template.dmn)) |
| **Rule ID** | Pattern: `<process ID>, <activity number>, DT, <rule number>` | `<rule id="...">` |
| **Inputs (1 … *n*)** | Logical **AND** across input columns within a single row; logical **OR** across separate rows | `<input><inputExpression>` columns and `<inputEntry>` cells (FEEL unary tests; `-` = any value) |
| **Outputs** | Value(s) concluded when all input conditions in the row hold | `<output>` and `<outputEntry>` literal expressions |
| **Action** | Recommended clinical prompt, alert, referral or order presented by the DSS | Secondary `<output name="action">` column |
| **Annotations** | Supporting clinical notes, counselling messages or explanations | `<rule><description>...</description></rule>` or `<annotationEntry>` |
| **Reference / Source** | Citation to the WHO clinical guideline recommendation | `meta.source` / provenance citation on the decision table |

## Decision structure

Written from the DMN file next to this page.

- **Inputs:**
  - `rulesMutuallyExclusive` (`boolean`): All rules are mutually exclusive (no overlap)
  - `multipleOutputsInOrder` (`boolean`): Overlapping rules return multiple outputs in priority order
- **Outputs:**
  - `hitPolicyCode` (`"U"` | `"R"` | `"F"` | `"unknown"`): Annex 11 Hit Policy code
  - `dmnHitPolicy`: DMN 1.5 HitPolicy attribute
- **Rules:** 4, hit policy `FIRST`. The last rule returns `"unknown"` when any input has not been answered.
