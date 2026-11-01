import { chapter, section } from "../../schema/builders";

export default chapter({
  number: 3,
  title: "Chapter 3. Understand user requirements",
  label: "chap:ch03-user-requirements",
  sections: [
    section({
      title: "Chapter overview and phase panel",
      label: "sec:ch03-lead",
      lead: true,
      blocks: ["p-ch03-overview", "t-ch03-phase-panel", "bp-understand-user-requirements"],
    }),
    section({
      title: "3.1 Follow key requirement-gathering methods",
      label: "sec:3-1",
      blocks: ["p-ch03-sec-012-methods", "p-ch03-sec-012-interviews-and-workshops", "f-ch03-fig-8"],
    }),
    section({
      title: "3.2 Get to know the users",
      label: "sec:3-2",
      blocks: ["p-ch03-sec-013-personas", "p-ch03-sec-013-use-cases-and-stories"],
    }),
    section({
      title: "3.3 Map business processes and workflows",
      label: "sec:3-3",
      blocks: ["p-ch03-sec-014-workflows", "t-ch03-table-1", "f-ch03-fig-9", "f-ch03-fig-10", "f-ch03-fig-11", "p-fig-10-11-anc-registration-reproduces"],
    }),
    section({
      title: "3.4 Streamline data collection and indicator reporting",
      label: "sec:3-4",
      blocks: ["p-ch03-sec-015-streamline-data-and-indicators", "t-ch03-fig-12", "f-ch03-fig-12", "dt-keep-data-element"],
    }),
    section({
      title: "3.5 Create a data dictionary",
      label: "sec:3-5",
      blocks: ["p-ch03-sec-016-data-dictionary"],
    }),
    section({
      title: "3.6 Determine decision-support logic",
      label: "sec:3-6",
      blocks: ["p-ch03-sec-017-decision-support-logic", "f-ch03-fig-13", "p-fig-13-hiv-decision-matrix-reproduces", "f-ch03-fig-14", "p-fig-14-anc-hiv-decision-tree-reproduces"],
    }),
    section({
      title: "3.7 Map health service schedules",
      label: "sec:3-7",
      blocks: ["p-ch03-sec-018-schedules"],
    }),
    section({
      title: "3.8 Gather and prioritize requirements",
      label: "sec:3-8",
      blocks: ["p-ch03-sec-019-requirements", "dt-requirement-priority"],
    }),
  ],
});
