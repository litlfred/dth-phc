# Solutions architect

A core member of the PCPOSS implementing team (section 2.2) who designs the end-to-end technical architecture and enterprise integration of the PCPOSS:

- **Role definition (section 2.2):** *"Someone who designs the overall technical structure of the system, making sure all the parts fit together and can connect with other digital health systems."*
- **Phase 2 — Design and adaptation (Chapter 4, `sec-020`, `sec-023`):** Designs the system architecture and interoperability standards (4.4), aligning the PCPOSS with national enterprise architecture (OpenHIE / ITU digital health platform), offline-first synchronisation, security/privacy controls, and HL7 FHIR / IHE profiles.
- **Phase 4 — Scale-up (Chapter 6, `sec-029`):** Assesses technical infrastructure and interoperability readiness for national scale-up (6.1).

## Three-way linkage

1. **BPMN lanes performed:**
   - [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn) (*Solutions Architect & Health Informatician*)
   - [`scale-up.bpmn#Lane-Ch6-ME`](../../../processes/scale-up.bpmn) (*M&E Specialist & Solutions Architect*)
2. **`smart-ra` ArchiMate mapping:** Shared `archimate:BusinessRole` **Enterprise / solutions architect** (across `dth-phc`, `dth-sc`, `dth-hrh`, `smart-ra`) linked to `Interoperability Component` (`id-80856538cbd44167a37b276e38c994c3`) and `Interoperability Layer` view (`id-8c5dd12b8d4e425184f6003d0513d569`).
3. **Glossary term:** `dth-phc:solutions-architect`.
