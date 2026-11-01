# Data-element minimization decision table (section 3.4.4, Fig. 12)

Formal DMN 1.5 decision table (`Decision_KeepDataElement`, `hitPolicy="FIRST"`) encoding the Fig. 12 decision tree in section 3.4.4 (*Determine which data elements are needed*, `sec-015`), evaluated at gateway `GW_KeepDataElement` in [`understand-user-requirements.bpmn`](../../../processes/understand-user-requirements.bpmn).

## Decision structure

Written from the DMN file next to this page.

- **Inputs:**
  - `duplicated` (`boolean`): Duplicated?
  - `orphaned` (`boolean`): Orphaned?
  - `neededForCareOrIndicator` (`boolean`): Needed for care or for an indicator?
- **Outputs:**
  - `decision` (`"remove"` | `"keep"` | `"unknown"`): Keep or remove
  - `action`: Action to be taken (Fig. 12)
- **Rules:** 6, hit policy `FIRST`. The last rule returns `"unknown"` when any input has not been answered.
