import { chapter, section } from "../../schema/builders";

export default chapter({
  number: 4,
  title: "Chapter 4. Undertake design and adaptation",
  label: "chap:ch04-design-and-adaptation",
  sections: [
    section({
      title: "Chapter overview and phase panel",
      label: "sec:ch04-lead",
      lead: true,
      blocks: ["p-ch04-overview", "t-ch04-phase-panel", "bp-design-and-adaptation"],
    }),
    section({
      title: "4.1 Finalize software and vendor selection",
      label: "sec:4-1",
      blocks: ["p-ch04-sec-020-vendor-selection"],
    }),
    section({
      title: "4.2 Validate functional requirements",
      label: "sec:4-2",
      blocks: ["p-ch04-sec-021-validate-requirements"],
    }),
    section({
      title: "4.3 Develop and test prototype design",
      label: "sec:4-3",
      blocks: ["p-ch04-sec-022-prototyping", "f-ch04-fig-15"],
    }),
    section({
      title: "4.4 Design system architecture",
      label: "sec:4-4",
      blocks: ["p-ch04-sec-023-architecture-overview", "p-ch04-sec-023-architecture-domains", "t-ch04-table-2", "p-ch04-sec-023-interoperability", "t-ch04-table-3", "p-ch04-sec-023-standards", "t-ch04-table-4"],
    }),
    section({
      title: "4.5 Build and quality assurance",
      label: "sec:4-5",
      blocks: ["p-ch04-sec-024-build-and-qa"],
    }),
  ],
});
