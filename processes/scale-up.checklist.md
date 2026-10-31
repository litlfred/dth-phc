<!-- GENERATED from dth-phc/processes/scale-up.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — Prepare for scale-up and legacy phase-out (Ch 6, 6.1-6.5)

> **Generated, and not the authority.** This is `dth-phc/processes/scale-up.bpmn` (process `Process_ScaleUp`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

Assess readiness of the PCPOSS and health system to scale up, define and monitor SMART objectives and benchmarks for legacy phase-out, execute staged region-by-region phase-out of paper and legacy systems while retaining paper backup SOPs, and embed change management and electronic data-use culture.

## Begin — Live version of PCPOSS in use (Ch 6 input) (`Start_Ch6`)

- Begin here: Chapter 6 opener panel input (prose-sec-029, page 66): Live version of the PCPOSS being used in routine care.
- Call `workflow_start` with `process: "Process_ScaleUp"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_6_1_AssessReadiness` (6.1 Assess PCPOSS & health-system readiness (MAPS toolkit, DHA, infrastructure))

### 1. 6.1 Assess PCPOSS & health-system readiness (MAPS toolkit, DHA, infrastructure) (`Task_6_1_AssessReadiness`)

- Who: the `Implementing team` lane (role `pers:implementing-team`).
- Skill: `methodology-adoption`.
- What: Section 6.1 (prose-sec-029, pages 66-68): Use the WHO MAPS toolkit to assess PCPOSS and health-system readiness for scale-up, register the project in the WHO Digital Health Atlas, and verify foundational elements (power, connectivity, political support).
- Record it: `workflow_complete` with `node: "Task_6_1_AssessReadiness"`.
- next: → `Task_6_2_DefineObjectives` (6.2 Set SMART objectives, phase-out benchmarks (Table 5) & legal recognition policies)

### 2. 6.2 Set SMART objectives, phase-out benchmarks (Table 5) & legal recognition policies (`Task_6_2_DefineObjectives`)

- Who: the `Public health authority (ministry of health)` lane (role `pers:public-health-authority`).
- Skill: `methodology-adoption`.
- What: Section 6.2 and Table 5 (prose-sec-030, pages 68-70): Establish country-defined SMART objectives and benchmarks for legacy phase-out, enact policies legally recognizing digital health records, and define downtime/offline backup paper SOPs.
- Record it: `workflow_complete` with `node: "Task_6_2_DefineObjectives"`.
- next: → `Task_6_3_MonitorObjectives` (6.3 Monitor and evaluate progress against objectives (Table 5 metrics))

### 3. 6.3 Monitor and evaluate progress against objectives (Table 5 metrics) (`Task_6_3_MonitorObjectives`)

- Who: the `Monitoring and evaluation specialist` lane (role `pers:monitoring-and-evaluation-specialist`).
- Skill: `methodology-adoption`.
- What: Sections 6.2-6.3 (prose-sec-030, prose-sec-031, pages 68-71): M&E specialists monitor system functionality, data migration, user adoption, efficiency, care quality, costs and health outcomes, leveraging direct in-system indicators where possible.
- Record it: `workflow_complete` with `node: "Task_6_3_MonitorObjectives"`.
- next: → `GW_ReadyToScaleUp` (Ready to scale up and phase out (6.1, 6.2)?)

### Decide — Ready to scale up and phase out (6.1, 6.2)? (`GW_ReadyToScaleUp`)

- Computed from decisions/ready-to-scale-up.dmn#Decision_ReadyToScaleUp (Sections 6.1-6.2, prose-sec-029, prose-sec-030): evaluates PCPOSS readiness, health-system readiness and whether country-defined SMART objectives are met.
- Computed by the DMN table `decisions/ready-to-scale-up.dmn#Decision_ReadyToScaleUp`: call `workflow_complete` with `node: "GW_ReadyToScaleUp"` and the `facts` it reads — the table returns the branch; pass no `outcome`.
  - «not» → `Task_6_1_RemediateGaps` (6.1-6.2 Remediate PCPOSS, infrastructure or adoption gaps before phase-out)
  - «proceed» → `Task_6_4_StagedPhaseOut` (6.4 Execute staged region-by-region legacy phase-out while retaining paper backup)

### 4. 6.1-6.2 Remediate PCPOSS, infrastructure or adoption gaps before phase-out (`Task_6_1_RemediateGaps`)

- Who: the `Technology partner` lane (role `pers:technology-partner`).
- Skill: `methodology-adoption`.
- What: Sections 6.1-6.2 (prose-sec-029, prose-sec-030): Technology partners and implementing teams address technical, infrastructure or adoption gaps while maintaining the PCPOSS until readiness benchmarks are met.
- Record it: `workflow_complete` with `node: "Task_6_1_RemediateGaps"`.
- next: → `Task_6_3_MonitorObjectives` (6.3 Monitor and evaluate progress against objectives (Table 5 metrics))

### 5. 6.4 Execute staged region-by-region legacy phase-out while retaining paper backup (`Task_6_4_StagedPhaseOut`)

- Who: the `Public health authority (ministry of health)` lane (role `pers:public-health-authority`).
- Skill: `methodology-adoption`.
- What: Section 6.4 (prose-sec-032, page 71): Phase out paper and/or legacy systems in a staged, province-by-province manner as each region meets readiness criteria, while keeping a backup paper mechanism for blackouts, cybersecurity incidents or crises.
- Record it: `workflow_complete` with `node: "Task_6_4_StagedPhaseOut"`.
- next: → `Task_6_5_ChangeManagement` (6.5 Adopt change management practices & cultivate electronic data-use culture)

### 6. 6.5 Adopt change management practices & cultivate electronic data-use culture (`Task_6_5_ChangeManagement`)

- Who: the `End-users (health workers, supervisors & programme managers)` lane (role `pers:health-worker`).
- Skill: `methodology-adoption`.
- What: Section 6.5 (prose-sec-033, pages 71-72): Embed change management at all health-system levels and cultivate a culture of electronic data use across health workers, supervisors and programme managers (linking toward SMART Guidelines L5 dynamic guidelines).
- Record it: `workflow_complete` with `node: "Task_6_5_ChangeManagement"`.
- next: → `End_Ch6` (PCPOSS scaled up & legacy systems phased out with paper backup)

## Done — PCPOSS scaled up & legacy systems phased out with paper backup (`End_Ch6`)

- The instance completes here: Chapter 6 opener panel outputs complete: Set of objectives and benchmarks met, and strategic plan for phasing out paper and/or legacy systems executed with resilient backup SOPs. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
