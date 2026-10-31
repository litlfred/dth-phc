import { chapter, section } from "../../schema/builders";

export default chapter({
  number: 2,
  title: "Chapter 2. How to use this handbook",
  label: "chap:ch02-how-to-use",
  sections: [
    section({
      title: "2.1 Targeted scenarios of digital readiness",
      label: "sec:2-1",
      lead: true,
      blocks: ["p-ch02-sec-007-readiness-scenarios"],
    }),
    section({
      title: "2.2 Targeted users",
      label: "sec:2-2",
      blocks: ["p-ch02-sec-008-targeted-users"],
    }),
    section({
      title: "2.3 Before using this resource",
      label: "sec:2-3",
      blocks: ["p-ch02-sec-009-prerequisites", "f-ch02-fig-6"],
    }),
    section({
      title: "2.4 The stepwise approaches to digitizing",
      label: "sec:2-4",
      blocks: ["p-ch02-sec-010-stepwise-approach", "f-ch02-fig-7"],
    }),
    section({
      title: "2.5 Choices for software and digital applications",
      label: "sec:2-5",
      blocks: ["p-ch02-sec-011-software-choices"],
    }),
  ],
});
