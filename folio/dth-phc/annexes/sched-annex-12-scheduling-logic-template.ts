import { schedulingLogic } from "../../schema/dak";

export default schedulingLogic({
  label: "sched:annex-12-scheduling-logic-template",
  title: "Annex 12: Scheduling-logic template mapping to smart-base:SchedulingLogic",
  uses: ["pers:business-analyst", "pers:system-dss", "prose:annex-12-hepb-schedule-reproduces"],
  meta: {
  "title": "Annex 12: Scheduling-logic template mapping to smart-base:SchedulingLogic",
  "templateColumns": [
    "Schedule ID / Visit or intervention ID",
    "Title / Activity name",
    "Description",
    "Trigger event (anchor event or observation)",
    "Timing / Ideal window (earliest to latest offset)",
    "Frequency / Recurrence",
    "Due / Overdue / Expiration criteria",
    "Dependencies / Prerequisites (prior dose or visit)",
    "Action when due or overdue (alert, reminder, defaulter tracing)",
    "Reference / Guideline source"
  ],
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-018",
      "sec-044"
    ],
    "pdfPages": [
      46,
      99
    ],
    "method": "p4b-scheduling-logic-template-formalization"
  }
},
});
