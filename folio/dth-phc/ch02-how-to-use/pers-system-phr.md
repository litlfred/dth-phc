# Personal health record (PHR) system

One of the four core application types that make up a PCPOSS (section 1.1, `sec-004`; Glossary, `sec-003`) — a client-facing digital application or messaging interface enabling health service users (`pers:health-service-user`) to view their own health records, receive appointment reminders and targeted health information, and interact with primary care services:

- **Role in the handbook:** Connects health service users directly to their longitudinal health information, immunization schedules and follow-up care plans (1.1, 3.7, 4.4).

## Three-way linkage

1. **BPMN lanes & resources:**
   - Declared as `<bpmn:resource id="pers-system-phr">` in [`pcposs-implementation-lifecycle.bpmn`](https://github.com/litlfred/dth-phc/blob/main/processes/pcposs-implementation-lifecycle.bpmn) and integrated in [`design-and-adaptation.bpmn#Lane-Ch4-Architect`](https://github.com/litlfred/dth-phc/blob/main/processes/design-and-adaptation.bpmn).
2. **Concepts:** [Personal Health Record (PHR)](https://litlfred.github.io/dth-phc/v0/ns/glossary/dth-phc/personal-health-record), [Point-of-service applications](https://litlfred.github.io/smart-ra/v0/ns/glossary/dpi-h-ra/point-of-service-applications)
3. **Glossary term:** `dth-phc:personal-health-record`.
