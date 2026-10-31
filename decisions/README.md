# DMN 1.5 Decision Tables — Digitalizing Primary Health Care (PCPOSS)

This directory contains the executable DMN 1.5 decision tables (`omg-2024-dmn-1-5`) referenced by `<cat-harness.processes:decision ref="..."/>` gateways in the BPMN 2.0 process models under [`../`](../) and mirrored as `decision-table` (`smart-base:DecisionTable`) blocks in `folio/dth-phc/`.

| DMN File | Decision ID | Hit Policy | Bound Gateway | Handbook Source | Folio Block |
|---|---|---|---|---|---|
| [`starting-scenario.dmn`](starting-scenario.dmn) | `Decision_StartingScenario` | `FIRST` | `GW_StartingScenario` in `pcposs-implementation-lifecycle.bpmn` | Section 2.1 (`sec-007`) | [`dt:starting-scenario`](../../folio/dth-phc/ch02-getting-started/dt-starting-scenario.ts) |
| [`keep-data-element.dmn`](keep-data-element.dmn) | `Decision_KeepDataElement` | `FIRST` | `GW_KeepDataElement` in `understand-user-requirements.bpmn` | Section 3.4.4, Fig. 12 (`sec-015`) | [`dt:keep-data-element`](../../folio/dth-phc/ch03-understanding-user-requirements/dt-keep-data-element.ts) |
| [`requirement-priority.dmn`](requirement-priority.dmn) | `Decision_RequirementPriority` | `FIRST` | `GW_RequirementPriority` in `understand-user-requirements.bpmn` | Section 3.8 (`sec-019`) & Annex 13 (`sec-045`) | [`dt:requirement-priority`](../../folio/dth-phc/ch03-understanding-user-requirements/dt-requirement-priority.ts) |
| [`ready-to-scale-up.dmn`](ready-to-scale-up.dmn) | `Decision_ReadyToScaleUp` | `FIRST` | `GW_ReadyToScaleUp` in `scale-up.bpmn` | Sections 6.1 & 6.2, Table 5 (`sec-029`, `sec-030`) | [`dt:ready-to-scale-up`](../../folio/dth-phc/ch06-scale-up/dt-ready-to-scale-up.ts) |
| [`annex-11-decision-support-table-template.dmn`](annex-11-decision-support-table-template.dmn) | `Decision_Annex11DecisionSupportTableTemplate` | `FIRST` | Template hit-policy selector (`U`, `R`, `F`) | Section 3.6 (`sec-017`) & Annex 11 (`sec-043`) | [`dt:annex-11-decision-support-table-template`](../../folio/dth-phc/annexes/dt-annex-11-decision-support-table-template.ts) |
