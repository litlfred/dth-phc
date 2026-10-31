import { persona } from "../../schema/dak";

export default persona({
  label: "pers:technology-partner",
  title: "Technology partner (vendor)",
  uses: ["bp:pcposs-implementation-lifecycle", "bp:design-and-adaptation", "bp:training-testing-and-roll-out"],
  meta: {
  "title": "Technology partner (vendor)",
  "personaType": "organisation",
  "bpmnRoleId": "technology-partner",
  "bpmnLanes": [
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Tech",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Engineer",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Engineer"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:Stakeholder",
    "elementName": "Technology partner / vendor",
    "elementStatus": "proposed-shared-role",
    "relatedComponentIds": [
      "id-3bd1011d76c843fa860255f00a6aa68f"
    ],
    "sharedAcross": [
      "dth-phc",
      "dth-sc",
      "dth-pc",
      "dth-hrh"
    ]
  },
  "glossaryTerm": "dth-phc:technology-partner",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-008",
      "sec-020",
      "sec-024",
      "sec-025",
      "sec-026",
      "sec-027",
      "sec-028"
    ],
    "pdfPages": [
      19,
      50,
      58,
      61,
      63,
      65,
      67
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "RelatedSectorServiceProvider"
},
});
