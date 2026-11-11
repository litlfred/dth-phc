import { chapter, section } from "../../schema/builders";

export default chapter({
  number: 1,
  title: "Chapter 1. Introduction",
  label: "chap:ch01-introduction",
  sections: [
    section({
      title: "Introduction and WHO Digital Guideline Recommendation 8",
      label: "sec:1-0",
      lead: true,
      blocks: ["p-ch01-sec-003-introduction", "t-ch01-fig-1", "f-ch01-fig-1", "rec-who-2019-digital-tracking-decision-support", "t-ch01-fig-2", "f-ch01-fig-2", "p-ch01-sec-003-phc-digital-ecosystem", "f-ch01-fig-3", "p-ch01-sec-003-clerical-burden"],
    }),
    section({
      title: "1.1 Person-centred point of service systems",
      label: "sec:1-1",
      blocks: ["p-ch01-sec-004-pcposs", "f-ch01-fig-4"],
    }),
    section({
      title: "1.2 SMART Guidelines",
      label: "sec:1-2",
      blocks: ["p-ch01-sec-005-smart-guidelines", "f-ch01-fig-5"],
    }),
    section({
      title: "1.3 How this handbook was developed",
      label: "sec:1-3",
      blocks: ["p-ch01-sec-006-how-developed"],
    }),
  ],
});
