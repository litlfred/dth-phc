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
      blocks: ["p-ch02-sec-007-readiness-scenarios", "dt-starting-scenario"],
    }),
    section({
      title: "2.2 Targeted users",
      label: "sec:2-2",
      blocks: [
        "p-ch02-sec-008-targeted-users",
        "pers-business-analyst",
        "pers-health-informatician",
        "pers-software-engineer",
        "pers-solutions-architect",
        "pers-designer",
        "pers-user-researcher",
        "pers-technology-partner",
        "pers-implementing-team",
        "pers-monitoring-and-evaluation-specialist",
        "pers-public-health-authority",
        "pers-health-worker",
        "pers-clerk",
        "pers-supervisor",
        "pers-health-service-user",
        "pers-system-ehr",
        "pers-system-dss",
        "pers-system-cbis",
        "pers-system-phr",
        "pers-donors-and-development-partners",
      ],
    }),
    section({
      title: "2.3 Before using this resource",
      label: "sec:2-3",
      blocks: ["p-ch02-sec-009-prerequisites", "f-ch02-fig-6", "p-fig-06-diig-reproduces"],
    }),
    section({
      title: "2.4 The stepwise approaches to digitizing",
      label: "sec:2-4",
      blocks: ["p-ch02-sec-010-stepwise-approach", "f-ch02-fig-7", "bp-pcposs-implementation-lifecycle"],
    }),
    section({
      title: "2.5 Choices for software and digital applications",
      label: "sec:2-5",
      blocks: ["p-ch02-sec-011-software-choices"],
    }),
  ],
});
