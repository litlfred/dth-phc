import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:starting-scenario",
  title: "Starting-scenario classification decision table (section 2.1)",
  companions: { dmn: "dt-starting-scenario.dmn" },
  uses: ["pers:implementing-team", "pers:public-health-authority"],
  meta: {
  "title": "Starting-scenario classification decision table (section 2.1)",
  "decisionId": "Decision_StartingScenario",
  "canonicalDmn": "processes/decisions/starting-scenario.dmn",
  "dmnSpec": "omg-2024-dmn-1-5",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-007"
    ],
    "pdfPages": [
      17,
      18
    ],
    "method": "p4b-dmn-formalization"
  }
},
});
