# Pro 1.8 / Standalone 1.11 website update

Website published from `main` on 5 October 2026. This record concerns the public website, not App Store approval or app release status.

## Scope

- The landing page and Product Updates present the month and year recaps for Pro and Standalone. The Watch experience is shown for both apps; Pro also shows the expanded iPhone recap and shareable cards.
- Period comparisons, achievements, weekly and monthly activity, and the existing Match Flow, Momentum, history, export, and backup information appear in the relevant site sections.
- Product Updates contains release descriptions and screenshots. The landing page, Product Updates, Help, and Privacy are maintained in English and nine other languages.
- The top-level README now describes the current website versions. Older release records are kept in this directory without changing their historical version numbers.

## Publication and checks

- `5583227` published the localized season recap and Product Updates content.
- `990cabe` aligned the nine translations with English and introduced localization checks.
- `e47a878` updated the GitHub overview and required its version line to match the English page.
- The localization check passed for all 36 translated pages; six regression tests passed. GitHub Pages deployment and the localization workflow completed successfully for `e47a878`.
- The 36 published translated HTML pages were compared byte-for-byte with the repository files after deployment.

The website's version labels and its publication do not establish that either app build was approved or released in App Store Connect. Verify app status there separately.
