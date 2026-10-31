import { businessProcess } from "../../schema/dak";

export default businessProcess({
  label: "bp:scale-up",
  title: "Phase 4: Scale-up (Chapter 6)",
  companions: { bpmn: "bp-scale-up.bpmn" },
  uses: ["dt:ready-to-scale-up", "pers:public-health-authority", "pers:monitoring-and-evaluation-specialist", "pers:solutions-architect", "pers:implementing-team", "pers:supervisor", "pers:health-worker", "pers:clerk", "pers:donors-and-development-partners"],
  meta: {
  "title": "Phase 4: Scale-up (Chapter 6)",
  "processId": "Process_ScaleUp",
  "canonicalBpmn": "processes/scale-up.bpmn",
  "canonicalSvg": "processes/scale-up.svg",
  "checklist": "processes/scale-up.checklist.md",
  "bpmnSpec": "omg-2013-bpmn-2-0-2",
  "sdlcMapping": "arxiv-2404.04834v4",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-029",
      "sec-030",
      "sec-031",
      "sec-032",
      "sec-033"
    ],
    "pdfPages": [
      71,
      72,
      74,
      75,
      77,
      79
    ],
    "method": "p4b-bpmn-formalization"
  }
},
});
