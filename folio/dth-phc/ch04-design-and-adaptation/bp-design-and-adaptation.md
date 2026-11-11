# Phase 2: Design and adaptation (Chapter 4)

Formal BPMN 2.0 model of Chapter 4 (sections 4.1 to 4.5, `sec-020`–`sec-024`), covering software and vendor selection, functional requirement validation, the three-stage human-centred prototyping loop, enterprise architecture and interoperability standards, and software build with the 7-part QA test suite.

![Phase 2: Design and adaptation](media/bp-design-and-adaptation.svg)

## Structure of the model (`Process_DesignAndAdaptation`)

1. **Software and vendor selection (4.1, `sec-020`, Annex 1):** `Task_4_1_SelectSoftwareAndVendor` evaluates candidate platforms (adapting an existing global good / commercial platform vs building from scratch) against prioritized requirements and total cost of ownership.
2. **Validating functional requirements (4.2, `sec-021`):** `Task_4_2_ValidateFunctionalRequirements` reviews requirement specifications with clinical and technical stakeholders before design begins.
3. **Three-stage iterative prototyping loop with end-users (4.3, `sec-022`):**
   - Stage 1: `Task_4_3a_Wireframes` (*Build low-fidelity wireframes*) → `Task_4_3a_TestWireframes` (*Test wireframes with end-users*) → `GW_WireframesApproved`.
   - Stage 2: `Task_4_3b_Mockups` (*Develop visual mock-ups*) → `Task_4_3b_TestMockups` (*Test mock-ups with end-users*) → `GW_MockupsApproved`.
   - Stage 3: `Task_4_3c_ClickablePrototype` (*Build interactive clickable prototype*) → `Task_4_3c_TestPrototype` (*Test clickable prototype with end-users*) → `GW_PrototypeApproved`.
4. **System architecture and interoperability standards (4.4, `sec-023`):** `Task_4_4_ArchitectureAndStandards` defines the target enterprise architecture, offline/online synchronisation, security/privacy controls, and HL7 FHIR / IHE / ICD-11 / LOINC / SNOMED-GPS interoperability standards.
5. **Software build and 7-part QA test suite (4.5, `sec-024`):** `Task_4_5a_BuildAndConfigure` builds the increment and `Task_4_5b_Run7QATests` runs unit, integration, functional, performance, security, usability and compatibility tests, looping via `GW_QAPassed` until all 7 test categories pass (aligned with `cat-harness` `crdm-deliver.bpmn`).
