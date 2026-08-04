# Tennis Score Wizard Website

This repository contains the public website, Help Center, Privacy Policy, release notes, and localized product pages for both Tennis Score Wizard products:

- **Standalone** — the complete Apple Watch-only tennis scorekeeper
- **Companion** — the complete Apple Watch app connected to iPhone for synchronized history, calendar views, performance statistics, trends, workout insights, and sharing

Live website: https://zhirnoff.github.io/TennisScoreWizard/

## Repository structure

The GitHub Pages site is stored in `docs/`:

- `docs/index.html` — English landing page
- `docs/help.html` — Help Center
- `docs/privacy.html` — Privacy Policy
- `docs/whats-new.html` — Standalone and Companion release history
- `docs/assets/` — app icons, Apple Watch screenshots, Companion screenshots, and optimized image variants
- `docs/de`, `docs/es`, `docs/fr`, `docs/ja`, `docs/ru`, `docs/tr`, `docs/zh-Hans` — localized pages

The site currently supports English, German, Spanish, French, Japanese, Russian, Turkish, and Simplified Chinese.

## Local preview

From the repository root, run:

```sh
python3 -m http.server 8000 --directory docs
```

Then open http://localhost:8000/ in a browser. Check desktop and narrow mobile layouts before publishing, and verify at least one page in every localization when shared markup or styling changes.

## Images

Keep original PNG assets as the high-quality source. Where responsive variants exist, preserve the corresponding WebP files and their 720/1080 versions. New image optimization must retain the original aspect ratio and readable UI text.

## Release workflow

- `main` represents the public website and is published through GitHub Pages.
- Prepare website content for an unreleased app version in a dedicated feature or release branch.
- Merge and publish that branch only after the corresponding App Store version is successfully released.
- Keep all eight localized versions aligned when product names, versions, links, screenshots, privacy text, or release notes change.
- Website deployments do not require Git release tags by default; application releases are tagged in the Xcode repository.

## App Store

- Standalone: https://apps.apple.com/app/tennis-score-wizard/id6782709004
- Companion: https://apps.apple.com/app/id6789285015

## Support and privacy

For questions, bug reports, or feedback, open a GitHub issue or email tennisscorewizard@gmail.com.

When reporting an app issue, include the device model, operating-system version, app version, steps to reproduce, expected result, and actual result.

Tennis Score Wizard does not require an account and does not send match history to developer-operated servers. Companion transfers match data directly between the paired Apple Watch and iPhone.
