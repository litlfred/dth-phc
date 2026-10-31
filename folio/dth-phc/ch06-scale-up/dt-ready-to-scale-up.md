# Scale-up readiness decision table (sections 6.1 and 6.2, Table 5)

Formal DMN 1.5 decision table (`Decision_ReadyToScaleUp`, `hitPolicy="FIRST"`) encoding the readiness criteria in section 6.1 (*Assess readiness for scale-up*, `sec-029`) and the SMART objective benchmark checks in section 6.2 (*Set SMART objectives for scale-up*, Table 5, `sec-030`), evaluated at gateway `GW_ReadyToScaleUp` in [`scale-up.bpmn`](../../../processes/scale-up.bpmn).

## Decision structure

- **Inputs:**
  - `pcpossReady` (`boolean`): PCPOSS technical, functional and usability readiness verified (6.1).
  - `healthSystemReady` (`boolean`): Health system governance, financing, infrastructure and workforce readiness verified (6.1).
  - `objectivesMet` (`boolean`): SMART objectives and Table 5 benchmark thresholds met during pilot monitoring (6.2, 6.3).
- **Outputs:**
  - `scaleUpDecision` (`"proceed"` | `"not"`): Routes to `Task_6_4_PhaseOutLegacySystems` (`"proceed"`) or `Task_6_3a_RemediateReadinessGaps` (`"not"`).
  - `nextStep`: Actionable remediation or scale-up instruction.
