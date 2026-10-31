import { persona } from "../../schema/dak";

export default persona({
  label: "pers:software-engineer",
  title: "Software engineer",
  uses: ["bp:design-and-adaptation", "bp:training-testing-and-roll-out"],
  meta: {
  "title": "Software engineer",
  "personaType": "person",
  "bpmnRoleId": "software-engineer",
  "bpmnLanes": [
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Engineer",
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Tech",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Engineer"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "Software developer / engineer",
    "elementStatus": "proposed-shared-role",
    "relatedComponentIds": [
      "id-3bd1011d76c843fa860255f00a6aa68f"
    ],
    "relatedViewIds": [
      "id-0e97a3f6a8f545f5bd90e123c11a2545",
      "id-b44f768c54ea493c8b33499e5d2e2d33"
    ],
    "sharedAcross": [
      "dth-phc",
      "smart-base",
      "cat-harness"
    ]
  },
  "glossaryTerm": "dth-phc:software-engineer",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-008",
      "sec-020",
      "sec-024",
      "sec-025",
      "sec-027"
    ],
    "pdfPages": [
      19,
      50,
      58,
      63,
      66
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "RelatedSectorServiceProvider"
},
});
