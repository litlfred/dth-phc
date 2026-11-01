<!-- GENERATED from dth-phc/processes/pcposs-implementation-lifecycle.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — PCPOSS implementation lifecycle (2.4, Fig. 7)

> **Generated, and not the authority.** This is `dth-phc/processes/pcposs-implementation-lifecycle.bpmn` (process `Process_PcpossImplementationLifecycle`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

End-to-end iterative lifecycle for transitioning primary health care point-of-service systems from paper or siloed legacy tools to an enterprise-grade, interoperable PCPOSS across the four handbook phases and the agile release loop of Fig.

## Begin — PCPOSS selected as health intervention (2.3, Fig. 7) (`Start_Lifecycle`)

- Begin here: Section 2.3 (prose-sec-009) and Fig.
- Call `workflow_start` with `process: "Process_PcpossImplementationLifecycle"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_AssessReadinessScenario` (Assess digital readiness starting scenario (2.1))

### 1. Assess digital readiness starting scenario (2.1) (`Task_AssessReadinessScenario`)

- Who: the `Business analyst, health informatician & user researcher` lane (role `pers:business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Section 2.1 (prose-sec-007, pages 22-23): Determine whether the health system is starting from a paper-only system or starting with some parts already digitized (disparate/siloed PCPOSSs or parallel paper records).
- Record it: `workflow_complete` with `node: "Task_AssessReadinessScenario"`.
- next: → `GW_StartingScenario` (Starting scenario (2.1)?)

### Decide — Starting scenario (2.1)? (`GW_StartingScenario`)

- Computed from decisions/starting-scenario.dmn#Decision_StartingScenario (Section 2.1, prose-sec-007): routes 'paper only' or 'partly digitized' into Phase 1 requirements gathering.
- Computed by the DMN table `decisions/starting-scenario.dmn#Decision_StartingScenario`: call `workflow_complete` with `node: "GW_StartingScenario"` and the `facts` it reads — the table returns the branch; pass no `outcome`.
  - «paper only» → `Call_Phase1_Requirements` (Phase 1: Understand and prioritize user requirements (Ch 3))
  - «partly digitized» → `Call_Phase1_Requirements` (Phase 1: Understand and prioritize user requirements (Ch 3))

### 2. Phase 1: Understand and prioritize user requirements (Ch 3) (`Call_Phase1_Requirements`)

- Who: the `Business analyst, health informatician & user researcher` lane (role `pers:business-analyst`).
- Skill: `l2-dak-authoring`.
- What: Section 2.4 Step 1 and Chapter 3 (prose-sec-010, prose-sec-012..019): Understand users, map workflows, streamline forms and indicators, define data dictionary, decision logic, schedules and prioritized requirements.
- A subprocess (`Process_UnderstandUserRequirements`): `workflow_next` reports its own steps; complete those — this call activity itself is not completable.
- next: → `Call_Phase2_Design` (Phase 2: Undertake design and adaptation — build and test (Ch 4))

### 3. Phase 2: Undertake design and adaptation — build and test (Ch 4) (`Call_Phase2_Design`)

- Who: the `Technology partner (solutions architect, software engineer, designer)` lane (role `pers:technology-partner`).
- Skill: `l2-dak-authoring`.
- What: Section 2.4 Step 2, Fig.
- A subprocess (`Process_DesignAndAdaptation`): `workflow_next` reports its own steps; complete those — this call activity itself is not completable.
- next: → `GW_MvpSpecsMet` (Meets MVP / release specs to deploy (Fig. 7)?)

### Decide — Meets MVP / release specs to deploy (Fig. 7)? (`GW_MvpSpecsMet`)

- Fig.
- Call `workflow_complete` with `node: "GW_MvpSpecsMet"` and `outcome` set to the label that holds:
  - «repeat build and test» → `Call_Phase2_Design` (Phase 2: Undertake design and adaptation — build and test (Ch 4))
  - «ready to train and deploy» → `Call_Phase3_RollOut` (Phase 3: Conduct training, testing and roll-out (Ch 5))

### 4. Phase 3: Conduct training, testing and roll-out (Ch 5) (`Call_Phase3_RollOut`)

- Who: the `Implementing team & M&E specialist` lane (role `pers:implementing-team`).
- Skill: `test-plan-execution`.
- What: Section 2.4 Step 3, Fig.
- A subprocess (`Process_TrainingTestingAndRollOut`): `workflow_next` reports its own steps; complete those — this call activity itself is not completable.
- next: → `Task_GatherUserFeedback` (Gather and manage user feedback in routine use (Fig. 7, 5.4))

### 5. Gather and manage user feedback in routine use (Fig. 7, 5.4) (`Task_GatherUserFeedback`)

- Who: the `Health worker occupational groups & health service users` lane (role `pers:health-worker`).
- Skill: `content-feedback`.
- What: Fig.
- Record it: `workflow_complete` with `node: "Task_GatherUserFeedback"`.
- next: → `GW_NextIterationOrScale` (Agile iteration stage (Fig. 7)?)

### Decide — Agile iteration stage (Fig. 7)? (`GW_NextIterationOrScale`)

- Fig.
- Call `workflow_complete` with `node: "GW_NextIterationOrScale"` and `outcome` set to the label that holds:
  - «iterate Version 1 / Version 2» → `Call_Phase1_Requirements` (Phase 1: Understand and prioritize user requirements (Ch 3))
  - «prepare for scale-up» → `Call_Phase4_ScaleUp` (Phase 4: Prepare for scaling up and legacy phase-out (Ch 6))

### 6. Phase 4: Prepare for scaling up and legacy phase-out (Ch 6) (`Call_Phase4_ScaleUp`)

- Who: the `Public health authority (ministry of health)` lane (role `pers:public-health-authority`).
- Skill: `methodology-adoption`.
- What: Section 2.4 Step 4, Fig.
- A subprocess (`Process_ScaleUp`): `workflow_next` reports its own steps; complete those — this call activity itself is not completable.
- next: → `End_Lifecycle` (PCPOSS scaled up with continuous improvement (Fig. 7))

## Done — PCPOSS scaled up with continuous improvement (Fig. 7) (`End_Lifecycle`)

- The instance completes here: Fig. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
