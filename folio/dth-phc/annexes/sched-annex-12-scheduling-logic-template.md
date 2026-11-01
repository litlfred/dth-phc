# Annex 12: Scheduling-logic template mapping to `smart-base:SchedulingLogic`

Formal mapping of the handbook's **Annex 12 Scheduling-logic template** (`sec-044`, section 3.7 `sec-018`) onto `smart-base:SchedulingLogic`.

> **Boundary rule (`litlfred/dth-phc#1` §3b & §3d):** The worked Hepatitis B birth-dose vaccination schedule shown in Annex 12 is an illustrative excerpt from the WHO Immunization Digital Adaptation Kit (DAK) and is recorded separately as a `"reproduces"` link in [`p-annex-12-hepb-schedule-reproduces`](https://github.com/litlfred/dth-phc/blob/main/folio/dth-phc/annexes/p-annex-12-hepb-schedule-reproduces.ts) — never re-extracted as a PHC clinical rule. Only the Annex 12 template structure itself belongs to `dth-phc`.

## Column-by-column mapping from Annex 12 to `smart-base:SchedulingLogic`

| Annex 12 Template Column (`sec-044`) | Purpose in PCPOSS Requirements (Section 3.7) | `smart-base:SchedulingLogic` Field Mapping |
|---|---|---|
| **Schedule ID / Visit or intervention ID** | Unique identifier for the scheduled encounter, immunization dose or follow-up service | `label` (`sched:<slug>`) and `meta.scheduleId` |
| **Title / Activity name** | Human-readable name of the scheduled care activity | `title` |
| **Description** | Clinical/operational description of the scheduled service and target population | Markdown body (`.md`) |
| **Trigger event** | Clinical event, birth, registration or prior encounter that initiates the schedule | `meta.triggerEvent` |
| **Timing / Ideal window** | Recommended target offset and earliest/latest acceptable window relative to the trigger event | `meta.timingWindow` |
| **Frequency / Recurrence** | Number of occurrences and interval between repeat visits or doses | `meta.frequency` |
| **Due / Overdue / Expiration criteria** | Thresholds at which the scheduled activity becomes due, overdue (triggering defaulter tracing) or expired | `meta.dueOverdueCriteria` |
| **Dependencies / Prerequisites** | Prior visits, minimum intervals between doses, or clinical preconditions required | `uses` and `meta.dependencies` |
| **Action when due or overdue** | System action in the DSS / EHR / CBIS / PHR (e.g. task-list prompt, SMS reminder, CHW outreach visit) | `meta.actions` |
| **Reference / Source** | Citation to the WHO clinical guideline or national protocol | `meta.source` |
