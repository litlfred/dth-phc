import { chapter, section } from "../../schema/builders";

export default chapter({
  number: 6,
  title: "Chapter 6. Scale up the system",
  label: "chap:ch06-scale-up",
  sections: [
    section({
      title: "Chapter overview and phase panel",
      label: "sec:ch06-lead",
      lead: true,
      blocks: ["p-ch06-overview", "t-ch06-phase-panel", "bp-scale-up"],
    }),
    section({
      title: "6.1 Determine readiness for scaling up",
      label: "sec:6-1",
      blocks: ["p-ch06-sec-029-readiness-to-scale", "dt-ready-to-scale-up"],
    }),
    section({
      title: "6.2 Plan for phase-out of legacy system(s)",
      label: "sec:6-2",
      blocks: ["p-ch06-sec-030-plan-legacy-phaseout", "t-ch06-table-5"],
    }),
    section({
      title: "6.3 Monitor and evaluate progress on objectives",
      label: "sec:6-3",
      blocks: ["p-ch06-sec-031-monitoring"],
    }),
    section({
      title: "6.4 Phase-out of legacy system(s)",
      label: "sec:6-4",
      blocks: ["p-ch06-sec-032-execute-legacy-phaseout"],
    }),
    section({
      title: "6.5 Adopt change management practices",
      label: "sec:6-5",
      blocks: ["p-ch06-sec-033-change-management"],
    }),
  ],
});
