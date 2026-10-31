<!-- GENERATED from dth-phc/processes/understand-user-requirements.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — Understand user requirements (Ch 3, 3.1-3.8)

> **Generated, and not the authority.** This is `dth-phc/processes/understand-user-requirements.bpmn` (process `Process_UnderstandUserRequirements`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

Gather, streamline and prioritize the user, workflow, data, clinical decision-support, scheduling and system requirements for a PCPOSS across steps 3.1 to 3.8, producing each corresponding WHO SMART Guidelines L2 DAK component.

## Begin — Ch 3 inputs assembled (strategies, guidelines, paper registers) (`Start_Ch3`)

- Begin here: Chapter 3 opener panel (prose-sec-012, page 28): National health and digital health strategies, privacy/security policies, architecture blueprint, infrastructure assessment, unique ID method, WHO/national guidelines, SOPs and existing paper forms.
- Call `workflow_start` with `process: "Process_UnderstandUserRequirements"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_3_1_Methods` (3.1 Conduct desk review, observations, interviews & workshops)

### 1. 3.1 Conduct desk review, observations, interviews & workshops (`Task_3_1_Methods`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `dak-l1-library`.
- What: Section 3.1 (prose-sec-012, pages 28-33) and Annex 2/3 Observations worksheet (prose-sec-036): Combine desk review (3.1.1), facility observations (3.1.2), semi-structured and follow-up interviews (3.1.3, Fig.
- Record it: `workflow_complete` with `node: "Task_3_1_Methods"`.
- next: → `Task_3_1_Participate` (3.1 Share routine care workflows, constraints & needs)

### 2. 3.1 Share routine care workflows, constraints & needs (`Task_3_1_Participate`)

- Who: the `Targeted health worker occupational groups & health service users` lane (role `health-worker`).
- Skill: `guideline-use-case`.
- What: Section 3.1.2-3.1.4 (prose-sec-012): Targeted health worker occupational groups and health service users participate in observations, interviews and workshops to ground requirements in real point-of-care practice.
- Record it: `workflow_complete` with `node: "Task_3_1_Participate"`.
- next: → `Task_3_2_1_Personas` (3.2.1 Create user personas [produces: persona])

### 3. 3.2.1 Create user personas [produces: persona] (`Task_3_2_1_Personas`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Section 3.2.1 (prose-sec-013, pages 33-34) and Annex 4 User persona worksheet (prose-sec-037): Produce structured user personas (DAK kind `persona`, smart-base:Persona) describing demographics, responsibilities, goals, pain points and digital literacy.
- Record it: `workflow_complete` with `node: "Task_3_2_1_Personas"`.
- next: → `Task_3_2_2_UseCases` (3.2.2 Gather use cases & 3.2.3 user stories [produces: user-scenario])

### 4. 3.2.2 Gather use cases & 3.2.3 user stories [produces: user-scenario] (`Task_3_2_2_UseCases`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Sections 3.2.2-3.2.3 (prose-sec-013, pages 34-35) and Annex 5 User stories worksheet (prose-sec-038): Produce use cases and 'As a <persona>, I want <action>, so that <outcome>' user stories (DAK kind `user-scenario`, smart-base:UserScenario).
- Record it: `workflow_complete` with `node: "Task_3_2_2_UseCases"`.
- next: → `Task_3_3_Workflows` (3.3 Map as-is and to-be business processes [produces: business-process])

### 5. 3.3 Map as-is and to-be business processes [produces: business-process] (`Task_3_3_Workflows`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `bpmn-authoring`.
- What: Section 3.3 (prose-sec-014, pages 35-38, Table 1, Figs.
- Record it: `workflow_complete` with `node: "Task_3_3_Workflows"`.
- next: → `Task_3_4_InventoryAndIndicators` (3.4.1-3.4.3 Inventory forms, map form data & compile indicators [produces: indicator])

### 6. 3.4.1-3.4.3 Inventory forms, map form data & compile indicators [produces: indicator] (`Task_3_4_InventoryAndIndicators`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Sections 3.4.1-3.4.3 (prose-sec-015, pages 39-40) and Annexes 7-9 (prose-sec-040..042): Inventory paper registers (3.4.1), map data elements across forms (3.4.2), and compile aggregate indicators and calculation methods (3.4.3, DAK kind `indicator`, smart-base:Indicator).
- Record it: `workflow_complete` with `node: "Task_3_4_InventoryAndIndicators"`.
- next: → `Task_3_4_4_EvaluateDataElement` (3.4.4 Assess data element for duplication, need & orphan links (Fig. 12))

### 7. 3.4.4 Assess data element for duplication, need & orphan links (Fig. 12) (`Task_3_4_4_EvaluateDataElement`)

- Who: the `Health informatician` lane (role `health-informatician`).
- Skill: `l2-dak-authoring`.
- What: Section 3.4.4 and Fig.
- Record it: `workflow_complete` with `node: "Task_3_4_4_EvaluateDataElement"`.
- next: → `GW_KeepDataElement` (Keep or remove data element (3.4.4, Fig. 12)?)

### Decide — Keep or remove data element (3.4.4, Fig. 12)? (`GW_KeepDataElement`)

- Computed from decisions/keep-data-element.dmn#Decision_KeepDataElement (Section 3.4.4, Fig.
- Computed by the DMN table `decisions/keep-data-element.dmn#Decision_KeepDataElement`: call `workflow_complete` with `node: "GW_KeepDataElement"` and the `facts` it reads — the table returns the branch; pass no `outcome`.
  - «remove» → `Task_3_4_4_RemoveElement` (3.4.4 Remove non-essential data element with audit trail)
  - «keep» → `Task_3_5_DataDictionary` (3.4.5 & 3.5 Create data dictionary & map terminologies [produces: data-element])

### 8. 3.4.4 Remove non-essential data element with audit trail (`Task_3_4_4_RemoveElement`)

- Who: the `Health informatician` lane (role `health-informatician`).
- Skill: `l2-dak-authoring`.
- What: Section 3.4.4 (prose-sec-015, page 41): Remove data elements not needed for care delivery or indicator reporting while maintaining a backup original file and audit trail.
- Record it: `workflow_complete` with `node: "Task_3_4_4_RemoveElement"`.
- next: → `Task_3_5_DataDictionary` (3.4.5 & 3.5 Create data dictionary & map terminologies [produces: data-element])

### 9. 3.4.5 & 3.5 Create data dictionary & map terminologies [produces: data-element] (`Task_3_5_DataDictionary`)

- Who: the `Health informatician` lane (role `health-informatician`).
- Skill: `terminology-management`.
- What: Sections 3.4.5 and 3.5.1-3.5.2 (prose-sec-015, prose-sec-016, pages 41-44): Consolidate kept data elements into a data dictionary and map to standardized classifications and terminologies (ICD-11, LOINC, SNOMED-GPS, ICF, ICHI, HL7 FHIR; DAK kind `data-element`, smart-base:DataElement).
- Record it: `workflow_complete` with `node: "Task_3_5_DataDictionary"`.
- next: → `Task_3_6_DecisionLogic` (3.6 Document clinical decision-support logic [produces: decision-table])

### 10. 3.6 Document clinical decision-support logic [produces: decision-table] (`Task_3_6_DecisionLogic`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `dmn-authoring`.
- What: Section 3.6 (prose-sec-017, pages 44-47, Figs.
- Record it: `workflow_complete` with `node: "Task_3_6_DecisionLogic"`.
- next: → `Task_3_7_Schedules` (3.7 Map health service schedules [produces: scheduling-logic])

### 11. 3.7 Map health service schedules [produces: scheduling-logic] (`Task_3_7_Schedules`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Section 3.7 (prose-sec-018, pages 47-48) and Annex 12 Scheduling logic table guide (prose-sec-044): Document trigger events, due dates, overdue dates and expiration rules for recurring contacts and vaccinations (DAK kind `scheduling-logic`, smart-base:SchedulingLogic).
- Record it: `workflow_complete` with `node: "Task_3_7_Schedules"`.
- next: → `Task_3_8_GatherRequirements` (3.8 Gather functional & non-functional requirements [produces: freq, nfreq])

### 12. 3.8 Gather functional & non-functional requirements [produces: freq, nfreq] (`Task_3_8_GatherRequirements`)

- Who: the `Software engineer` lane (role `software-engineer`).
- Skill: `l2-dak-authoring`.
- What: Section 3.8 (prose-sec-019, pages 48-49) and Annex 13 Prioritization of requirements guide (prose-sec-045): Compile functional and non-functional requirements (DAK kinds `functional-requirement` and `non-functional-requirement`) with software engineering engagement on technical context.
- Record it: `workflow_complete` with `node: "Task_3_8_GatherRequirements"`.
- next: → `GW_RequirementPriority` (Requirement priority (3.8, Annex 13)?)

### Decide — Requirement priority (3.8, Annex 13)? (`GW_RequirementPriority`)

- Computed from decisions/requirement-priority.dmn#Decision_RequirementPriority (Section 3.8, Annex 13, prose-sec-019, prose-sec-045): classifies each requirement as 'High' (need-to-have), 'Medium' (should-have) or 'Low' (nice-to-have).
- Computed by the DMN table `decisions/requirement-priority.dmn#Decision_RequirementPriority`: call `workflow_complete` with `node: "GW_RequirementPriority"` and the `facts` it reads — the table returns the branch; pass no `outcome`.
  - «High» → `Task_3_8_PriorityHigh` (3.8 Classify as High priority (need-to-have for complete PCPOSS))
  - «Medium» → `Task_3_8_PriorityMedium` (3.8 Classify as Medium priority (should-have for uptake & usability))
  - «Low» → `Task_3_8_PriorityLow` (3.8 Classify as Low priority (nice-to-have for future roadmap))

### 13. 3.8 Classify as High priority (need-to-have for complete PCPOSS) (`Task_3_8_PriorityHigh`)

- Who: the `Business analyst & user researcher` lane (role `business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Annex 13 (prose-sec-045, page 95): High priority ('need-to-have') — without this function or feature, the PCPOSS is considered incomplete.
- Record it: `workflow_complete` with `node: "Task_3_8_PriorityHigh"`.
- next: → `Task_3_8_ConfirmPackage` (3.8 Confirm prioritized requirements documentation with public health authority)

### 14. 3.8 Classify as Medium priority (should-have for uptake & usability) (`Task_3_8_PriorityMedium`)

- Who: the `Health informatician` lane (role `health-informatician`).
- Skill: `l2-dak-authoring`.
- What: Annex 13 (prose-sec-045, page 95): Medium priority ('should-have') — strongly advised to improve uptake, usability and overall system performance.
- Record it: `workflow_complete` with `node: "Task_3_8_PriorityMedium"`.
- next: → `Task_3_8_ConfirmPackage` (3.8 Confirm prioritized requirements documentation with public health authority)

### 15. 3.8 Classify as Low priority (nice-to-have for future roadmap) (`Task_3_8_PriorityLow`)

- Who: the `Software engineer` lane (role `software-engineer`).
- Skill: `l2-dak-authoring`.
- What: Annex 13 (prose-sec-045, page 95): Low priority ('nice-to-have') — value-adding feature recorded for future developments and updates on the roadmap.
- Record it: `workflow_complete` with `node: "Task_3_8_PriorityLow"`.
- next: → `Task_3_8_ConfirmPackage` (3.8 Confirm prioritized requirements documentation with public health authority)

### 16. 3.8 Confirm prioritized requirements documentation with public health authority (`Task_3_8_ConfirmPackage`)

- Who: the `Public health authority` lane (role `public-health-authority`).
- Skill: `content-review`.
- What: Chapter 3 opener panel and Section 3.8 (prose-sec-012, prose-sec-019): Confirm the complete nine-component requirements documentation package with the public health authority to hand off to Chapter 4 Design and adaptation.
- Record it: `workflow_complete` with `node: "Task_3_8_ConfirmPackage"`.
- next: → `End_Ch3` (Ch 3 requirements documentation complete)

## Done — Ch 3 requirements documentation complete (`End_Ch3`)

- The instance completes here: Chapter 3 opener panel outputs complete: User personas, Use cases, User stories, As-is and to-be business processes, Data dictionary and data model, Documented health service schedule, Documented decision logic algorithms, List of indicators and calculation method, and Prioritized functional and non `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
