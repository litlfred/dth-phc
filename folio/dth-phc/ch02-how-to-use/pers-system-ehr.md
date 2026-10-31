# Electronic health record (EHR) system

One of the four core application types that make up a PCPOSS (section 1.1, `sec-004`; Glossary, `sec-003`) — a longitudinal digital record of a health service user's clinical encounters, diagnoses, observations, medications and referrals across care episodes:

- **Role in the handbook:** Captures standardized core data elements at the point of care (3.4), exchanges longitudinal clinical summaries with the national Shared Health Record (`SHR Repository`) and registries via HL7 FHIR / IHE profiles (4.4), and feeds aggregate HMIS reporting indicators automatically (3.4.3).

## Three-way linkage

1. **BPMN lanes & resources:**
   - Declared as `<bpmn:resource id="pers-system-ehr">` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn) and modelled under [`understand-user-requirements.bpmn#Lane-Ch3-HI`](../../../processes/understand-user-requirements.bpmn) and [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn).
2. **Concepts:** [Electronic Health Record System (EHR)](https://litlfred.github.io/dth-phc/v0/ns#glossary/dth-phc/electronic-health-record-system), [Point-of-service applications](https://litlfred.github.io/smart-ra/v0/ns#glossary/dpi-h-ra/point-of-service-applications)
3. **Glossary term:** `dth-phc:electronic-health-record` (links to `dpi-h-ra:electronic-health-record`).
