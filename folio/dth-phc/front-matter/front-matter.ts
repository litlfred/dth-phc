import { chapter, section } from "../../schema/builders";

export default chapter({
  title: "Front matter and acknowledgements",
  label: "chap:front-matter",
  sections: [
    section({
      title: "Cover",
      label: "sec:fm-cover",
      lead: true,
      blocks: ["f-fm-cover"],
    }),
    section({
      title: "Publication metadata and contents",
      label: "sec:fm-metadata",
      blocks: ["p-fm-publication-metadata"],
    }),
    section({
      title: "Acknowledgements",
      label: "sec:fm-acknowledgements",
      blocks: ["p-fm-acknowledgements"],
    }),
  ],
});
