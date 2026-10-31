import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:requirement-priority",
  title: "Requirement prioritization decision table (section 3.8 and Annex 13)",
  companions: { dmn: "dt-requirement-priority.dmn" },
  uses: ["pers:business-analyst", "pers:implementing-team", "pers:public-health-authority"],
  meta: {
  "title": "Requirement prioritization decision table (section 3.8 and Annex 13)",
  "decisionId": "Decision_RequirementPriority",
  "canonicalDmn": "processes/decisions/requirement-priority.dmn",
  "dmnSpec": "omg-2024-dmn-1-5",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-019",
      "sec-045"
    ],
    "pdfPages": [
      47,
      48,
      100
    ],
    "method": "p4b-dmn-formalization"
  }
},
});
