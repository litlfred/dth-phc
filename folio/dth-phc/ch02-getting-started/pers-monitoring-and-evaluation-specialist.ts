import { persona } from "../../schema/dak";

export default persona({
  label: "pers:monitoring-and-evaluation-specialist",
  title: "Monitoring and evaluation (M&E) specialist",
  uses: ["bp:understand-user-requirements", "bp:scale-up", "dt:ready-to-scale-up"],
  meta: {
  "title": "Monitoring and evaluation (M&E) specialist",
  "personaType": "person",
  "bpmnRoleId": "monitoring-and-evaluation-specialist",
  "bpmnLanes": [
    "processes/pcposs-implementation-lifecycle.bpmn#Lane-Lifecycle-Impl",
    "processes/understand-user-requirements.bpmn#Lane-Ch3-HI",
    "processes/scale-up.bpmn#Lane-Ch6-ME"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "M&E specialist",
    "elementStatus": "proposed-shared-role",
    "relatedComponentIds": [
      "id-3fd92d497ca040c8a436f355c0b68770"
    ],
    "sharedAcross": [
      "dth-phc",
      "dth-sc",
      "dth-hrh"
    ]
  },
  "glossaryTerm": "dth-phc:monitoring-and-evaluation-specialist",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-011",
      "sec-015",
      "sec-029",
      "sec-030",
      "sec-031"
    ],
    "pdfPages": [
      25,
      35,
      71,
      74,
      75
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "DataManagerOrRoutineHealthInformationSystemStaff"
},
});
