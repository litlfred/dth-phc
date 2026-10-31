import { persona } from "../../schema/dak";

export default persona({
  label: "pers:solutions-architect",
  title: "Solutions architect",
  uses: ["bp:design-and-adaptation", "bp:scale-up"],
  meta: {
  "title": "Solutions architect",
  "personaType": "person",
  "bpmnRoleId": "solutions-architect",
  "bpmnLanes": [
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Architect",
    "processes/scale-up.bpmn#Lane-Ch6-ME"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "Enterprise / solutions architect",
    "elementStatus": "proposed-shared-role",
    "relatedComponentIds": [
      "id-80856538cbd44167a37b276e38c994c3",
      "id-0e6d89398fff4f20994a31b4de58e7d7",
      "id-539b04ae45f147258d8253ae5cb87402"
    ],
    "relatedViewIds": [
      "id-8c5dd12b8d4e425184f6003d0513d569",
      "id-cefde7ed0dcd47d3bb214657ac3e5725",
      "id-3ad41900b17d47f78129e16d32ed2f38"
    ],
    "sharedAcross": [
      "dth-phc",
      "dth-sc",
      "dth-hrh",
      "smart-ra"
    ]
  },
  "glossaryTerm": "dth-phc:solutions-architect",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-008",
      "sec-020",
      "sec-023",
      "sec-029"
    ],
    "pdfPages": [
      19,
      50,
      56,
      71
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "HealthSystemManager"
},
});
