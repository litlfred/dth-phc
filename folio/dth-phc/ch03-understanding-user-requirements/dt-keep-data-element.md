# Data-element minimization decision table (section 3.4.4, Fig. 12)

Formal DMN 1.5 decision table (`Decision_KeepDataElement`, `hitPolicy="FIRST"`) encoding the Fig. 12 decision tree in section 3.4.4 (*Determine which data elements are needed*, `sec-015`), evaluated at gateway `GW_KeepDataElement` in [`understand-user-requirements.bpmn`](../../../processes/understand-user-requirements.bpmn).

## Decision structure

- **Inputs:**
  - `duplicated` (`boolean`): Is the data element duplicated across forms or registers?
  - `orphaned` (`boolean`): Is the data element orphaned (collected on a form without any downstream clinical or reporting use)?
  - `neededForCareOrIndicator` (`boolean`): Is the data element needed for direct clinical care, continuity of care, or an approved aggregate health indicator (section 3.4.3)?
- **Outputs:**
  - `disposition` (`"keep"` | `"remove"`): Routes to `Task_3_4_4_RetainDataElement` (`"keep"`) or `Task_3_4_4_RemoveDataElement` (`"remove"`).
  - `rationale`: Standardized explanation recorded in the form data mapping worksheet (Annex 8).
