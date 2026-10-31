import { prose } from "../../schema/builders";

export default prose({
  label: "prose:annex-12-hepb-schedule-reproduces",
  title: "Annex 12 worked example: Hepatitis B birth-dose vaccination schedule (reproduces WHO Immunization DAK)",
  uses: ["pers:system-dss"],
  meta: {
  "title": "Annex 12 worked example: Hepatitis B birth-dose vaccination schedule (reproduces WHO Immunization DAK)",
  "reproduces": {
    "kind": "reproduces",
    "upstreamDocument": "WHO Digital Adaptation Kit for Immunizations (Immunization DAK / smart-immunizations)",
    "upstreamComponent": "Component 7 \u2014 Scheduling logic: Hepatitis B birth-dose vaccination schedule (`IMMZ.S.HepB`)",
    "templateUsed": "sched:annex-12-scheduling-logic-template"
  },
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-018",
      "sec-044"
    ],
    "pdfPages": [
      46,
      99
    ],
    "method": "p4b-reproduces-link"
  }
},
});
