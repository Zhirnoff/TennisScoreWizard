# Tennis Score Wizard Website

This repository contains the public website, Help Center, Privacy Policy, release notes, and localized product pages for both Tennis Score Wizard products:

- **Standalone** — the complete Apple Watch-only tennis scorekeeper
- **Companion** — the complete Apple Watch app connected to iPhone for synchronized history, calendar views, performance statistics, trends, workout insights, and sharing

This branch prepares the website for **Companion 1.6 (54)** and **Standalone 1.9 (35)**. Manual played matches and editing, optional court context, expanded Match Highlights, richer sharing and Watch history filters are covered in all ten languages. This is an unpublished branch; public release status has not been verified.

Live website: https://zhirnoff.github.io/TennisScoreWizard/

## Repository structure

The GitHub Pages site is stored in `docs/`:

- `docs/index.html` — English landing page
- `docs/help.html` — Help Center
- `docs/privacy.html` — Privacy Policy
- `docs/whats-new.html` — Standalone and Companion release history
- `docs/index.html#rivalries` — English Rivalries feature section on the main page
- `docs/assets/` — app icons, Apple Watch screenshots, Companion screenshots, and optimized image variants
- `docs/de`, `docs/es`, `docs/fr`, `docs/it`, `docs/ja`, `docs/ko`, `docs/ru`, `docs/tr`, `docs/zh-Hans` — localized pages

The site currently supports English, German, Spanish, French, Italian, Japanese, Korean, Russian, Turkish, and Simplified Chinese.

## Coordinated release preparation

- Branch: `feature/website-companion-1-6-standalone-1-9-en`.
- The user reported uploading earlier archives to App Store Connect. Builds 54 / 35 were prepared on 12 September after the Entire year wording check; their upload, approval and public availability have not been verified.
- Keep this multilingual draft unmerged and unpublished until release is confirmed. Public-facing pages use the normal site layout, without preview banners or extra release navigation.
- Updated the landing page, Product Updates, Help and factual Privacy disclosures in all ten languages, plus the existing English UK campaign page. Product Updates stays text-only; historical entries are retained. Screenshots and the complete Match Highlights catalog belong on the main page.
- Shared update styles and navigation behavior: `docs/release-1-6-en.css` and `docs/navigation-en.js`, now loaded by all ten languages. The filenames retain their original English preparation suffix.
- New original app screenshots: `docs/assets/release-1-6-en/`. See [asset provenance and release checklist](RELEASE-1.6-EN.md).
- Localized follow-up: native manual editor and Watch Period screenshots, year/month walkthrough, editing/sync help and updated product comparisons in all ten languages.
- Localized copy includes search/social descriptions, screenshot captions and accessibility labels. Original app screenshots remain in English, with that fact disclosed in translated captions; no app UI or results were redrawn.
- Use polite, formal address consistently across existing and new copy: German Sie, Spanish usted, Italian Lei, Turkish siz, Russian вы and Chinese 您. Keep natural polite wording in French, Japanese and Korean; English does not distinguish formal and informal second-person pronouns. Preserve the exact names of app controls referenced in instructions.

## Local preview

From the repository root, run:

```sh
python3 -m http.server 8000 --directory docs
```

Then open http://localhost:8000/ in a browser. Check desktop and narrow mobile layouts before publishing, and verify at least one page in every localization when shared markup or styling changes.

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
- Prepare website content for an unreleased app version in a dedicated feature or release branch.
- Merge and publish that branch only after the corresponding App Store version is successfully released.
- Keep all ten language versions aligned when product names, versions, links, screenshots, privacy text, or release notes change.
- Website deployments do not require Git release tags by default; application releases are tagged in the Xcode repository.

## App Store

- Standalone: https://apps.apple.com/app/tennis-score-wizard/id6782709004
- Companion: https://apps.apple.com/app/id6789285015

## Support and privacy

For questions, bug reports, or feedback, open a GitHub issue or email tennisscorewizard@gmail.com.

When reporting an app issue, include the device model, operating-system version, app version, steps to reproduce, expected result, and actual result.

Tennis Score Wizard does not require a Tennis Score Wizard account and does not send match history or Rivalry data to a developer-operated server. Companion can transfer match data and a Watch-safe opponent list directly between a paired Apple Watch and iPhone. Companion 1.5 and Standalone 1.8 can also synchronize saved matches and Rivalry library data through the private CloudKit database associated with the user’s Apple Account.
