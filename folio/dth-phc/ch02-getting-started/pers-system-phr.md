# Personal health record (PHR) system

One of the four core application types that make up a PCPOSS (section 1.1, `sec-004`; Glossary, `sec-003`) — a client-facing digital application or messaging interface enabling health service users (`pers:health-service-user`) to view their own health records, receive appointment reminders and targeted health information, and interact with primary care services:

- **Role in the handbook:** Connects health service users directly to their longitudinal health information, immunization schedules and follow-up care plans (1.1, 3.7, 4.4).

## Three-way linkage

1. **BPMN lanes & resources:**
   - Declared as `<bpmn:resource id="pers-system-phr">` in [`pcposs-implementation-lifecycle.bpmn`](../../../processes/pcposs-implementation-lifecycle.bpmn) and integrated in [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](../../../processes/design-and-adaptation.bpmn).
2. **`smart-ra` ArchiMate mapping:** `archimate:ApplicationComponent` **Personal health record (PHR)** on the `smart-ra` PCPOSS view, serving `Patients` (`id-a2320dbc07e6450b94f3f0f3e03bb877`) and synchronising with `SHR Repository` (`id-0e6d89398fff4f20994a31b4de58e7d7`).
3. **Glossary term:** `dth-phc:personal-health-record`.
