# Tennis Score Wizard Website

<img src="docs/assets/tennis_ball_app_icon_128.png" alt="Tennis Score Wizard app icon" width="72">

[Explore the website](https://zhirnoff.github.io/TennisScoreWizard/) · [Product updates](https://zhirnoff.github.io/TennisScoreWizard/whats-new.html) · [Help](https://zhirnoff.github.io/TennisScoreWizard/help.html) · [Privacy](https://zhirnoff.github.io/TennisScoreWizard/privacy.html)

This repository contains the public website, Help Center, Privacy Policy, release notes, and localized product pages for both Tennis Score Wizard products:

- **Standalone** — the complete Apple Watch-only tennis scorekeeper
- **Pro** — Apple Watch scoring plus an iPhone app for played-match entry, match history, Rivalries, statistics, period recaps, and sharing

Current website versions: Pro 1.8 · Standalone 1.11

The published pages describe month and year recaps on both Watch apps, expanded recaps and shareable cards in Pro on iPhone, period comparisons, achievements, Match Flow and Momentum, and the existing history export and backup tools. Website content and App Store approval are separate; the developer controls app submissions and releases.

Live website: https://zhirnoff.github.io/TennisScoreWizard/

## Repository structure

The GitHub Pages site is stored in `docs/`:

- `docs/index.html` — English landing page
- `docs/help.html` — Help Center
- `docs/privacy.html` — Privacy Policy
- `docs/whats-new.html` — Standalone and Pro release history
- `docs/assets/` — app icons, Apple Watch screenshots, Pro screenshots, and optimized image variants
- `docs/de`, `docs/es`, `docs/fr`, `docs/it`, `docs/ja`, `docs/ko`, `docs/ru`, `docs/tr`, `docs/zh-Hans` — localized pages
- `release-history/` — dated records of past website releases, separate from the current site overview
- `scripts/check_site_locales.py` — English-first checks for localized page structure, links, images, accessibility labels, release metadata, and this README
- `.github/workflows/site-localizations.yml` — runs those checks on site changes

The site currently supports English, German, Spanish, French, Italian, Japanese, Korean, Russian, Turkish, and Simplified Chinese.

## Current site content

- The landing page introduces Pro before Standalone and shows their current website versions, feature comparison, and product screenshots.
- Product Updates includes release details and screenshots for the latest Pro and Standalone versions. Older releases remain in the history.
- Help explains recaps, match history, manual match editing, Match Flow, sharing, and related features. Privacy describes the site's analytics and the apps' data handling.
- All four main pages are available in ten languages. English is the content and structure reference; translations should be natural to native readers while preserving the same facts, links, screenshots, and accessibility information.
- The [website release history](release-history/README.md) keeps implementation and asset provenance, including the [current 1.8/1.11 website record](release-history/RELEASE-1.8-1.11-WEBSITE.md).

## Local preview

From the repository root, run:

```sh
python3 -m http.server 8000 --directory docs
```

Then open http://localhost:8000/ in a browser. Check desktop and narrow mobile layouts before publishing, and verify at least one page in every localization when shared markup or styling changes.

Run the localization checks from the repository root:

```sh
python3 scripts/check_site_locales.py
python3 -m unittest discover -s scripts -p 'test_site_locales.py'
```

## Website analytics

GoatCounter dashboard: https://tennisscorewizard.goatcounter.com/ (login required).
The shared `docs/analytics.js` loads the counter only on the production GitHub
Pages host under `/TennisScoreWizard/`; local previews do not send analytics.
All ten localizations and the promotional landing page use this one loader.

App Store links record separate `app-store-standalone:<page>` and
`app-store-companion:<page>` events. These measure website interactions, not
downloads or purchases. Existing App Store campaign parameters are preserved.

To exclude your visits, use the browser-exclusion link in the website analytics
section of any Privacy page. The setting applies to that browser/profile only;
repeat it on other devices. The same link enables tracking again. No public
visitor counter is displayed. Website analytics is separate from app data.

## Images

Keep original PNG assets as the high-quality source. Where responsive variants exist, preserve the corresponding WebP files and their 720/1080 versions. New image optimization must retain the original aspect ratio and readable UI text.

## Release workflow

- `main` represents the public website and is published through GitHub Pages.
- Start with the English landing page, Product Updates, Help, and Privacy page as needed. Then update all nine translations against those English pages, including metadata and accessibility text.
- Update this README's current website versions and feature summary whenever the site changes. The localization check fails if the version line falls behind the English page.
- Keep release records in `release-history/`, one file per website release. They describe the facts and checks at that time: never rename an old release to the current version or reuse its record. If a past fact needs correction, add a dated correction without erasing the original context.
- The top-level README is the current GitHub overview; move superseded release records out of the repository root and keep their links working. Add a new website release record when publishing a substantive new version.
- Run the automated checks and review the rendered desktop and mobile layouts before committing.
- Prepare unreleased app content on a separate branch by default; publish early only when the developer explicitly requests it. Do not equate website publication with App Store approval.
- After an authorized push to `main`, confirm both the localization workflow and GitHub Pages deployment succeeded, then inspect the live site.
- Website deployments do not require Git release tags by default; application releases are tagged in the Xcode repository.

## App Store

- Standalone: https://apps.apple.com/app/tennis-score-wizard/id6782709004
- Pro: https://apps.apple.com/app/id6789285015

## Support and privacy

For questions, bug reports, or feedback, open a GitHub issue or email tennisscorewizard@gmail.com.

When reporting an app issue, include the device model, operating-system version, app version, steps to reproduce, expected result, and actual result.

Tennis Score Wizard does not require a Tennis Score Wizard account and does not send match history or Rivalry data to a developer-operated server. Pro can transfer match data and a Watch-safe opponent list directly between a paired Apple Watch and iPhone. Current Pro and Standalone releases can also synchronize saved matches and Rivalry library data through the private CloudKit database associated with the user’s Apple Account.
