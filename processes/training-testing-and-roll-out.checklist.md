<!-- GENERATED from dth-phc/processes/training-testing-and-roll-out.bpmn by cat-harness-tools/scripts/bpmn-checklist.ts. Do not edit: change the diagram and regenerate (bun run cat bpmn:checklist). -->

# Checklist — Conduct training, testing and roll-out (Ch 5, 5.1-5.4)

> **Generated, and not the authority.** This is `dth-phc/processes/training-testing-and-roll-out.bpmn` (process `Process_TrainingTestingAndRollOut`) walked as a state machine. The diagram and the workflow engine decide; this list only reads them. Follow the `next:` line of each step rather than the order on the page, and record each step with the call it names, so the engine's committed state — not this list — says which edge was taken.

Prepare policies and training curricula, conduct competency-based end-user training and maintenance training, execute user acceptance testing (UAT) with curated test cases and test data, deploy the PCPOSS to production sites, and operate the continuous feedback and system maintenance loop.

## Begin — Beta version of PCPOSS available (Ch 5 input) (`Start_Ch5`)

- Begin here: Chapter 5 opener panel input (prose-sec-025, page 62): Beta version of the PCPOSS from Chapter 4.
- Call `workflow_start` with `process: "Process_TrainingTestingAndRollOut"` and the subject this run is about; keep the instance id it returns.
- next: → `Task_5_0_Policies` (5.0 Implement cybersecurity, privacy, e-signature, data-use & ID policies)

### 1. 5.0 Implement cybersecurity, privacy, e-signature, data-use & ID policies (`Task_5_0_Policies`)

- Who: the `Public health authority` lane (role `public-health-authority`).
- Skill: `methodology-adoption`.
- What: Chapter 5 opener panel (prose-sec-025, page 62): Public health authority implements policies surrounding cybersecurity, privacy, confidentiality, acceptability of electronic signatures, data use, identification management and content management.
- Record it: `workflow_complete` with `node: "Task_5_0_Policies"`.
- next: → `Task_5_1_1_TrainUsers` (5.1.1 Develop tailored curriculum & conduct training of trainers and end-users)

### 2. 5.1.1 Develop tailored curriculum & conduct training of trainers and end-users (`Task_5_1_1_TrainUsers`)

- Who: the `Implementing team` lane (role `implementing-team`).
- Skill: `methodology-adoption`.
- What: Section 5.1.1 (prose-sec-025, pages 62-63): Develop culturally and linguistically tailored competency-based training materials, test curriculum at small scale, train trainers for first-line support, and train health workers (including device familiarization).
- Record it: `workflow_complete` with `node: "Task_5_1_1_TrainUsers"`.
- next: → `Task_5_1_2_TrainMaintenance` (5.1.2 Train local technology partner(s) on system maintenance & troubleshooting)

### 3. 5.1.2 Train local technology partner(s) on system maintenance & troubleshooting (`Task_5_1_2_TrainMaintenance`)

- Who: the `Software engineer / technology partner` lane (role `software-engineer`).
- Skill: `methodology-adoption`.
- What: Section 5.1.2 (prose-sec-025, pages 63-64): Train local technology partner(s) on in-depth system architecture, troubleshooting and customization so they can maintain the PCPOSS without external intervention.
- Record it: `workflow_complete` with `node: "Task_5_1_2_TrainMaintenance"`.
- next: → `Task_5_2_1_CurateTestCases` (5.2.1 Create UAT test cases & curate realistic and edge-case test data)

### 4. 5.2.1 Create UAT test cases & curate realistic and edge-case test data (`Task_5_2_1_CurateTestCases`)

- Who: the `Implementing team` lane (role `implementing-team`).
- Skill: `test-data-curation`.
- What: Section 5.2.1 (prose-sec-026, pages 64-65): Create test cases from Section 3.2.2 and Section 4.3.2 use cases with expected outcomes, and curate test data reflecting real-time settings plus edge cases (aligned with DAK `test-scenario` and cat-harness `test-data-curation`).
- Record it: `workflow_complete` with `node: "Task_5_2_1_CurateTestCases"`.
- next: → `Task_5_2_RunUat` (5.2 Execute user acceptance testing (UAT) in existing workflows)

### 5. 5.2 Execute user acceptance testing (UAT) in existing workflows (`Task_5_2_RunUat`)

- Who: the `Targeted health workers & UAT end-users` lane (role `health-worker`).
- Skill: `test-plan-execution`.
- What: Section 5.2 (prose-sec-026, page 64): Trained UAT testers (including end-users and trusted advisers) use the beta PCPOSS in existing workflows and report bugs, design flaws, usability roadblocks and direct feedback to engineers.
- Record it: `workflow_complete` with `node: "Task_5_2_RunUat"`.
- next: → `GW_UatPassed` (UAT & deployment readiness passed?)

### Decide — UAT & deployment readiness passed? (`GW_UatPassed`)

- Section 5.2 (prose-sec-026, page 64): Determine whether bugs or usability roadblocks require updates to the beta PCPOSS before production deployment, or whether UAT passed for Version 1 release.
- Call `workflow_complete` with `node: "GW_UatPassed"` and `outcome` set to the label that holds:
  - «bugs or roadblocks found» → `Task_5_2_UpdatePcposs` (5.2 & 5.4 Address feedback, fix bugs & update PCPOSS release)
  - «UAT passed» → `Task_5_3_DeploySystem` (5.3 Install site infrastructure/hardware, migrate data, configure & deploy to production)

### 6. 5.2 & 5.4 Address feedback, fix bugs & update PCPOSS release (`Task_5_2_UpdatePcposs`)

- Who: the `Software engineer / technology partner` lane (role `software-engineer`).
- Skill: `l4-application-build`.
- What: Chapter 5 opener panel and Sections 5.2, 5.4 (prose-sec-025, prose-sec-026, prose-sec-028): Software engineers take direct end-user and UAT feedback and update the PCPOSS accordingly.
- Record it: `workflow_complete` with `node: "Task_5_2_UpdatePcposs"`.
- next: → `Task_5_2_RunUat` (5.2 Execute user acceptance testing (UAT) in existing workflows)

### 7. 5.3 Install site infrastructure/hardware, migrate data, configure & deploy to production (`Task_5_3_DeploySystem`)

- Who: the `Software engineer / technology partner` lane (role `software-engineer`).
- Skill: `methodology-adoption`.
- What: Section 5.3 (prose-sec-027, page 65): Install site infrastructure, deliver hardware, install PCPOSS software, migrate legacy data, load configuration data, set up facility and health-worker accounts, test site hardware, schedule non-disruptive deployment and deploy to production.
- Record it: `workflow_complete` with `node: "Task_5_3_DeploySystem"`.
- next: → `Task_5_4_FeedbackAndMaintenance` (5.4 Operate feedback SOP, hardware/software maintenance & impact M&E)

### 8. 5.4 Operate feedback SOP, hardware/software maintenance & impact M&E (`Task_5_4_FeedbackAndMaintenance`)

- Who: the `Implementing team` lane (role `implementing-team`).
- Skill: `content-feedback`.
- What: Section 5.4 (prose-sec-028, page 65): Operate the central feedback mechanism and SOP, provide continuous training and hardware/software maintenance, and monitor efficiency gains, cost savings and health outcomes to inform scale-up.
- Record it: `workflow_complete` with `node: "Task_5_4_FeedbackAndMaintenance"`.
- next: → `GW_MaintenanceUpdate` (Software update needed from roll-out feedback (5.4)?)

### Decide — Software update needed from roll-out feedback (5.4)? (`GW_MaintenanceUpdate`)

- Section 5.4 (prose-sec-028, page 65): Route bugs or enhancement requests back to engineering for software updates and re-verification, or complete the roll-out phase with the live PCPOSS ready for Chapter 6 scale-up.
- Call `workflow_complete` with `node: "GW_MaintenanceUpdate"` and `outcome` set to the label that holds:
  - «apply software update» → `Task_5_2_UpdatePcposs` (5.2 & 5.4 Address feedback, fix bugs & update PCPOSS release)
  - «live PCPOSS stable» → `End_Ch5` (Deployed and rolled-out PCPOSS live in production)

## Done — Deployed and rolled-out PCPOSS live in production (`End_Ch5`)

- The instance completes here: Chapter 5 opener panel outputs complete: Training materials and a deployed and rolled-out PCPOSS in routine production use. `workflow_next` then reports nothing enabled — that, not this line, is the record of completion.
