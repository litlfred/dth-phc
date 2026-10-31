import { persona } from "../../schema/dak";

export default persona({
  label: "pers:public-health-authority",
  title: "Public health authority / Ministry of Health (MoH)",
  uses: ["bp:pcposs-implementation-lifecycle", "bp:understand-user-requirements", "bp:training-testing-and-roll-out", "bp:scale-up", "dt:starting-scenario", "dt:requirement-priority", "dt:ready-to-scale-up"],
  meta: {
  "title": "Public health authority / Ministry of Health (MoH)",
  "personaType": "organisation",
  "bpmnRoleId": "public-health-authority",
  "bpmnLanes": [
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-PHA",
    "processes/understand-user-requirements.bpmn#Lane-Ch3-PHA",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-PHA",
    "processes/scale-up.bpmn#Lane-Ch6-PHA"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-1c5c0bc9234e4282b654dbc71b9da706",
    "elementType": "archimate:Stakeholder",
    "elementName": "Ministry of Health",
    "elementStatus": "existing",
    "sharedAcross": [
      "dth-phc",
      "dth-hrh",
      "dth-sc",
      "dth-pc",
      "smart-ra"
    ]
  },
  "glossaryTerm": "dth-phc:public-health-authority",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-006",
      "sec-007",
      "sec-009",
      "sec-011",
      "sec-020",
      "sec-025",
      "sec-029"
    ],
    "pdfPages": [
      15,
      17,
      20,
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
