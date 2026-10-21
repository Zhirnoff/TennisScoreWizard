# Pro 2.0 / Standalone 2.0 English website staging

Prepared on `feature/website-2-0-en` on 12–13 October 2026. The English pages speak as released 2.0 marketing copy, as requested; the branch itself remains unpublished and is not evidence of App Store approval. The thirteen localized editions on this branch have now been updated to the same 2.0 page structure. Do not merge or publish this branch before the user approves it.

## Narrative order

Keep the established landing-page sequence: product choice, a **single current-release spotlight**, season recaps, Pro history and details, calendar and statistics, manual matches, Match Flow, **Time Machine**, Rivalries, sharing, Watch scoring, comparison, and Help. A compact hero link points to the spotlight without pushing product choice out of the page. Time Machine is additive; do not overwrite the historical 1.8 / 1.11 articles. Product Updates lists 2.0 first and retains every earlier release below it.

## English changes

- Landing page and Help: describe recorded-point Time Machine on iPhone Pro and on both Watch apps; note that manual or older matches without point history cannot be replayed.
- Product Updates: add separate Pro and Standalone 2.0 entries. Pro-only iPhone features remain distinct from standalone Watch behavior.
- Explain progressive set tiles, ordinary tie-break indices without parentheses, Match Tie-Break brackets, and stopped-match leadership based on completed sets and games (not unfinished-game points).
- Update current score, replay, result, and share-card imagery from the Pro 2.0 and Standalone 2.0 simulator builds. Keep older imagery for unchanged setup, manual-entry, recap, context, and statistical workflows where its visible behavior remains accurate.
- Place three click-to-play videos in the spotlight: Watch score-flip footage, Pro iPhone Time Machine, and a 20-second Watch Time Machine replay. Their sound uses the corresponding original app audio asset synchronized to simulator footage. Use local MP4s, static posters, `preload="none"`, inline controls, captions, and no autoplay. Do not equate the decorative heart animation with each measured heartbeat; describe the live numeric heart rate only when a workout is running.
- Preserve the existing section order, navigation, and the entire earlier release history across English and thirteen localized editions. The application source and user match data are not changed by this website branch.

## Screenshot provenance and review

The screenshots in `docs/assets/release-2-0-en/` came from clean feature branches `feature/2.0-pro` and `feature/2.0-standalone`, using dedicated iPhone and Watch simulators and deterministic demonstration matches. The temporary manual-card fixture, if used, is built from a separate disposable clone; it is not in either production application repository. Website-sized iPhone JPEGs derive from original simulator PNG captures. Capture content is demonstrative, not the user's private history.

Reviewed image placements in the English landing page and Product Updates against the changed 2.0 interface. Replace images where the visible score tiles, tie-break notation, progressive sets, or result layout changed; retain unchanged feature screenshots with their established section. On 13 October, the Live Scoring and Rivalries Watch images were refreshed to show Advantage–40 with a 126 BPM reading; the latter was captured by a passing simulator UI test. Manual Match Details links and localized image descriptions were corrected, and changed image URLs were versioned to avoid stale browser caches. Before publication, repeat visual review across small and large phones, narrow and wide Watch, and both appearance sizes. The developer will test physical Apple Watch devices after an app archive.

### Screenshot disposition

| Area | 2.0 treatment |
| --- | --- |
| Pro iPhone home, history, calendar, Stats, Rivalries, and Match Details | New simulator captures with the current interface and demonstration data; manual Match Details uses a readable three-set example. |
| Time Machine | New start, tie-break and final iPhone states plus Pro and Standalone Watch start states, added in the established page order after Match Flow. |
| Live Watch scoring and completed results | New Pro and Standalone captures with progressive set tiles and compact tie-break points; both finished and stopped states are represented. |
| Sharing | New set tie-break, Match Tie-Break and five-set manually entered result cards; ordinary set tie-break points appear without parentheses. |
| Manual Watch history | Replaced an old stopped-result image with a 2.0 screenshot whose equal completed sets and games legitimately display **Stopped · Tied**. |
| Existing setup, season recap, manual editor, context, statistics and complication examples | Retained where the depicted behavior and placement remain valid; earlier release articles stay intact. |

One separate application issue was observed during screenshot generation: the Pro iPhone Match Details set-score table clips its rightmost column for a manually entered five-set **custom** match with two-digit game and tie-break scores on the large iPhone simulator. The exported five-set result card fits. The website therefore uses that five-set case for sharing and a three-set custom example for Match Details; the clipping is not fixed by this website-only branch. Track it before using a five-set manual Match Details image or claiming that screen supports every extreme score cleanly.

Overall Stats and period recap Win Rate now use the same decided-result rule: completed results and stopped matches with a clear leader count as wins or losses; tied stopped matches are neutral. Help explains how the leader is determined from completed sets and current-set games, never unfinished-game points.

## Checks and publication gate

Run `node scripts/test_section_menu.js`, `node scripts/test_back_to_top.js`, `python3 scripts/check_site_locales.py`, and `python3 scripts/test_site_locales.py`. On 13 October the locale check passed for all 52 pages and the 14 locale tests passed. Browser-review the landing page, Help, and Product Updates at desktop and mobile widths, including image loading and overflow, before merging to `main`.

No 2.0 site publication, commit, push, App Store submission, or application release is implied by this staging record.

## 21 October: English editorial and screenshot refresh

This addendum supersedes the current-page copy and media disposition above, not the historical record of the earlier staging work.

- Rewrote all five English pages: landing, Help, Privacy, Product Updates and the UK Pro page. The leading message is “A little retro magic. For every point.” Benefits lead; operational details belong in Help rather than release marketing.
- Preserved the established landing-page sequence and earlier Product Updates entries. New English copy has not been propagated to the thirteen existing localized drafts; they await English approval.
- Help now covers first-match setup, live and saved Time Machine, serve-side perspective, No-Ad guidance, scoring and history notation, stopped results, statistics, Month/Year/All Time, manual results, sharing/import, reports, backups and optional Health access.
- Replaced current app-screen references with real synthetic-demonstration captures from Pro build 75 and Standalone build 53 in `docs/assets/site-refresh-en-20261021/`. Original PNGs and exported JPEGs remain in the task artifacts. Images are resized/compressed without changing the depicted UI. The Files illustration is a crop of its original screen; the provenance manifest records this exception.
- Captured three real exported result cards. Save-to-Photos permission was granted only on the dedicated demonstration iPhone, with explicit user approval. No physical phone or personal photo library was used.
- The manual sharing example now shows 6–4, 6–3 rather than the earlier five-set custom fixture. Watch All Time receives its own year-by-year image, and the Highlights image shows recorded-match highlights rather than a manual result.
- Reused the 20 October, build-74, 30-second landscape Time Machine recording for the English iPhone video. It was compressed for web delivery without changing its UI, with a new poster and English captions. The two Watch videos and two unchanged watch-face complication illustrations remain from the earlier staging assets; they were not newly captured. Older release images remain historical.
- Small English-only layout adjustments improve wrapping and give Watch/iPhone sync illustrations the same 260-pixel image area. No application behavior was changed.

### Verification and remaining gate

The five pages pass the focused English link/asset/anchor checks, and the section-menu and back-to-top checks pass. Desktop (1512 pixels) and narrow mobile (390 pixels) page views show no document-level horizontal overflow. Browser checks include section navigation, return to top, full-resolution image loading and manually started video playback. Three Debug app builds were used for capture; no application test suite was run as part of this website task.

Review locally at `http://127.0.0.1:8877/`. The website remains on `feature/website-2-0-en`, unpublished and uncommitted. English approval, localized-copy/media parity and explicit release authorization are still required before publication. The public checkout and both application repositories are outside this change.

### 21 October follow-up: remaining Watch media and Files visibility

At the user's request, replaced the last two current Watch videos and both complication illustrations in English only. New 30-second recordings show Pro 75 live scoring and a long set tie-break in Time Machine. Each has a new poster, English captions, manual playback and `preload="none"`. The live recording is condensed from 40 seconds to 30; replay remains at real-time speed. Original app click audio is synchronized to recorded actions at application gain, as the simulator's screen recorder has no audio capture. The provenance JSON records processing and original take names.

New real full-face captures show World Time's corner widget and Meridian's circular widget, both explicitly selected as Tennis Score Wizard Pro. World Time applies its own monochrome widget treatment; Meridian shows the green app mark. The original screenshots are retained without UI retouching. These face replacements were subsequently rejected by the user: the English home and Pro page now use the original complication illustrations again. The two new Watch videos remain. Other locales and historical media files remain unchanged.

Also corrected the empty “Take your history with you” illustration reported by the user: the previous long-screen CSS crop still shifted the new pre-cropped image upward by 310 pixels. The English override now uses normal flow, automatic height and responsive width. Verified the actual image is visible in the browser rather than merely present on disk. Updated the English stylesheet cache key. No application source or application tests were changed or run for this follow-up. No commit, push or publication is authorized or performed.

### 21 October follow-up: English audit fixes and authorized localization

Added export, importable backup and recipient-perspective match sharing to the Pro landing page, and explained the actual mechanical-style scoreboard audio in Help. Standardized US spelling on general English pages while retaining UK spelling on the UK landing page. Restored the original historical release descriptions and images; a guard compares all 26 older articles in English and each of the thirteen locales with their baseline text. Historical descriptions are immutable; future changes belong in new entries.

After explicit authorization, transferred the four approved English pages to all thirteen existing locales, including current media, accessibility descriptions and three localized subtitle files per language. Parallel translation work was followed by a source-based semantic audit, correcting inherited shifts between table rows, FAQ questions and answers, and screenshot descriptions. Existing wallet-widget translations and Arabic direction/menu styling were retained. Original complication illustrations remain unchanged. App screenshots intentionally remain authentic English demo captures; surrounding explanations and video captions are localized.

The current local review address is `http://127.0.0.1:8878/`. All 57 pages pass static references/anchors/image/video-policy checks, 52 localized pages match the approved structure, and 18 website regression tests pass. Responsive checks cover 390- and 1512-pixel widths, with targeted visual proof. No application tests, commit, push, merge or publication were performed. User review and explicit release authorization remain the publication gate.

### 21 October follow-up: linguistic review and authorized archive corrections

Reviewed complete connected copy in all thirteen localized editions, including Help, Privacy, current Product Updates, accessibility descriptions and all thirty-nine subtitle files. Corrected confirmed terminology, agreement, literal translations, repeated question fragments, unfinished examples and inline spacing. Product names and UI terminology remain recognizable; no feature behavior or page composition was changed. This was AI linguistic review, not certification by external native-speaking editors.

The user subsequently explicitly authorized correcting the reported language defects in older release descriptions. Applied twenty-three minimal, individually recorded corrections to historical language only; versions, numerical facts and historical feature descriptions were preserved. The historical guard now requires exact agreement with original articles plus this reviewed correction list; unrelated historical edits remain prohibited. All twenty website regression tests, localization parity, static page checks and historical guards pass. Responsive checks again cover all fifty-seven pages at 390 and 1512 pixels. No commit, push, merge or publication was performed.

### 21 October publication authorization

After reviewing the English edition, localized pages and language corrections, the developer explicitly requested publication. Release preparation targets the existing GitHub Pages site at `https://zhirnoff.github.io/TennisScoreWizard/`, built from `main:/docs`; no hosting migration or App Store action is part of this publication. The approved candidate includes all fourteen language editions and the current demonstration media. GitHub's commit, localization check and Pages deployment records provide the authoritative publication outcome.
