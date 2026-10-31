# Implementing team

The multidisciplinary team formed in section 2.2 (`sec-008`) that coordinates and executes all four phases of the PCPOSS implementation lifecycle (Chapters 2–6):

- **Composition (section 2.2):** Brings together the six core specialist roles — [`pers:business-analyst`](pers-business-analyst.ts), [`pers:health-informatician`](pers-health-informatician.ts), [`pers:software-engineer`](pers-software-engineer.ts), [`pers:solutions-architect`](pers-solutions-architect.ts), [`pers:designer`](pers-designer.ts) and [`pers:user-researcher`](pers-user-researcher.ts) — working alongside clinical subject-matter experts, M&E specialists and public health authority leadership.
- **Responsibilities across phases:** Assesses the starting scenario (2.1), aligns with the national digital health strategy (2.3), leads stakeholder engagement (3.1), coordinates requirements prioritization (3.8), conducts software and vendor selection (4.1), develops training plans and UAT test cases (5.1, 5.2), manages production deployment and feedback loops (5.3, 5.4), and executes staged legacy phase-out and change management during scale-up (6.4, 6.5).

## Three-way linkage

1. **BPMN lanes performed:**
   - [`pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Impl`](../../../processes/pcposs-implementation-lifecycle.bpmn) (*Implementing Team*)
   - [`understand-user-requirements.bpmn#Lane-Ch3-BA`](../../../processes/understand-user-requirements.bpmn) (*Implementing Team*)
   - [`design-and-adaptation.bpmn#Lane-Ch4-BA`](../../../processes/design-and-adaptation.bpmn) (*Implementing Team*)
   - [`training-testing-and-roll-out.bpmn#Lane-Ch5-Impl`](../../../processes/training-testing-and-roll-out.bpmn) (*Implementing Team & Trainers*)
   - [`scale-up.bpmn#Lane-Ch6-Impl`](../../../processes/scale-up.bpmn) (*Implementing Team*)
2. **`smart-ra` ArchiMate mapping:** Composite `archimate:BusinessRole` **PCPOSS implementing team** comprising the six section 2.2 core roles under `Ministry of Health` (`id-1c5c0bc9234e4282b654dbc71b9da706`).
3. **Glossary term:** `dth-phc:implementing-team`.
