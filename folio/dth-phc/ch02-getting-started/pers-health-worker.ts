import { persona } from "../../schema/dak";

export default persona({
  label: "pers:health-worker",
  title: "Health worker (clinician, nurse, midwife, community health worker)",
  uses: ["bp:pcposs-implementation-lifecycle", "bp:understand-user-requirements", "bp:design-and-adaptation", "bp:training-testing-and-roll-out", "bp:scale-up"],
  meta: {
  "title": "Health worker (clinician, nurse, midwife, community health worker)",
  "personaType": "person",
  "bpmnRoleId": "health-worker",
  "bpmnLanes": [
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Users",
    "processes/understand-user-requirements.bpmn#Lane-Ch3-Users",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Users",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Users",
    "processes/scale-up.bpmn#Lane-Ch6-Users"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-8d3dd8b68d504c2a9fe8cf414b16c127",
    "elementType": "archimate:Stakeholder",
    "elementName": "Health Workers",
    "elementStatus": "existing",
    "sharedAcross": [
      "dth-phc",
      "dth-hrh",
      "dth-sc",
      "dth-pc",
      "smart-ra"
    ]
  },
  "glossaryTerm": "dth-phc:health-worker",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-004",
      "sec-011",
      "sec-012",
      "sec-013",
      "sec-020",
      "sec-022",
      "sec-025",
      "sec-026",
      "sec-027",
      "sec-029",
      "sec-033"
    ],
    "pdfPages": [
      12,
      25,
      27,
      29,
      50,
      53,
      61,
      62,
      65,
      71,
      79
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "HealthcareProvider; CommunityHealthWorker"
},
});
