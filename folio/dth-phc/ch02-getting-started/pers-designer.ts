import { persona } from "../../schema/dak";

export default persona({
  label: "pers:designer",
  title: "Designer",
  uses: ["bp:design-and-adaptation"],
  meta: {
  "title": "Designer",
  "personaType": "person",
  "bpmnRoleId": "designer",
  "bpmnLanes": [
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Designer"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "User-experience designer",
    "elementStatus": "proposed-role",
    "relatedComponentIds": [
      "id-3bd1011d76c843fa860255f00a6aa68f"
    ],
    "sharedAcross": [
      "dth-phc"
    ]
  },
  "glossaryTerm": "dth-phc:designer",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-008",
      "sec-020",
      "sec-022"
    ],
    "pdfPages": [
      19,
      50,
      53
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "RelatedSectorServiceProvider"
},
});
