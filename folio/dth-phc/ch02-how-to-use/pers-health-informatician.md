# Health informatician

A core member of the PCPOSS implementing team (section 2.2) responsible for health data dictionaries, terminology bindings, indicator mappings and semantic interoperability:

- **Role definition (section 2.2):** *"Someone who understands both health care and information systems. They help make sure the system captures and uses health data in a meaningful and standardized way."*
- **Phase 1 — Understanding user requirements (Chapter 3, `sec-011`, `sec-015`):** Leads the paper-form inventory (3.4.1, Annex 7), form data element extraction (3.4.2, Annex 8), aggregate indicator mapping (3.4.3, Annex 9), data-element minimization decision (`keep-data-element.dmn`, 3.4.4, Fig. 12), and core data dictionary compilation with ICD-11, LOINC, SNOMED-GPS, ICHI and ICF terminology bindings (3.4.5, Annex 10).
- **Phase 2 — Design and adaptation (Chapter 4, `sec-020`, `sec-023`):** Co-designs the system architecture and HL7 FHIR / IHE interoperability profiles (4.4).

## Three-way linkage

1. **BPMN lanes performed:**
   - [`understand-user-requirements.bpmn#Lane-Ch3-HI`](../../../processes/understand-user-requirements.bpmn) (*Health Informatician & M&E Specialist*)
   - [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn) (*Solutions Architect & Health Informatician*)
2. **`smart-ra` ArchiMate mapping:** Shared `archimate:BusinessRole` **Health informatician** associated with `Terminology Service` (`id-3f41de2b51c24041b08243bf72b140d1`) and `Logical Information Model Registry` (`id-c0d39bf67fe64f54b07fbeb9bf37d404`) on the `Interoperability Layer` (`id-8c5dd12b8d4e425184f6003d0513d569`) and `SHR` (`id-cefde7ed0dcd47d3bb214657ac3e5725`) views.
3. **Glossary term:** `dth-phc:health-informatician`.
