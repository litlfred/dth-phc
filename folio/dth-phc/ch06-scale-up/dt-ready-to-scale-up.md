# Scale-up readiness decision table (sections 6.1 and 6.2, Table 5)

Formal DMN 1.5 decision table (`Decision_ReadyToScaleUp`, `hitPolicy="FIRST"`) encoding the readiness criteria in section 6.1 (*Assess readiness for scale-up*, `sec-029`) and the SMART objective benchmark checks in section 6.2 (*Set SMART objectives for scale-up*, Table 5, `sec-030`), evaluated at gateway `GW_ReadyToScaleUp` in [`scale-up.bpmn`](https://github.com/litlfred/dth-phc/blob/main/processes/scale-up.bpmn).

## Decision structure

Written from the DMN file next to this page.

- **Inputs:**
  - `pcpossReady` (`boolean`): PCPOSS ready?
  - `healthSystemReady` (`boolean`): Health system ready?
  - `objectivesMet` (`boolean`): Objectives met?
- **Outputs:**
  - `outcome` (`"proceed"` | `"not"` | `"unknown"`): Proceed or not
  - `guidance`: Handbook guidance (6.1, 6.2, 6.4)
- **Rules:** 5, hit policy `FIRST`. The last rule returns `"unknown"` when any input has not been answered.
