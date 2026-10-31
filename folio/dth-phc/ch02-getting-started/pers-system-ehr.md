# Electronic health record (EHR) system

One of the four core application types that make up a PCPOSS (section 1.1, `sec-004`; Glossary, `sec-003`) — a longitudinal digital record of a health service user's clinical encounters, diagnoses, observations, medications and referrals across care episodes:

- **Role in the handbook:** Captures standardized core data elements at the point of care (3.4), exchanges longitudinal clinical summaries with the national Shared Health Record (`SHR Repository`) and registries via HL7 FHIR / IHE profiles (4.4), and feeds aggregate HMIS reporting indicators automatically (3.4.3).

## Three-way linkage

1. **BPMN lanes & resources:**
   - Declared as `<bpmn:resource id="pers-system-ehr">` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn) and modelled under [`understand-user-requirements.bpmn#Lane-Ch3-HI`](../../../processes/understand-user-requirements.bpmn) and [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn).
2. **`smart-ra` ArchiMate mapping:** Existing `SHR Repository` (`id-0e6d89398fff4f20994a31b4de58e7d7`) and `Vendor EHR Product` (`id-3bd1011d76c843fa860255f00a6aa68f`) on the `SHR` view (`id-cefde7ed0dcd47d3bb214657ac3e5725`), and `Electronic health record (EHR)` component on the `smart-ra` PCPOSS view.
3. **Glossary term:** `dth-phc:electronic-health-record` (links to `dpi-h-ra:electronic-health-record`).
