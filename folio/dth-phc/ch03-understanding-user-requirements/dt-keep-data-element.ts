import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:keep-data-element",
  title: "Data-element minimization decision table (section 3.4.4, Fig. 12)",
  companions: { dmn: "dt-keep-data-element.dmn" },
  uses: ["pers:health-informatician", "pers:monitoring-and-evaluation-specialist"],
  meta: {
  "title": "Data-element minimization decision table (section 3.4.4, Fig. 12)",
  "decisionId": "Decision_KeepDataElement",
  "canonicalDmn": "processes/decisions/keep-data-element.dmn",
  "dmnSpec": "omg-2024-dmn-1-5",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-015"
    ],
    "pdfPages": [
      38,
      39
    ],
    "method": "p4b-dmn-formalization"
  }
},
});
