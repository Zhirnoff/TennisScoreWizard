# Pro 1.7 / Standalone 1.10 website release

Branch: `feature/website-match-flow-export-1-7-1-10`

The developer confirmed that both app versions were released. The website release is integrated into `main` and published through GitHub Pages.

## Scope

- Landing page: new Match Flow section above the Pro 1.6 / Standalone 1.9 section, with Momentum, Scores, Key Moments, Watch Momentum, and Pro history export.
- Product Updates: text-only release entries for Pro 1.7 and Standalone 1.10, keeping earlier entries as history.
- Help: point-history availability and history-file export/import guidance.
- Privacy: factual disclosure of stored point sequences and user-initiated report/backup sharing.
- Languages: English, German, Spanish, French, Italian, Japanese, Korean, Russian, Turkish, and Simplified Chinese.

## Screenshot provenance

The new PNG files in `docs/assets/release-1-7-en/` are direct simulator captures from the current UI, not composites or edited sample screens. The Match Flow captures use deterministic recorded-match data from the app UI tests:

| Website asset | Source test capture |
| --- | --- |
| `iphone-momentum.png` | Pro `ManualMatchEntryUITests.testRecordedMatchFlowShowsAllThreeViews`, `/private/tmp/tsw-site-pro-signed-ui.xcresult` |
| `iphone-scores.png` | Same Pro test and result bundle |
| `iphone-key-moments.png` | Same Pro test and result bundle |
| `watch-momentum.png` | Standalone `TennisScore_Watch_AppUITests.testRecordedHistoryShowsCompactMomentum`, `/private/tmp/tsw-site-standalone-signed-ui.xcresult` |
| `pro-watch-momentum.png` | Pro Watch version of the same Watch UI test, `/private/tmp/tsw-site-watch-signed-ui.xcresult` |
| `iphone-history-files.png` | Current Pro Info screen on the iPhone 17 Pro Max iOS 26.5 simulator, showing Match History Files with sample match data |

The source result bundles are local QA artifacts, not tracked in this repository. Captions in localized pages state that app screenshots show the English UI. The Standalone Watch screenshot is used on the landing page; the Pro Watch screenshot is retained for comparison.

## Accuracy and release checks

- Match Flow requires a valid recorded point history. Older results may show it only when sufficient data was saved; manually entered scores never gain fabricated points.
- Pro adds detailed Match Flow on iPhone, a separate shareable Match Flow image/text summary, and CSV/Excel/PDF reports plus restorable JSON/ZIP backups.
- Standalone remains independently playable. Its new Watch History Momentum does not add taps while scoring and it does not have a file importer.
- History imports skip existing match identifiers and do not restore previously deleted identifiers.
- Verify desktop and narrow-screen layout, internal links, local asset paths, localization completeness, and `git diff --check` before merging.
- Do not upload these website screenshots as App Store listing screenshots without separate device-size and listing review.
