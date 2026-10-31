# Community-based information system (CBIS)

One of the four core application types that make up a PCPOSS (section 1.1, `sec-004`; Glossary, `sec-003`) — a mobile or offline-capable digital system used by community health workers (CHWs) during household visits, community outreach and bidirectional referral with primary care facilities:

- **Role in the handbook:** Supports community-level registration, household enumeration, community case management, defaulters tracing and referral linkage between community health workers and facility-based EHR systems (1.1, 4.4).

## Three-way linkage

1. **BPMN lanes & resources:**
   - Declared as `<bpmn:resource id="pers-system-cbis">` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn) and integrated in [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn).
2. **`smart-ra` ArchiMate mapping:** `archimate:ApplicationComponent` **Community-based information system (CBIS)** on the `smart-ra` PCPOSS view, interoperating with `SHR Repository` (`id-0e6d89398fff4f20994a31b4de58e7d7`) via `Interoperability Component` (`id-80856538cbd44167a37b276e38c994c3`).
3. **Glossary term:** `dth-phc:community-based-information-system`.
