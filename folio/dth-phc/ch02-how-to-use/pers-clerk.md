# Clerk (facility registration and records staff)

Health facility registration, reception and medical records staff who check in clients, verify identity in the client registry / EHR, and manage paper or electronic registers:

- **Role in the handbook:** Highlighted in stakeholder mapping (3.1), featured as a distinct swimlane in the reproduced WHO ANC DAK Workflow A registration business process (Figs. 10 & 11, section 3.3.2, `sec-014`), included in facility training and UAT (5.1, 5.2), and central to the staged phase-out of legacy paper registers and paper backup SOPs (6.4, `sec-032`).

## Three-way linkage

1. **BPMN lanes performed:**
   - [`understand-user-requirements.bpmn#Lane-Ch3-Users`](../../../processes/understand-user-requirements.bpmn) (*Health Workers, Clerks, Supervisors & Service Users*)
   - [`training-testing-and-roll-out.bpmn#Lane-Ch5-Users`](../../../processes/training-testing-and-roll-out.bpmn) (*Health Workers, Clerks & Supervisors*)
   - [`scale-up.bpmn#Lane-Ch6-Users`](../../../processes/scale-up.bpmn) (*Health Workers & Clerks*)
2. **`smart-ra` ArchiMate mapping:** Sub-role of existing `archimate:Stakeholder` **Health Workers** (`id-8d3dd8b68d504c2a9fe8cf414b16c127`) and **Health Care Institutions** (`id-515be0d38c564767bc2b1ee5fcb0adb6`).
3. **Glossary term:** `dth-phc:clerk`.
