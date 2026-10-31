# Health worker (clinician, nurse, midwife, community health worker)

The primary point-of-service end-user of a PCPOSS (section 1.1, `sec-004`; Phase 1–4 panels): doctors, clinical officers, nurses, midwives and community health workers delivering primary health care services:

- **Co-design and validation:** Participates in stakeholder mapping (3.1), contextual observations and interviews (3.2), prototype usability testing across wireframes, mock-ups and clickable prototypes (4.3), training on PCPOSS use (5.1.1), User Acceptance Testing (5.2), and routine clinical data entry and data-use culture at scale (6.4, 6.5).

## Three-way linkage

1. **BPMN lanes performed:**
   - [`pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Users`](../../../processes/pcposs-implementation-lifecycle.bpmn) (*Health Workers & Facility Staff*)
   - [`understand-user-requirements.bpmn#Lane-Ch3-Users`](../../../processes/understand-user-requirements.bpmn) (*Health Workers, Clerks, Supervisors & Service Users*)
   - [`design-and-adaptation.bpmn#Lane-Ch4-Users`](../../../processes/design-and-adaptation.bpmn) (*Health Workers & Health Service Users*)
   - [`training-testing-and-roll-out.bpmn#Lane-Ch5-Users`](../../../processes/training-testing-and-roll-out.bpmn) (*Health Workers, Clerks & Supervisors*)
   - [`scale-up.bpmn#Lane-Ch6-Users`](../../../processes/scale-up.bpmn) (*Health Workers & Clerks*)
2. **`smart-ra` ArchiMate mapping:** Existing `archimate:Stakeholder` **Health Workers** (`id-8d3dd8b68d504c2a9fe8cf414b16c127` in `WHOBaseFile.archimate`); `smart-base` generic personas `HealthcareProvider; CommunityHealthWorker`.
3. **Glossary term:** `dth-phc:health-worker` (aligned with `dth-hrh:health-worker`).
