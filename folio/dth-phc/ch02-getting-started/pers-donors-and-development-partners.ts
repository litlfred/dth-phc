import { persona } from "../../schema/dak";

export default persona({
  label: "pers:donors-and-development-partners",
  title: "Donors, development partners and implementing partners",
  uses: ["bp:pcposs-implementation-lifecycle", "bp:scale-up"],
  meta: {
  "title": "Donors, development partners and implementing partners",
  "personaType": "organisation",
  "bpmnRoleId": "donors-and-development-partners",
  "bpmnLanes": [
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-PHA",
    "processes/scale-up.bpmn#Lane-Ch6-PHA"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:Stakeholder",
    "elementName": "Donors and development partners",
    "elementStatus": "proposed-shared-role",
    "relatedStakeholderId": "id-1c5c0bc9234e4282b654dbc71b9da706",
    "sharedAcross": [
      "dth-phc",
      "dth-sc",
      "dth-pc",
      "dth-hrh"
    ]
  },
  "glossaryTerm": "dth-phc:donors-and-development-partners",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-006",
      "sec-009",
      "sec-011",
      "sec-029"
    ],
    "pdfPages": [
      15,
      20,
      25,
      71
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "HealthSystemManager"
},
});
