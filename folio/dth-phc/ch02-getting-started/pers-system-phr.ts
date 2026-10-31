import { persona } from "../../schema/dak";

export default persona({
  label: "pers:system-phr",
  title: "Personal health record (PHR) system",
  uses: ["bp:design-and-adaptation"],
  meta: {
  "title": "Personal health record (PHR) system",
  "personaType": "system",
  "bpmnRoleId": "system-phr",
  "bpmnLanes": [
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Architect"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:ApplicationComponent",
    "elementName": "Personal health record (PHR)",
    "elementStatus": "proposed-pcposs-component",
    "relatedStakeholderId": "id-a2320dbc07e6450b94f3f0f3e03bb877",
    "relatedComponentIds": [
      "id-0e6d89398fff4f20994a31b4de58e7d7"
    ]
  },
  "glossaryTerm": "dth-phc:personal-health-record",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-003",
      "sec-004",
      "sec-023"
    ],
    "pdfPages": [
      10,
      12,
      56
    ],
    "method": "p4b-persona-formalization"
  }
},
});
