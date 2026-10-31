import { persona } from "../../schema/dak";

export default persona({
  label: "pers:health-informatician",
  title: "Health informatician",
  uses: ["bp:understand-user-requirements", "bp:design-and-adaptation", "dt:keep-data-element"],
  meta: {
  "title": "Health informatician",
  "personaType": "person",
  "bpmnRoleId": "health-informatician",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-HI",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Architect"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "Health informatician",
    "elementStatus": "proposed-shared-role",
    "relatedComponentIds": [
      "id-3f41de2b51c24041b08243bf72b140d1",
      "id-c0d39bf67fe64f54b07fbeb9bf37d404"
    ],
    "relatedViewIds": [
      "id-8c5dd12b8d4e425184f6003d0513d569",
      "id-cefde7ed0dcd47d3bb214657ac3e5725"
    ],
    "sharedAcross": [
      "dth-phc",
      "dth-hrh",
      "smart-base"
    ]
  },
  "glossaryTerm": "dth-phc:health-informatician",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-008",
      "sec-011",
      "sec-015",
      "sec-020",
      "sec-023"
    ],
    "pdfPages": [
      19,
      25,
      36,
      50,
      56
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "DataManagerOrRoutineHealthInformationSystemStaff"
},
});
