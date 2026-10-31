import { persona } from "../../schema/dak";

export default persona({
  label: "pers:system-dss",
  title: "Decision-support system (DSS)",
  uses: ["bp:understand-user-requirements", "bp:design-and-adaptation", "dt:annex-11-decision-support-table-template", "sched:annex-12-scheduling-logic-template"],
  meta: {
  "title": "Decision-support system (DSS)",
  "personaType": "system",
  "bpmnRoleId": "system-dss",
  "bpmnLanes": [
    "processes/understand-user-requirements.bpmn#Lane-Ch3-BA",
    "processes/design-and-adaptation.bpmn#Lane-Ch4-Architect"
  ],
  "archimate": {
    "repository": "litlfred/smart-ra",
    "elementId": "id-539b04ae45f147258d8253ae5cb87402",
    "elementType": "archimate:ApplicationComponent",
    "elementName": "Decision Support Engine",
    "elementStatus": "existing",
    "relatedViewIds": [
      "id-4c98f10e0a244315acddaf5257c7822e"
    ]
  },
  "glossaryTerm": "dth-phc:decision-support-system",
  "source": {
    "library": "9789240093362-eng",
    "sections": [
      "sec-003",
      "sec-004",
      "sec-017",
      "sec-018",
      "sec-023",
      "sec-043",
      "sec-044"
    ],
    "pdfPages": [
      10,
      12,
      42,
      46,
      56,
      98,
      99
    ],
    "method": "p4b-persona-formalization"
  }
},
});
