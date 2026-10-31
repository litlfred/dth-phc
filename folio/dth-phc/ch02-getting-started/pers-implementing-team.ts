import { persona } from "../../schema/dak";

export default persona({
  label: "pers:implementing-team",
  title: "Implementing team",
  uses: ["bp:pcposs-implementation-lifecycle", "bp:understand-user-requirements", "bp:design-and-adaptation", "bp:training-testing-and-roll-out", "bp:scale-up", "pers:business-analyst", "pers:health-informatician", "pers:software-engineer", "pers:solutions-architect", "pers:designer", "pers:user-researcher"],
  meta: {
  "title": "Implementing team",
  "personaType": "organisation",
  "bpmnRoleId": "implementing-team",
  "bpmnLanes": [
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Impl",
    "processes/understand-user-requirements.bpmn#Lane-Ch3-BA",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-BA",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Impl",
    "processes/scale-up.bpmn#Lane-Ch6-Impl"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "PCPOSS implementing team",
    "elementStatus": "proposed-role",
    "relatedStakeholderId": "id-1c5c0bc9234e4282b654dbc71b9da706",
    "comprisesRoles": [
      "pers:business-analyst",
      "pers:health-informatician",
      "pers:software-engineer",
      "pers:solutions-architect",
      "pers:designer",
      "pers:user-researcher"
    ]
  },
  "glossaryTerm": "dth-phc:implementing-team",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-007",
      "sec-008",
      "sec-010",
      "sec-011",
      "sec-020",
      "sec-025",
      "sec-029"
    ],
    "pdfPages": [
      17,
      19,
      22,
      25,
      50,
      61,
      71
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "HealthSystemManager"
},
});
