# Starting-scenario classification decision table (section 2.1)

Formal DMN 1.5 decision table (`Decision_StartingScenario`, `hitPolicy="FIRST"`) derived from section 2.1 (*Assessing the starting scenario*, `sec-007`), evaluated at gateway `GW_StartingScenario` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn).

## Decision structure

Written from the DMN file next to this page.

- **Inputs:**
  - `anyPcpossInPlace` (`boolean`): Any PCPOSS in place?
  - `comprehensiveAndInteroperable` (`boolean`): Comprehensive and interoperable?
- **Outputs:**
  - `scenario` (`"paper only"` | `"partly digitized"` | `"unknown"`): Starting scenario
  - `entryStep`: Entry step
- **Rules:** 4, hit policy `FIRST`. The last rule returns `"unknown"` when any input has not been answered.
