import { persona } from "../../schema/dak";

export default persona({
  label: "pers:supervisor",
  title: "Supervisor / health facility manager",
  uses: ["bp:understand-user-requirements", "bp:training-testing-and-roll-out", "bp:scale-up"],
  meta: {
  "title": "Supervisor / health facility manager",
  "personaType": "person",
  "bpmnRoleId": "supervisor",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-Users",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Users",
    "processes/scale-up.bpmn#Lane-Ch6-Users"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-515be0d38c564767bc2b1ee5fcb0adb6",
    "elementType": "archimate:Stakeholder",
    "elementName": "Health Care Institutions (Facility manager / supervisor)",
    "elementStatus": "existing",
    "sharedAcross": [
      "dth-phc",
      "dth-hrh",
      "smart-ra"
    ]
  },
  "glossaryTerm": "dth-phc:supervisor",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-004",
      "sec-011",
      "sec-012",
      "sec-025",
      "sec-028",
      "sec-029",
      "sec-032",
      "sec-033"
    ],
    "pdfPages": [
      12,
      25,
      27,
      61,
      67,
      71,
      77,
      79
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "HealthSystemManager"
},
});
