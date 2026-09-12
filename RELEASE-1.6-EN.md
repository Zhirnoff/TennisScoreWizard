# Website release preparation — Companion 1.6 / Standalone 1.9

Prepared 10 September 2026 on `feature/website-companion-1-6-standalone-1-9-en`.

## Release gate

This is a multilingual draft on a release-preparation branch, not a published announcement. The initial English changes were translated on 11 September; the manual-editing and Watch-history follow-up was extended to the other nine languages on 12 September. The user reported uploading earlier archives to App Store Connect; Apple approval and public availability have not been verified. Do not merge into `main` or publish until the user confirms the release and approves the website update.

- Initial screenshot baseline: Companion 1.6 (52), commit `a66bb6db2b2ac196656d8d46286a4ff028e8af88`, and Standalone 1.9 (33), commit `8282f89cb371b2230778bda03117ecafad61dbe0`.
- English follow-up baseline: Companion 1.6 (53) and Standalone 1.9 (34), prepared on 11 September after prerelease checks. On 12 September, after checking Entire year in both apps, the archive build numbers were increased to Companion 1.6 (54) and Standalone 1.9 (35). The older commits above do not include these later changes. Build preparation is not evidence of an archive upload, Apple approval or public availability.
- Website branch is separate from both app release branches. No app source or release tags are changed here.

## 12 September — localized follow-up and formal address

- Manual-match editing, synchronized corrections and Watch History year/month filters are now covered in all ten languages on the landing page, Help and Product Updates, including search/social descriptions and screenshot accessibility text.
- Existing and new website copy uses formal, polite address. German, Spanish, Italian and Turkish copy was aligned throughout all four page types; isolated informal Russian and Chinese wording was corrected as well. English, French, Japanese and Korean were reviewed for consistency. Exact app control names and the original English app screenshots remain intact.
- Historical release facts, product behavior, links and analytics remain unchanged by the tone correction. Two long comparison headings were shortened for 320 px screens.
- Static validation: 41 pages and 1,942 local references, with no missing files, missing anchors or duplicate IDs. Original screenshot hashes match the native QA sources; `git diff --check` passes.
- Browser validation: 40 localized pages at 320, 390, 768 and 1440 px, 160 checks without document overflow or clipped headings/body copy after the fixes. Screenshots in `output/playwright/formal-*.png` are local, ignored QA artifacts.
- App handoff commits: Companion `c36b55b` (1.6 build 54), Standalone `4d0c70b` (1.9 build 35), pushed to their respective feature branches. Both unsigned Release device builds passed; application, Watch and complication version metadata agree. This does not represent new archives or App Store uploads.
- Website push is to the preparation branch only. GitHub Pages remains configured to publish `main:/docs`; no main merge or public release is part of this handoff.

## 11 September — English-only follow-up: manual editing and Watch History

At this stage, the 11 September follow-up updated English only. The nine translated versions retained the previous approved draft until the 12 September localization recorded above. Shared localized styles and original image assets were unchanged at this stage.

- Landing page: a manual-match editing block and a three-card Watch History walkthrough; refreshed History images, version comparison and manual-match FAQ.
- Product Updates: manual editing and synchronized corrections folded into the main played-match feature; year/month history browsing added for both Watch apps. Previous releases remain unchanged, with no screenshot gallery or release-preview banner.
- Help: editing scope, synchronization, corrected-history comparisons, year/month filters and progressive loading. The score editor cannot modify a Watch-recorded score or change match type/players; assignment and context have separate controls.
- English UK campaign: updated feature copy and a native editor screenshot. Existing pricing and campaign links are preserved.
- Privacy reviewed: editing and filtering introduce no additional data category or location permission beyond the existing manual-match/context disclosures. No privacy wording changed in this follow-up.

Five new native PNGs were copied unchanged from the latest app QA captures. They contain test data, not real-world customer matches. The on-screen sync badge is part of a test fixture, not proof of live iCloud synchronization. Native sizes: phone 1320 × 2868; Watch 416 × 496. Watch images display at no more than 200 CSS pixels and remain inside individual promotional cards.

| New asset in `docs/assets/release-1-6-en/` | Original native QA capture |
| --- | --- |
| manual-edit-form.png | `/tmp/tsw-preflight-phone-captures/5A1202C8-EC2B-491A-B0CC-42FB25843166.png` |
| manual-edit-details.png | `/tmp/tsw-preflight-phone-captures/8D76E986-376D-4BBB-B29F-B42A057BCB14.png` |
| watch-history-period.png | `/tmp/tsw-preflight-companion-captures/63EAD0DE-6952-4F18-B8BB-E4EE291658CC.png` |
| watch-history-years.png | `/tmp/tsw-preflight-companion-captures/C337F2F1-824C-4024-962C-5A2E7D9F2DFA.png` |
| watch-history-months.png | `/tmp/tsw-preflight-standalone46-final-captures/01D31D14-3D34-4E30-B86E-A472A56E1023.png` |

Follow-up validation on 11 September:

- Browser layout checks: landing page, Help, Product Updates, Privacy and UK campaign at 320, 390, 768 and 1440 px. Document width matched viewport width in all 20 checks. Existing mobile screenshot carousels intentionally scroll inside their own containers.
- Rendered and inspected the new editor and Watch History sections at desktop and mobile sizes, plus the mobile Companion release article. Product Updates contains no screenshot images.
- Static check: 205 local references across the five pages, with no missing files, missing anchors or duplicate IDs. `git diff --check` passed.
- All five new PNG hashes match their native QA originals. Hash comparison also confirms the 36 translated HTML files were unchanged during this follow-up.
- Two broader browser interaction/resource probes were interrupted (process exit 137); they are not counted as passed. Local references were checked separately on disk. Live iCloud sync, production deployment and external App Store availability are outside this website check.
- Browser captures: `output/playwright/en-edit-played-match-{320,390,1440}.png`, `en-watch-history-{320,390,1440}.png` and `en-product-updates-390.png`. These local QA artifacts are ignored by Git.
- No commit, push, merge or publication was performed. The local preview remains on port 8765.

SHA-256 of new native assets:

```text
bcce00de0bea513697f1c495d742c0aed2e35e699f2e66aa56e8ed78a19a3794  manual-edit-form.png
a409128672dcb0d4ec460e4a9437ab27efffe35e6a59e59e608b84c03ce92c5b  manual-edit-details.png
3c9d5c8289630a46af4be264bf2dc7c7c10ce1f5302662765cd0dbb802848828  watch-history-period.png
7f04d90bb5aba5753b48ba40b5e4fb991fd3983c8187afc339a20830088b8b8c  watch-history-years.png
99e137e98cd11280e1cb44c48cfe0a29bf0fa65d28aeb8063521d03bc467368a  watch-history-months.png
```

### 12 September wording follow-up

The Watch period option is now **Entire year** in both app worktrees and the English landing page/Help. The accessibility identifier remains `history-period-whole-year`, so filtering and UI-test selectors are unchanged. The existing period UI test now also checks the displayed wording.

The landing page uses `watch-history-months-entire-year.png` (416 × 496), copied unchanged from `/tmp/tsw-entire-year-standalone-captures/C7913788-0457-4D36-9741-BB4CBDD0BAD5.png`, captured by the native Standalone UI test on 46 mm. SHA-256: `6fe97b2b6198f949ec5226a244e2beadccb459b95344e9ae665345a85117ab7a`. The previous screenshot is retained as historical source material; translated pages are unchanged.

Both app targets built successfully. `testHistoryPeriodFiltersAndReset` passed for Standalone and Companion on 40 mm and 46 mm (four successful runs), including the new wording assertion. Results: `/tmp/tsw-entire-year-standalone-20260912.xcresult` and `/tmp/tsw-entire-year-companion-20260912.xcresult`. The screenshot shows the full label without truncation. The 205 local website references still resolve. This was a targeted copy/UI check, not another full prerelease regression.

The wording check used Companion 53 / Standalone 34. After that check, the user authorized increasing the build numbers to 54 / 35 and committing/pushing the app and website branches. Marketing versions remain 1.6 / 1.9. No archive, App Store upload, main-branch merge or website publication is part of this handoff.

## English content prepared

- Landing page: manual played matches; optional court context; expanded Match Highlights; up to six highlights on shared cards; manual-entry Watch history. Retains the existing scoring, Rivalries, statistics, calendar and support sections.
- Product Updates: separate Companion 1.6 and Standalone 1.9 entries. Previous release articles are retained. Per the 11 September review, Product Updates is text-only; screenshot galleries are on the landing page. Headlines describe meaningful product changes; time entry and keyboard details are supporting details, not standalone release features.
- Help: manual entry, stopped/tied results, tie-break entry, remembered timing and midnight, direct field taps and keyboard navigation, available statistics, sync, court reuse, privacy and supported highlights.
- Privacy: factual disclosures about manually entered match/context data, local account-scoped favorite courts and what appears on a shared image.
- UK English campaign page: same major benefits and original screens. Existing campaign parameters, pricing and analytics code are preserved; price was not revalidated in this task.
- Initially prepared in English; the 11 September localization stage below extends the approved changes and shared update styles/navigation to all ten languages. The existing English-only UK campaign remains English-only.

## Product boundaries reflected in the copy

- Manual entry and the court/context editor are iPhone features, not a live iPhone scoreboard.
- Manual results can sync to Watch history. They are labeled Added manually and do not invent missing point-by-point, serve/return, break-point or Health measurements.
- Match Highlights appear in iPhone details and exported images, not Watch history. Details show all qualifying events; sharing prioritizes up to six. There are 26 possible event types, not 26 guaranteed cards.
- Records and milestones describe the saved history, not a verified entire playing career.
- Court conditions and location appear on shared images; personal match and Rivalry notes do not.
- Court context is optional descriptive information and does not generate statistical achievements.
- Court names are entered manually, without Maps/GPS lookup. Favorites remain local to the iPhone and account-scoped.

## Original screenshot provenance

All nine PNGs were copied byte-for-byte from actual application QA screenshots or native app-generated share images. They contain **demonstration/test match data**, not verified real-world customer matches. No score, duration, highlight, icon or app UI was drawn or replaced for the website. Display uses proportional CSS sizing and lazy loading; full-resolution PNG sources are retained.

Local QA source root:
`/Users/Mikhail_Zhirnov/.codex/.chatgpt-projects/g-p-6a390305947081918b11f17df0ff84b0/artifacts/release-qa-2026-09-10`.

Public destination root: `docs/assets/release-1-6-en/`.

| Website PNG | QA source under the root above | Native size |
| --- | --- | --- |
| manual-score.png | phone-large/8736563A-D05A-4C72-B1CF-23754F83BC12.png | 1320 × 2868 |
| court-conditions.png | phone-large/00F0B5DD-83D4-43AE-92F3-0B044E5DDE21.png | 1320 × 2868 |
| favorite-court.png | phone-large/59A176A5-58DE-4938-94F3-B2CD8E1FF314.png | 1320 × 2868 |
| match-highlights.png | phone-large/D102C96D-A83E-42EF-AF23-DAEDAF6EBF33.png | 1320 × 2868 |
| share-recorded-context.png | phone-large/3CE1ADEF-F317-48D7-904A-1CBC347E9167.png | 1080 × 1937 |
| share-custom-score.png | phone-large/C4B678E9-0EB7-421F-AB30-E35C74E7D042.png | 1080 × 924 |
| watch-manual-history.png | standalone-49/5D7CB33E-CB5E-4ACA-9B86-8AB7102ECCF4.png | 422 × 514 |
| manual-match-form.png | phone-large/08DCF979-EA39-450A-8D01-92238E0967A1.png | 1320 × 2868 |

### Complete Match Highlights catalog

Added after the user's 11 September review: `all-match-highlights.png`, 2160 × 1501, copied unchanged from `phone-large/934AA8EE-C3EF-4FAC-B57E-73BAF802828B.png` under the same QA source root.
The manifest identifies `AdditionalMatchHighlightsTests/testAllHighlightVisualVariantsCatalog()`. The app's native sharing-card renderer displays 26 types and 44 examples from separate scenarios, explicitly not one match. The latest QA version includes the recorded-history wording corrections.

SHA-256: `934a30b7494e05b6d7dd3e733e87f9b06a99b54e86ee361b014e6558ddf6392b`.

### Data integrity

The `share-recorded-context.png` example comes from the app's existing Watch-recorded demo fixture, enriched with court context by `MatchContextTests.swift`. Its original five-set score and **3 h 2 min** duration are retained. The test verifies that applying context does not change recorded score, duration or workout data; the image uses the app's own Match Highlights presentation and share renderer.

The `share-custom-score.png` export is a manually added five-Custom-Set example. Its double-digit games and tie-break values are the app's actual output, with only supported highlights and no fabricated point/workout measurements.

SHA-256, checked against the QA originals:

```text
25334493b92b8c459b3027e89b92c4eb21e5c9cc243e8c22d9f946e1644d00e0  manual-score.png
750ff705615f3bb0ba932c918ab999ffc93f8265a4c1c41bb3cc3f616e8d86d9  court-conditions.png
6c8ee55460c24bcc1d577682ce25965d499cd52a46bc66c124839f7124668650  favorite-court.png
06c023b3d08b8d1c0f7b57e95e02a9f91df342a1c40bc1a631440ffd42977946  match-highlights.png
49ce7de887d1a8920612541e0ee3f8709a5acd93dbca4cea27cf28bef87ec733  share-recorded-context.png
94c8a3a459fafac368513f141ca800b8c055f42bd1e4822dbd96cfeb0319b121  share-custom-score.png
36c8bdd19846be6c569a6749d5163c9413581fde3dca9e6d330467cb92453da8  watch-manual-history.png
6b5e019fe348c8ea430f823ceb1c5c7347e2df9250c8366caf505e4340ee46f6  manual-match-form.png
```

## Website validation

11 September review: visitor-facing release-preview banners, metadata wording and extra release links removed from all five English pages. Product Updates contains no screenshots; existing release-note bullet points are retained. Added the native complete Highlights catalog to the main page. Existing five-highlight and two-highlight match-share examples are retained without duplicate cards.

Rechecked all five pages at 320, 390, 768 and 1440 CSS pixels: no document overflow or release-preview wording. New main-page assets retain their aspect ratios; Product Updates content contains zero images. Revised captures use `*-revised.png` in `output/playwright/`.

- Local Chromium preview on 320, 390, 768 and 1440 CSS-pixel widths: all five updated English pages have no document-level horizontal overflow.
- Existing horizontally scrolling galleries on the main page are retained; new release cards are not horizontal carousels.
- New images decode successfully. Native aspect ratios are preserved, including the corrected campaign-page image sizing.
- New Watch image is displayed at no more than 200 CSS pixels wide, inside its own promotional card.
- No duplicate IDs or missing local files in the five edited pages. The existing `#toggle-goatcounter` hash is an intentional analytics action handled by `analytics.js`, not a missing document section.
- Browser captures are in the ignored `output/playwright/` directory. They are local review artifacts, not public assets.
- This is website QA. It does not replace the app's release tests or an end-to-end physical-device/iCloud check.

### Final English copy and layout audit — 11 September

- Reviewed all five English pages against the current Companion source for manual entry, match outcomes and Highlights. Corrected stopped-match copy: compare completed sets, then the current unfinished set and recorded points; do not sum earlier games to determine the leader.
- Added manual Match Tie-Break and interrupted set tie-break instructions. Clarified one-to-five-set support, optional timing, missing statistics and the distinction between Stats results and completed-win streak/milestone Highlights.
- Updated the Help overview and English metadata; replaced awkward or ambiguous English without adding unsupported features. Surface/place remain descriptive context, not achievement criteria; notes remain private.
- Fixed actual line splits inside numeric score examples using the English-only `score-nowrap` utility. Preserve this utility when adapting the approved content to other languages.
- Responsive geometry check: five pages at 320, 375, 390, 430, 768, 1024 and 1440 CSS pixels (35 combinations), with no document overflow or split numeric score examples. Additional text-clipping checks at 320, 390, 768 and 1440 found no clipped text blocks.
- Rendered and inspected representative mobile and desktop screenshots after the copy corrections: feature cards, manual-entry Help and the latest Product Updates article. Captures are `output/playwright/audit-final-*.png`. Browser testing used local Chromium, not physical iPhones or Safari.
- Clicking the Highlights catalog opens the original 2160 × 1501 image in a new tab. No extra full-size text link is displayed.
- Final local link/anchor and duplicate-ID checks passed. All 87 pre-existing Product Updates bullet points are retained. No public release-preview copy returned; other language pages and shared existing assets remain untouched.

Translation baseline: keep Match Highlights terminology consistent; distinguish Completed from Stopped, and manually entered scores from Watch-recorded point/workout data. Do not translate “location” as automatic GPS tracking. Keep release headlines focused on major benefits, with timing and keyboard details under manual match entry.

### Navigation feedback — 11 September

- English primary navigation now uses consistent green pill feedback for activation and the current page. Hover alone does not leave a touch link green; keyboard focus remains visible.
- `navigation-en.js` clears transient activation and restored link focus on history return, including same-page anchor history. Help and Product Updates retain their correct current-page indication on their own pages; the homepage has no current-page link.
- Verified Compare, Help and Product Updates click/Back flows and repeated them with Chromium mobile/touch emulation. All links returned to white on the homepage. Desktop Back and keyboard-focus checks passed.
- Checked all four English primary headers at 320, 390, 768, 1024 and 1440 CSS pixels (20 combinations): no clipped links or links outside the header. Screenshots: `output/playwright/nav-mobile-compare-selected.png`, `nav-mobile-after-back.png`, `nav-desktop-help-selected.png`.
- This interaction change is still English-only; include the script and styles when localizing the approved pages. No physical iOS Safari test is claimed.

## Localization — 11 September

- Personally authored natural-language adaptations for German, Spanish, French, Italian, Japanese, Korean, Russian, Turkish and Simplified Chinese: 36 pages across the landing page, Help, Privacy and Product Updates. No external translation service was used.
- Translated new features, revised existing descriptions and FAQs, comparison rows, release articles, captions, image alt text, accessibility labels and search/social descriptions. Local navigation and Help links remain within their language; canonical/hreflang links remain intact.
- All 87 previous Product Updates bullet points in each locale remain unchanged. Product Updates is text-only; feature screenshots and the clickable 26-type / 44-example catalog follow the approved homepage design.
- Shared update styles and navigation behavior now load in every language. The `-en` filenames are retained for continuity, not to imply English-only scope.
- Original English app screenshots and native exports are reused byte-for-byte. Translated captions disclose English UI and demonstration data; no scores, durations, images or app labels were fabricated.
- Shortened a few Russian and German comparison cells for the narrowest layout. Kept numeric score examples together next to Japanese/Korean text and preserved Korean word boundaries where space permits.
- Playwright/Chromium checks: 36 localized pages at 320, 390, 768, 1024 and 1440 CSS pixels (180 page/width combinations). Separate checks found no document overflow, overflowing tested labels/cells, or hidden vertically clipped text. All 20 Korean page/width combinations were rechecked after the final word-boundary refinement.
- Navigation: 27 real click/Back scenarios (Compare, Help and Product Updates in each language) returned every homepage link to white after its 150 ms color transition. No physical Safari test is implied.
- Static checks passed for local files/anchors, required feature sections, duplicate IDs, comparison/share-card structure and preservation of historical release-note bullets.
- Rendered and inspected mobile feature cards and latest Product Updates in every locale, plus representative desktop comparisons, the Russian feature grid and Russian/Japanese Help. Local captures: `output/playwright/i18n-<locale>-mobile.png`, `i18n-<locale>-comparison.png`, `i18n-<locale>-updates.png`, `i18n-ru-features.png`, `i18n-ru-help.png` and `i18n-ja-help.png`. These are ignored review artifacts, not public website assets.
- The English-only audit entries above describe the earlier stage, not the current multilingual scope. No physical-device Safari or new app/iCloud test is claimed by this website localization task.

## Before publication

1. English content/layout approval received; obtain review of the localized update.
2. Translations are prepared in all nine additional languages. Keep their content aligned with any further approved English corrections.
3. Confirm App Store approval **and actual public availability** for both exact versions/builds. Do not present a submitted build as available.
4. Recheck versions, App Store links and UK campaign pricing. Do not reintroduce preview banners or extra release-navigation links: the 11 September review requests the site's usual public-facing layout. Publication remains gated by branch/workflow, not by visitor-facing preview notices.
5. Finish any outstanding app release checks, especially real-device iCloud/manual-match synchronization; do not claim a new physical-device check from this website task.
6. Re-run links, responsive layout and image checks after localization. Consider lossless delivery optimization for the large original iPhone PNGs, keeping originals and exact visual content.
7. Only after explicit authorization: commit/push the website branch and merge/publish. Verify the live pages after deployment. Do not create website release tags by default.
