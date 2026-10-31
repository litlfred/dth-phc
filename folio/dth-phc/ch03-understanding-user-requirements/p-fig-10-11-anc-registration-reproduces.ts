import { prose } from "../../schema/builders";

export default prose({
  label: "prose:fig-10-11-anc-registration-reproduces",
  title: "Figs. 10 and 11. Workflow A: ANC Registration business process and annotations (reproduces WHO ANC DAK)",
  uses: ["pers:health-service-user", "pers:clerk", "pers:health-worker"],
  meta: {
  "title": "Figs. 10 and 11. Workflow A: ANC Registration business process and annotations (reproduces WHO ANC DAK)",
  "reproduces": {
    "kind": "reproduces",
    "upstreamDocument": "WHO Digital Adaptation Kit for Antenatal Care (ANC DAK, 2021, ISBN 9789240020306)",
    "upstreamComponent": "Component 4 \u2014 Business processes and workflows: Workflow A (ANC Registration) diagram and annotation table",
    "swimlanesShown": [
      "Client (pers:health-service-user)",
      "Clerk (pers:clerk)",
      "Health worker / Nurse-Midwife (pers:health-worker)"
    ]
  },
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-014"
    ],
    "pdfPages": [
      33,
      34
    ],
    "method": "p4b-reproduces-link"
  }
},
});
