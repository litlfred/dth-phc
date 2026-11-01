// The harness data that is the same on every page of a build, written ONCE
// here instead of into each page (bean `gp2f`, page weight). Measured on
// gh-pages 1ad53fa, 2026-10-23: the tiles list was 12.5 KB and the navbar icon
// row 2.5 KB of every Jekyll page, about 15 KB of a 42 KB page.
//
// `head_custom.html` keeps the two places the readers look, empty, and loads
// this as the FIRST deferred script. Deferred scripts run in document order,
// so `navbar-row.js` and `docs-ui.js` find them filled, exactly as when the
// data was inlined. If this file does not load, the islands stay named and
// empty, and the readers report a failed load instead of "declared none".
(function () {
  var row = document.getElementById("fa-navbar-row");
  if (row && row.getAttribute("data-fa-row-src") === "harness-data" && !row.textContent) {
    row.textContent = "{\"icons\":[\"close\",\"todos\",\"beans\",\"fsh-guts\",\"qr\",\"launcher\"],\"hrefs\":{\"fsh-guts\":\"https://litlfred.github.io/folio-assistant/en/cat-harness/fsh-guts/\"},\"notes\":{\"beans\":\"no viewer yet\",\"todos\":\"dth-phc's todos graph is not published on this site\"},\"folders\":[{\"kind\":\"archimate\",\"label\":\"Archimate\",\"path\":\"/en/dth-phc/archimate/\"},{\"kind\":\"beans\",\"label\":\"Beans\",\"note\":\"no viewer yet\"},{\"kind\":\"folio\",\"label\":\"Folio\",\"path\":\"/en/dth-phc/\"},{\"kind\":\"fsh-guts\",\"label\":\"FSH guts\",\"stagingOnly\":true,\"path\":\"https://litlfred.github.io/folio-assistant/en/cat-harness/fsh-guts/\"},{\"kind\":\"glossary\",\"label\":\"Glossary\",\"path\":\"/en/folio-assistant-core/glossary/instance/dth-phc/\"},{\"kind\":\"processes\",\"label\":\"Processes\",\"path\":\"https://litlfred.github.io/folio-assistant/en/cat-harness/processes/\"},{\"kind\":\"todos\",\"label\":\"Todos\",\"note\":\"dth-phc's todos graph is not published on this site\"},{\"kind\":\"uploads\",\"label\":\"Uploads\",\"note\":\"dth-phc's uploads graph is not published on this site\"}],\"whose\":{\"fsh-guts\":\"the platform's: dth-phc's fsh-guts graph is not published on this site\"}}";
    row.removeAttribute("data-fa-row-src");
  }
  var tiles = document.querySelector('meta[name="fa-tiles"][data-fa-src="harness-data"]');
  if (tiles && !tiles.getAttribute("content")) {
    tiles.setAttribute("content", "[{\"id\":\"archimate\",\"directory\":\"archimate\",\"title\":\"Archimate\",\"qualifier\":\"Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems\",\"ref\":\"docs/en/dth-phc/archimate/index.html\",\"surfaces\":[\"navbar\",\"board\",\"glass\"],\"hidden\":false},{\"id\":\"folio\",\"directory\":\"folio\",\"title\":\"Working document\",\"qualifier\":\"Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems\",\"ref\":\"en/dth-phc/index.html\",\"surfaces\":[\"navbar\",\"board\",\"glass\"],\"hidden\":false},{\"id\":\"glossary\",\"directory\":\"glossary\",\"title\":\"Glossary\",\"qualifier\":\"Digital Transformation Handbook for Primary Health Care: optimizing person-centred point of service systems\",\"ref\":\"en/folio-assistant-core/glossary/instance/dth-phc/index.html\",\"surfaces\":[\"navbar\",\"board\",\"glass\"],\"hidden\":false}]");
    tiles.removeAttribute("data-fa-src");
  }
})();
