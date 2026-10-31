import { persona } from "../../schema/dak";

export default persona({
  label: "pers:clerk",
  title: "Clerk (facility registration and records staff)",
  uses: ["bp:understand-user-requirements", "bp:training-testing-and-roll-out", "bp:scale-up", "prose:fig-10-11-anc-registration-reproduces"],
  meta: {
  "title": "Clerk (facility registration and records staff)",
  "personaType": "person",
  "bpmnRoleId": "clerk",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-Users",
    "processes/training-testing-and-roll-out.bpmn#Lane-Ch5-Users",
    "processes/scale-up.bpmn#Lane-Ch6-Users"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-8d3dd8b68d504c2a9fe8cf414b16c127",
    "elementType": "archimate:BusinessRole",
    "elementName": "Clerk (sub-role of Health Workers / Health Care Institutions)",
    "elementStatus": "proposed-subrole",
    "relatedStakeholderId": "id-8d3dd8b68d504c2a9fe8cf414b16c127",
    "relatedInstitutionId": "id-515be0d38c564767bc2b1ee5fcb0adb6"
  },
  "glossaryTerm": "dth-phc:clerk",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-012",
      "sec-014",
      "sec-026",
      "sec-032"
    ],
    "pdfPages": [
      27,
      33,
      34,
      62,
      77
    ],
    "method": "p4b-persona-formalization"
  },
  "smartBaseGenericPersona": "DataManagerOrRoutineHealthInformationSystemStaff"
},
});
