<!-- GENERATED from dth-phc/processes/design-and-adaptation.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — Undertake design and adaptation (Ch 4, 4.1-4.5)

> **Generated, and not the authority.** This is `dth-phc/processes/design-and-adaptation.bpmn` (process `Process_DesignAndAdaptation`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

Select the software and vendor, validate functional requirements with stakeholders, iteratively design and test wireframes, mock-ups and clickable prototypes with end-users, specify the system and interoperability architecture, and build and QA-test the beta PCPOSS.

## Begin — Ch 3 requirements documentation & DAKs received (`Start_Ch4`)

- Begin here: Chapter 4 opener panel inputs (prose-sec-020, page 50): PCPOSS scope, governance structure, budget/timeline/risk plan, applicable WHO DAKs, and the nine requirements documentation outputs from Chapter 3.
- Call `workflow_start` with `process: "Process_DesignAndAdaptation"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_4_1_SelectSoftwareVendor` (4.1 Finalize software & vendor selection (bespoke, COTS or reference software))

### 1. 4.1 Finalize software & vendor selection (bespoke, COTS or reference software) (`Task_4_1_SelectSoftwareVendor`)

- Who: the `Business analyst & implementing team` lane (role `pers:business-analyst`).
- Skill: `l2-dependency-choice`.
- What: Section 4.1 (prose-sec-020, pages 50-53, Table 2): Conduct landscape analysis and scorecard evaluation across bespoke software, commercial/open-source COTS, digital public goods and SMART Guidelines L4 reference software.
- Record it: `workflow_complete` with `node: "Task_4_1_SelectSoftwareVendor"`.
- next: → `Task_4_2_ValidateRequirements` (4.2 Validate functional requirements in stakeholder workshops & design test use cases (4.3.2))

### 2. 4.2 Validate functional requirements in stakeholder workshops & design test use cases (4.3.2) (`Task_4_2_ValidateRequirements`)

- Who: the `Business analyst & implementing team` lane (role `pers:business-analyst`).
- Skill: `content-review`.
- What: Section 4.2 (prose-sec-021, page 53) and Section 4.3.2 Step 1 (prose-sec-022, page 55): Validate and confirm functional requirements with key stakeholders before build, and design testing use cases from Section 3.2 use cases and user stories.
- Record it: `workflow_complete` with `node: "Task_4_2_ValidateRequirements"`.
- next: → `Task_4_3_Wireframe` (4.3.1 Draw low-fidelity sketches and wireframes)

### 3. 4.3.1 Draw low-fidelity sketches and wireframes (`Task_4_3_Wireframe`)

- Who: the `Designer` lane (role `pers:designer`).
- Skill: `wireframe-design-review`.
- What: Section 4.3.1 and Fig.
- Record it: `workflow_complete` with `node: "Task_4_3_Wireframe"`.
- next: → `Task_4_3_TestWireframe` (4.3.2 Test wireframe structure & data-entry flow with end-users)

### 4. 4.3.2 Test wireframe structure & data-entry flow with end-users (`Task_4_3_TestWireframe`)

- Who: the `Targeted health worker occupational groups & end-users` lane (role `pers:health-worker`).
- Skill: `wireframe-design-review`.
- What: Section 4.3.1-4.3.2 and Fig.
- Record it: `workflow_complete` with `node: "Task_4_3_TestWireframe"`.
- next: → `GW_WireframeOk` (Wireframe layout & flow validated?)

### Decide — Wireframe layout & flow validated? (`GW_WireframeOk`)

- Section 4.3.2 (prose-sec-022): If layout or data-entry flow needs revision, iterate the wireframe; once validated, advance to moderate-fidelity mock-ups.
- Call `workflow_complete` with `node: "GW_WireframeOk"` and `outcome` set to the label that holds:
  - «iterate wireframe» → `Task_4_3_Wireframe` (4.3.1 Draw low-fidelity sketches and wireframes)
  - «advance to mock-up» → `Task_4_3_Mockup` (4.3.1 Create moderate-fidelity visual mock-ups)

### 5. 4.3.1 Create moderate-fidelity visual mock-ups (`Task_4_3_Mockup`)

- Who: the `Designer` lane (role `pers:designer`).
- Skill: `wireframe-design-review`.
- What: Section 4.3.1 and Fig.
- Record it: `workflow_complete` with `node: "Task_4_3_Mockup"`.
- next: → `Task_4_3_TestMockup` (4.3.2 Test mock-ups (look, feel & language) with end-users)

### 6. 4.3.2 Test mock-ups (look, feel & language) with end-users (`Task_4_3_TestMockup`)

- Who: the `Targeted health worker occupational groups & end-users` lane (role `pers:health-worker`).
- Skill: `wireframe-design-review`.
- What: Section 4.3.2 (prose-sec-022, pages 55-56): Test multiple mock-up options with end-users and document structured feedback (things liked, confusing features, improvements).
- Record it: `workflow_complete` with `node: "Task_4_3_TestMockup"`.
- next: → `GW_MockupOk` (Mock-up look & feel validated?)

### Decide — Mock-up look & feel validated? (`GW_MockupOk`)

- Section 4.3.2 (prose-sec-022): Iterate mock-ups on vetted feedback, or advance to higher-fidelity clickable prototype.
- Call `workflow_complete` with `node: "GW_MockupOk"` and `outcome` set to the label that holds:
  - «iterate mock-up» → `Task_4_3_Mockup` (4.3.1 Create moderate-fidelity visual mock-ups)
  - «advance to clickable prototype» → `Task_4_3_Prototype` (4.3.1 Build higher-fidelity clickable prototype)

### 7. 4.3.1 Build higher-fidelity clickable prototype (`Task_4_3_Prototype`)

- Who: the `Designer` lane (role `pers:designer`).
- Skill: `wireframe-design-review`.
- What: Section 4.3.1 and Fig.
- Record it: `workflow_complete` with `node: "Task_4_3_Prototype"`.
- next: → `Task_4_3_TestPrototype` (4.3.2 Validate clickable prototype via end-user role play)

### 8. 4.3.2 Validate clickable prototype via end-user role play (`Task_4_3_TestPrototype`)

- Who: the `Targeted health worker occupational groups & end-users` lane (role `pers:health-worker`).
- Skill: `wireframe-design-review`.
- What: Section 4.3.2 (prose-sec-022, pages 55-56): End-users experiment with the clickable prototype ('Show, don't tell') in role-play scenarios; feedback is documented and vetted by stakeholders to prevent scope creep.
- Record it: `workflow_complete` with `node: "Task_4_3_TestPrototype"`.
- next: → `GW_PrototypeOk` (Clickable prototype approved?)

### Decide — Clickable prototype approved? (`GW_PrototypeOk`)

- Section 4.3.2 Step 5 (prose-sec-022, page 56): Vetted feedback is either incorporated into another prototype iteration or approved for system architecture and engineering build.
- Call `workflow_complete` with `node: "GW_PrototypeOk"` and `outcome` set to the label that holds:
  - «incorporate vetted feedback» → `Task_4_3_Prototype` (4.3.1 Build higher-fidelity clickable prototype)
  - «prototype approved» → `Task_4_4_Architecture` (4.4 Design system architecture & interoperability standards (FHIR, HIE))

### 9. 4.4 Design system architecture & interoperability standards (FHIR, HIE) (`Task_4_4_Architecture`)

- Who: the `Solutions architect & health informatician` lane (role `pers:solutions-architect`).
- Skill: `archimate-models`.
- What: Section 4.4 (prose-sec-023, pages 56-60, Table 3, Figs.
- Record it: `workflow_complete` with `node: "Task_4_4_Architecture"`.
- next: → `Task_4_5_BuildAndDocument` (4.5 Establish test plan, build beta PCPOSS & product documentation)

### 10. 4.5 Establish test plan, build beta PCPOSS & product documentation (`Task_4_5_BuildAndDocument`)

- Who: the `Software engineer / technology partner` lane (role `pers:software-engineer`).
- Skill: `l4-application-build`.
- What: Section 4.5 (prose-sec-024, pages 60-61): Establish comprehensive test plan once requirements are finalized, build or adapt the PCPOSS beta version in sprints, and author product documentation.
- Record it: `workflow_complete` with `node: "Task_4_5_BuildAndDocument"`.
- next: → `Task_4_5_RunQaTests` (4.5 Execute installation, stress, security, UI, integration, QA & accessibility tests)

### 11. 4.5 Execute installation, stress, security, UI, integration, QA & accessibility tests (`Task_4_5_RunQaTests`)

- Who: the `Software engineer / technology partner` lane (role `pers:software-engineer`).
- Skill: `content-test`.
- What: Section 4.5 (prose-sec-024, page 61): Technology partner runs installation testing, stress testing, security testing, graphic UI testing, integration testing, quality assurance testing and accessibility testing.
- Record it: `workflow_complete` with `node: "Task_4_5_RunQaTests"`.
- next: → `GW_QaPassed` (All 4.5 QA & accessibility tests pass?)

### Decide — All 4.5 QA & accessibility tests pass? (`GW_QaPassed`)

- Section 4.5 Checkpoint (prose-sec-024, page 61): Verify that all seven test categories pass and that the MVP/beta version, UI design, system architecture and product documentation are ready for Chapter 5 UAT and roll-out.
- Call `workflow_complete` with `node: "GW_QaPassed"` and `outcome` set to the label that holds:
  - «fix defects» → `Task_4_5_BuildAndDocument` (4.5 Establish test plan, build beta PCPOSS & product documentation)
  - «beta ready» → `End_Ch4` (Beta version of PCPOSS & documentation ready)

## Done — Beta version of PCPOSS & documentation ready (`End_Ch4`)

- The instance completes here: Chapter 4 opener panel outputs complete: Selected software and software vendor, System architecture, User interface design, Product documentation, and Beta version of the PCPOSS. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
