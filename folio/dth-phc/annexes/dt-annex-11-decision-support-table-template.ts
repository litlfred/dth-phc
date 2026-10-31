import { decisionTable } from "../../schema/dak";

export default decisionTable({
  label: "dt:annex-11-decision-support-table-template",
  title: "Annex 11: Decision-support table template and DMN 1.5 column mapping",
  companions: { dmn: "dt-annex-11-decision-support-table-template.dmn" },
  uses: ["pers:business-analyst", "pers:system-dss"],
  meta: {
  "title": "Annex 11: Decision-support table template and DMN 1.5 column mapping",
  "decisionId": "Decision_Annex11DecisionSupportTableTemplate",
  "canonicalDmn": "processes/decisions/annex-11-decision-support-table-template.dmn",
  "dmnSpec": "omg-2024-dmn-1-5",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-017",
      "sec-043"
    ],
    "pdfPages": [
      42,
      43,
      44,
      45,
      98
    ],
    "method": "p4b-dmn-formalization"
  }
},
});
