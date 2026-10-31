import { chapter, section } from "../../schema/builders";

export default chapter({
  title: "Annexes",
  label: "chap:annexes",
  sections: [
    section({
      title: "Annex 1. Principles for digital development",
      label: "sec:annex-01",
      lead: true,
      blocks: ["p-annex-01-principles"],
    }),
    section({
      title: "Annex 2. Worksheet for semi-structured interviews",
      label: "sec:annex-02",
      blocks: ["t-annex-02-interview-worksheet"],
    }),
    section({
      title: "Annex 3. Observations worksheet",
      label: "sec:annex-03",
      blocks: ["t-annex-03-observations-worksheet"],
    }),
    section({
      title: "Annex 4. User persona worksheet",
      label: "sec:annex-04",
      blocks: ["t-annex-04-user-persona-worksheet"],
    }),
    section({
      title: "Annex 5. User stories worksheet",
      label: "sec:annex-05",
      blocks: ["t-annex-05-user-stories-worksheet"],
    }),
    section({
      title: "Annex 6. Business process matrix guide",
      label: "sec:annex-06",
      blocks: ["t-annex-06-business-process-matrix"],
    }),
    section({
      title: "Annex 7. Form inventory guide",
      label: "sec:annex-07",
      blocks: ["t-annex-07-form-inventory-guide"],
    }),
    section({
      title: "Annex 8. Form data mapping guide",
      label: "sec:annex-08",
      blocks: ["t-annex-08-form-data-mapping-guide"],
    }),
    section({
      title: "Annex 9. Aggregate indicator mapping guide",
      label: "sec:annex-09",
      blocks: ["t-annex-09-indicator-mapping-guide"],
    }),
    section({
      title: "Annex 10. Decision-support logic and scheduling matrix guide",
      label: "sec:annex-10",
      blocks: ["t-annex-10-decision-and-scheduling-matrix"],
    }),
    section({
      title: "Annex 11. Template for a decision-support table",
      label: "sec:annex-11",
      blocks: ["t-annex-11-decision-support-table-template"],
    }),
    section({
      title: "Annex 12. Scheduling logic table guide",
      label: "sec:annex-12",
      blocks: ["t-annex-12-scheduling-logic-guide"],
    }),
    section({
      title: "Annex 13. Prioritization of requirements guide",
      label: "sec:annex-13",
      blocks: ["t-annex-13-prioritization-guide"],
    }),
    section({
      title: "Annex 14. HL7 FHIR standard components",
      label: "sec:annex-14",
      blocks: ["p-annex-14-fhir-components"],
    }),
  ],
});
