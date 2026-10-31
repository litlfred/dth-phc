import { businessProcess } from "../../schema/dak";

export default businessProcess({
  label: "bp:training-testing-and-roll-out",
  title: "Phase 3: Training, testing and roll-out (Chapter 5)",
  companions: { bpmn: "bp-training-testing-and-roll-out.bpmn" },
  uses: ["pers:public-health-authority", "pers:implementing-team", "pers:technology-partner", "pers:software-engineer", "pers:health-worker", "pers:clerk", "pers:supervisor", "pers:health-service-user"],
  meta: {
  "title": "Phase 3: Training, testing and roll-out (Chapter 5)",
  "processId": "Process_TrainingTestingAndRollOut",
  "canonicalBpmn": "processes/training-testing-and-roll-out.bpmn",
  "canonicalSvg": "processes/training-testing-and-roll-out.svg",
  "checklist": "processes/training-testing-and-roll-out.checklist.md",
  "bpmnSpec": "omg-2013-bpmn-2-0-2",
  "sdlcMapping": "arxiv-2404.04834v4",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-025",
      "sec-026",
      "sec-027",
      "sec-028"
    ],
    "pdfPages": [
      61,
      62,
      65,
      67
    ],
    "method": "p4b-bpmn-formalization"
  }
},
});
