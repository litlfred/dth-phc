import { businessProcess } from "../../schema/dak";

export default businessProcess({
  label: "bp:understand-user-requirements",
  title: "Phase 1: Understanding user requirements (Chapter 3)",
  companions: { bpmn: "bp-understand-user-requirements.bpmn" },
  uses: ["dt:keep-data-element", "dt:requirement-priority", "prose:fig-10-11-anc-registration-reproduces", "prose:fig-13-hiv-decision-matrix-reproduces", "prose:fig-14-anc-hiv-decision-tree-reproduces", "pers:implementing-team", "pers:business-analyst", "pers:user-researcher", "pers:health-informatician", "pers:monitoring-and-evaluation-specialist", "pers:public-health-authority", "pers:health-worker", "pers:clerk", "pers:supervisor", "pers:health-service-user"],
  meta: {
  "title": "Phase 1: Understanding user requirements (Chapter 3)",
  "processId": "Process_UnderstandUserRequirements",
  "canonicalBpmn": "processes/understand-user-requirements.bpmn",
  "canonicalSvg": "processes/understand-user-requirements.svg",
  "checklist": "processes/understand-user-requirements.checklist.md",
  "bpmnSpec": "omg-2013-bpmn-2-0-2",
  "sdlcMapping": "arxiv-2404.04834v4",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-011",
      "sec-012",
      "sec-013",
      "sec-014",
      "sec-015",
      "sec-016",
      "sec-017",
      "sec-018",
      "sec-019"
    ],
    "pdfPages": [
      25,
      26,
      27,
      29,
      32,
      35,
      41,
      42,
      46,
      47
    ],
    "method": "p4b-bpmn-formalization"
  }
},
});
