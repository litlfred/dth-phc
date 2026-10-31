# Decision-support system (DSS)

One of the four core application types that make up a PCPOSS (section 1.1, `sec-004`; Glossary, `sec-003`) — the clinical and operational rule engine that evaluates decision-support tables (3.6, Annex 11) and scheduling logic (3.7, Annex 12) at the point of care:

- **Role in the handbook:** Executes WHO SMART Guidelines decision-support logic (3.6, Annex 11) and follow-up/immunization scheduling rules (3.7, Annex 12) to present real-time clinical prompts, alerts, counselling messages and care-plan schedules to health workers.

## Three-way linkage

1. **BPMN lanes & resources:**
   - Declared as `<bpmn:resource id="pers-system-dss">` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn) and linked to Step 3.6 (`Task_3_6_DecisionSupport`) and Step 3.7 (`Task_3_7_SchedulingLogic`) in [`understand-user-requirements.bpmn#Lane-Ch3-BA`](../../../processes/understand-user-requirements.bpmn) and Step 4.4 (`Task_4_4_ArchitectureAndStandards`) in [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn).
2. **`smart-ra` ArchiMate mapping:** Existing `archimate:ApplicationComponent` **Decision Support Engine** (`id-539b04ae45f147258d8253ae5cb87402`) on the `CDS` view (`id-4c98f10e0a244315acddaf5257c7822e`).
3. **Glossary term:** `dth-phc:decision-support-system` (links to `dpi-h-ra:clinical-decision-support-systems`).
