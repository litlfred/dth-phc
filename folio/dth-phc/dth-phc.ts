import { paper, chapterRef } from "../schema/builders";

/**
 * Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems
 *
 * The document manifest. `chapters` is an ORDERED list: its order is the
 * reading order, and it is the only place that order is recorded.
 *
 * Seeded from who-iris/library/9789240093362-eng and formalized per litlfred/dth-phc#1
 * §3b by scripts/folio/seed_from_l1.py.
 */
export default paper({
  title: "Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems",
  authors: ["World Health Organization"],
  date: "2024",
  meta: {
    documentKind: "smart-base:dth",
    level: "L1",
    targetLevel: "L2",
    isbn: "9789240093362",
    irisHandle: "https://iris.who.int/handle/10665/378469",
    source: { library: "9789240093362-eng", repository: "litlfred/who-iris" },
    licence: "CC BY-NC-SA 3.0 IGO",
    status: "seeded from L1 and formalized per dth-phc#1 §3b; linked to glossary and smart-ra ArchiMate",
  },
  chapters: [
    chapterRef({ dir: "front-matter" }),
    chapterRef({ dir: "ch01-introduction" }),
    chapterRef({ dir: "ch02-how-to-use" }),
    chapterRef({ dir: "ch03-user-requirements" }),
    chapterRef({ dir: "ch04-design-and-adaptation" }),
    chapterRef({ dir: "ch05-training-testing-rollout" }),
    chapterRef({ dir: "ch06-scale-up" }),
    chapterRef({ dir: "annexes" }),
    chapterRef({ dir: "glossary" }),
    chapterRef({ dir: "references" }),
  ],
});
