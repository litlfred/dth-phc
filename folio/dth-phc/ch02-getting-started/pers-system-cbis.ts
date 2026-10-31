import { persona } from "../../schema/dak";

export default persona({
  label: "pers:system-cbis",
  title: "Community-based information system (CBIS)",
  uses: ["bp:design-and-adaptation"],
  meta: {
  "title": "Community-based information system (CBIS)",
  "personaType": "system",
  "bpmnRoleId": "system-cbis",
  "bpmnLanes": [
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Architect"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:ApplicationComponent",
    "elementName": "Community-based information system (CBIS)",
    "elementStatus": "proposed-pcposs-component",
    "relatedComponentIds": [
      "id-0e6d89398fff4f20994a31b4de58e7d7"
    ],
    "relatedViewIds": [
      "id-8c5dd12b8d4e425184f6003d0513d569"
    ]
  },
  "glossaryTerm": "dth-phc:community-based-information-system",
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
