import { persona } from "../../schema/dak";

export default persona({
  label: "pers:business-analyst",
  title: "Business analyst",
  uses: ["bp:understand-user-requirements", "bp:design-and-adaptation"],
  meta: {
  "title": "Business analyst",
  "personaType": "person",
  "bpmnRoleId": "business-analyst",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-BA",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Designer"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementType": "archimate:BusinessRole",
    "elementName": "Business analyst",
    "elementStatus": "proposed-shared-role",
    "relatedStakeholderId": "id-1c5c0bc9234e4282b654dbc71b9da706",
    "relatedViewIds": [
      "id-4c98f10e0a244315acddaf5257c7822e",
      "id-3ad41900b17d47f78129e57c7822e"
    ],
    "sharedAcross": [
      "dth-phc",
      "smart-base",
      "cat-harness"
    ],
    "catHarnessRole": "cat-harness/skills/sdlc/crdm/roles/business-analyst.md"
  },
  "glossaryTerm": "dth-phc:business-analyst",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-008",
      "sec-011",
      "sec-013",
      "sec-014",
      "sec-016",
      "sec-020",
      "sec-021"
    ],
    "pdfPages": [
      19,
      25,
      29,
      32,
      41,
      47,
      50,
      52
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "HealthSystemManager"
},
});
