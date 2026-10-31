import { chapter, section } from "../../schema/builders";

export default chapter({
  number: 5,
  title: "Chapter 5. Conduct training, testing and roll-out",
  label: "chap:ch05-training-testing-rollout",
  sections: [
    section({
      title: "Chapter overview and phase panel",
      label: "sec:ch05-lead",
      lead: true,
      blocks: ["p-ch05-overview", "t-ch05-phase-panel"],
    }),
    section({
      title: "5.1 Develop and conduct training",
      label: "sec:5-1",
      blocks: ["p-ch05-sec-025-training"],
    }),
    section({
      title: "5.2 Test user acceptance and deployment readiness",
      label: "sec:5-2",
      blocks: ["p-ch05-sec-026-uat"],
    }),
    section({
      title: "5.3 Deploy the system",
      label: "sec:5-3",
      blocks: ["p-ch05-sec-027-deploy"],
    }),
    section({
      title: "5.4 Manage feedback and system maintenance",
      label: "sec:5-4",
      blocks: ["p-ch05-sec-028-maintenance"],
    }),
  ],
});
