# Content maintenance

The redesign uses the repository's existing research archive and the career update supplied by Mert on 15 October 2026.

- Greyparrot is the current employer. Mert confirmed his title as Senior Research Engineer, starting October 2026. The location has not been supplied.
- Agendia is a previous employer. The original start year (2023) is retained, and Mert confirmed an end date of October 2026.
- The linked CV is the original PDF and may still describe the earlier career status. It has not been rewritten.
- Publication metadata, author lists, descriptions, links, and patent labels and years are retained from the original site. In particular, the EP4058930A1 patent was labelled “US Patent, 2021”; confirm the jurisdiction and date before correcting it. WO2023117041A1 was labelled “WO Patent, 2022”; its displayed year also needs confirmation.
- The label “Preprint 2023” is retained for the incremental learning survey. No later publication status has been assumed.
- News is visible immediately after the bio. The 2023–2024 news is preserved in an “Earlier news” disclosure within that section.
- All seven original publication entries, four patents, seven supervision records, and 25 photographs remain available. The publication archive is complete relative to the original repository, not a claim about publications since its last update.

## Editing

This is a buildless GitHub Pages site. Edit `index.html` for research and career content, `images.html` for the photography journal, `assets/css/editorial.css` for the shared design tokens and layout, and `assets/js/editorial.js` for the theme preference and publication disclosure behavior. No package installation or build step is required.

## Publication illustrations

All seven publications now have matching SVG concept illustrations in `images/research/`. Each paper appears once in Research with its concept illustration, full metadata, description and resource links. The original paper figures are unchanged and linked below each redraw. Illustration descriptions and primary sources are documented in `images/research/README.md`; `python3 scripts/draw-publications.py` regenerates the complete set without external dependencies.

## ESMO 2026 news

Mert confirmed that Agendia's LBA20, “AI Driven Digital Pathology for the 70 Gene Recurrence Signature: Development and Validation in Early Stage Breast Cancer,” is his paper. The news item links to [Agendia's official announcement](https://agendia.com/agendia-ai-driven-digital-pathology-esmo-2026/), which lists the title, abstract number and 24 October 2026 podium presentation. The full author list and journal/DOI record are not supplied by that announcement, so no bibliographic entry or author metadata has been inferred. The site describes it as work presented at ESMO 2026.

## Research identity

Mert describes himself as an “autonomous vision researcher.” The bio and research introduction frame data curation, continual learning and adaptation to real-time changes as his research goal, rather than claiming these capabilities are already solved or deployed. This wording updates the personal identity, not historical job titles or publication metadata.

## Career navigation

The bio has a direct “Career & education” shortcut and both pages label the main navigation link “Experience.” The career timeline sits after News and before Research, with five roles listed most recent first, preserving the dates, locations, supervisor links and research areas already documented. CV and LinkedIn links sit beside the section introduction. Mert subsequently confirmed the Greyparrot title as Senior Research Engineer and the Agendia end date as October 2026.

## Structured profile and crawler discovery

The homepage includes Schema.org `ProfilePage`, `Person` and `ScholarlyArticle` JSON-LD. It describes the same research identity, current job, education and seven archive publications shown on the page. “Autonomous vision researcher” is the personal research identity; “Senior Research Engineer” is the confirmed Greyparrot job title. They are distinct fields.

`profile.md`, `profile.json`, `llms.txt` and `publications.bib` are generated from the visible HTML by `scripts/build-profile.py`. Career dates retain their original precision, including Agendia's confirmed October 2026 end date. Unknown locations and other absent values are not guessed. The CV remains the existing PDF; the plain-text profile flags its possible lag behind the current homepage. ESMO 2026 is included as news, not an invented full bibliographic entry. Patent labels remain quoted as original labels rather than treated as verified jurisdictions or grant dates.

Canonical and social metadata identify the homepage and photography page. The sitemap lists those two canonical pages without invented freshness dates or priorities. `robots.txt` allows ordinary crawling and points to the sitemap. `llms.txt` is an optional discovery convention; these changes do not guarantee indexing, rankings, or agent recommendations. The visible page remains the source of truth; run `python3 scripts/build-profile.py` after content edits and `--check` to catch stale exports.

## Organization marks

The career timeline uses five matching monochrome SVG marks, including Greyparrot. Agendia, TU/e, QUvA and Huawei are traced from the existing assets, with backgrounds, gradients and small taglines removed. Greyparrot's parrot symbol retains paths from its official website SVG. All original images are unchanged. Sources and regeneration instructions are documented in `images/organizations/README.md`.

## Unified research section

The separate Selected Research and Publications sections are combined into one Research section. All seven archive papers appear once, most recent first, with one consistent image-led layout. Original paper figures remain linked. Individual `publication-1` through `publication-7` anchors are unchanged; the former `#publications` anchor points to the Research section for existing links. Navigation, profile exports, structured metadata and the Markdown profile use the unified section.

## Scrolling and reading flow

The site keeps section navigation visible during long-page reading. On smaller screens the brand scrolls out naturally while the links remain available, without changing the header's layout height mid-scroll. News, Experience, Research, Patents, People and Memories are directly accessible; the current section is indicated without rewriting browser history. Anchors account for the navigation height, and “Back to top” targets an explicit page anchor. Section jumps are immediate while wheel, touch and keyboard scrolling retain browser behavior. No scroll snapping or scroll interception is used.

The pass trims section and entry spacing while retaining the existing body text sizes, all research entries and all photographs. Image dimensions remain explicit and the two local fonts are preloaded to reduce late layout changes. The keyboard skip link focuses the main content. Research profile exports remain identical to their content before this layout pass.
