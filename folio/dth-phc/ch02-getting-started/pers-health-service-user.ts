import { persona } from "../../schema/dak";

export default persona({
  label: "pers:health-service-user",
  title: "Health service user (patient / client)",
  uses: ["bp:understand-user-requirements", "bp:design-and-adaptation", "bp:training-testing-and-roll-out", "prose:fig-10-11-anc-registration-reproduces"],
  meta: {
  "title": "Health service user (patient / client)",
  "personaType": "person",
  "bpmnRoleId": "health-service-user",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-Users",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Users",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Users"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-a2320dbc07e6450b94f3f0f3e03bb877",
    "elementType": "archimate:Stakeholder",
    "elementName": "Patients",
    "elementStatus": "existing",
    "sharedAcross": [
      "dth-phc",
      "dth-hrh",
      "smart-ra"
    ]
  },
  "glossaryTerm": "dth-phc:health-service-users",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-003",
      "sec-004",
      "sec-011",
      "sec-012",
      "sec-014",
      "sec-020",
      "sec-022",
      "sec-025"
    ],
    "pdfPages": [
      10,
      12,
      25,
      27,
      33,
      50,
      53,
      61
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "ClientOrPatient; Caregiver"
},
});
