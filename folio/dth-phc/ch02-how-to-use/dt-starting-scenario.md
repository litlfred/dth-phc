# Starting-scenario classification decision table (section 2.1)

Formal DMN 1.5 decision table (`Decision_StartingScenario`, `hitPolicy="FIRST"`) derived from section 2.1 (*Assessing the starting scenario*, `sec-007`), evaluated at gateway `GW_StartingScenario` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn).

## Decision structure

- **Inputs:**
  - `anyPcpossInPlace` (`boolean`): Any PCPOSS already in place at the primary health care facility.
  - `comprehensiveAndInteroperable` (`boolean`): Whether existing point-of-service systems are already comprehensive and interoperable.
- **Outputs:**
  - `startingScenario` (`"paper only"` | `"partly digitized"`): Determines whether the implementing team executes the paper-only preparation track (`Task_2_1a_PaperOnlyPreparation`) or the partly-digitized system audit and migration track (`Task_2_1b_PartlyDigitizedAudit`).
  - `entryPreparationTrack` (`"paper-only-baseline-and-literacy"` | `"partly-digitized-system-audit-and-migration"`).
