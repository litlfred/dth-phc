import { businessProcess } from "../../schema/dak";

export default businessProcess({
  label: "bp:pcposs-implementation-lifecycle",
  title: "PCPOSS four-phase implementation lifecycle and agile iteration loop",
  companions: { bpmn: "bp-pcposs-implementation-lifecycle.bpmn" },
  uses: ["dt:starting-scenario", "prose:fig-06-diig-reproduces", "pers:public-health-authority", "pers:implementing-team", "pers:technology-partner", "pers:health-worker", "pers:monitoring-and-evaluation-specialist"],
  meta: {
  "title": "PCPOSS four-phase implementation lifecycle and agile iteration loop",
  "processId": "Process_PcpossImplementationLifecycle",
  "canonicalBpmn": "processes/pcposs-implementation-lifecycle.bpmn",
  "canonicalSvg": "processes/pcposs-implementation-lifecycle.svg",
  "checklist": "processes/pcposs-implementation-lifecycle.checklist.md",
  "bpmnSpec": "omg-2013-bpmn-2-0-2",
  "sdlcMapping": "arxiv-2404.04834v4",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-007",
      "sec-008",
      "sec-009",
      "sec-010"
    ],
    "pdfPages": [
      17,
      18,
      19,
      20,
      21,
      22,
      23
    ],
    "method": "p4b-bpmn-formalization"
  }
},
});
