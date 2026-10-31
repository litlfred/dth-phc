import { persona } from "../../schema/dak";

export default persona({
  label: "pers:system-ehr",
  title: "Electronic health record (EHR) system",
  uses: ["bp:understand-user-requirements", "bp:design-and-adaptation"],
  meta: {
  "title": "Electronic health record (EHR) system",
  "personaType": "system",
  "bpmnRoleId": "system-ehr",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-HI",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Architect"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-0e6d89398fff4f20994a31b4de58e7d7",
    "elementType": "archimate:ApplicationComponent",
    "elementName": "SHR Repository / Electronic health record (EHR)",
    "elementStatus": "existing-and-pcposs-view",
    "relatedComponentIds": [
      "id-0e6d89398fff4f20994a31b4de58e7d7",
      "id-3bd1011d76c843fa860255f00a6aa68f"
    ],
    "relatedViewIds": [
      "id-cefde7ed0dcd47d3bb214657ac3e5725"
    ]
  },
  "glossaryTerm": "dth-phc:electronic-health-record-system",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-003",
      "sec-004",
      "sec-015",
      "sec-023"
    ],
    "pdfPages": [
      10,
      12,
      36,
      56
    ],
    "method": "p4b-persona-formalization"
  }
},
});
