import { businessProcess } from "../../schema/dak";

export default businessProcess({
  label: "bp:design-and-adaptation",
  title: "Phase 2: Design and adaptation (Chapter 4)",
  companions: { bpmn: "bp-design-and-adaptation.bpmn" },
  uses: ["pers:implementing-team", "pers:business-analyst", "pers:designer", "pers:user-researcher", "pers:solutions-architect", "pers:health-informatician", "pers:software-engineer", "pers:technology-partner", "pers:health-worker", "pers:health-service-user"],
  meta: {
  "title": "Phase 2: Design and adaptation (Chapter 4)",
  "processId": "Process_DesignAndAdaptation",
  "canonicalBpmn": "processes/design-and-adaptation.bpmn",
  "canonicalSvg": "processes/design-and-adaptation.svg",
  "checklist": "processes/design-and-adaptation.checklist.md",
  "bpmnSpec": "omg-2013-bpmn-2-0-2",
  "sdlcMapping": "arxiv-2404.04834v4",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-020",
      "sec-021",
      "sec-022",
      "sec-023",
      "sec-024"
    ],
    "pdfPages": [
      50,
      51,
      52,
      53,
      56,
      58
    ],
    "method": "p4b-bpmn-formalization"
  }
},
});
