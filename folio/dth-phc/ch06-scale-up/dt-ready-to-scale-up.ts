import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:ready-to-scale-up",
  title: "Scale-up readiness decision table (sections 6.1 and 6.2, Table 5)",
  companions: { dmn: "dt-ready-to-scale-up.dmn" },
  uses: ["pers:public-health-authority", "pers:monitoring-and-evaluation-specialist", "pers:solutions-architect", "pers:implementing-team"],
  meta: {
  "title": "Scale-up readiness decision table (sections 6.1 and 6.2, Table 5)",
  "decisionId": "Decision_ReadyToScaleUp",
  "canonicalDmn": "processes/decisions/ready-to-scale-up.dmn",
  "dmnSpec": "omg-2024-dmn-1-5",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-029",
      "sec-030",
      "sec-031"
    ],
    "pdfPages": [
      71,
      72,
      74,
      75
    ],
    "method": "p4b-dmn-formalization"
  }
},
});
