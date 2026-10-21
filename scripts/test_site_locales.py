"""Regression tests for the site's English-first localization check."""

from html import escape, unescape
import json
import re
import unittest

from check_site_locales import DOCS, LANGUAGES, SitePage, matching_link, readme_releases, release_record_path


def page(html):
    result = SitePage()
    result.feed(html)
    return result


class LocalizationCheckTests(unittest.TestCase):
    def test_missing_badge_is_detected(self):
        english = page('<span class="badge">Match stats</span><span class="badge">Recaps</span>')
        localized = page('<span class="badge">Estadísticas</span>')
        self.assertNotEqual(english.classes, localized.classes)

    def test_missing_card_bullet_is_detected(self):
        english = page('<article id="pro"><ul><li>Watch</li><li>iPhone</li></ul></article>')
        localized = page('<article id="pro"><ul><li>Watch</li></ul></article>')
        self.assertNotEqual(english.card_items, localized.card_items)

    def test_missing_accessibility_label_is_detected(self):
        english = page('<a href="photo.png" aria-label="Open full-size photo">Photo</a>')
        localized = page('<a href="photo.png">Foto</a>')
        self.assertNotEqual(english.aria_sites, localized.aria_sites)

    def test_responsive_image_candidates_are_checked(self):
        parsed = page('<img src="photo-720.webp" '
                      'srcset="photo-720.webp 720w, photo-1080.webp 1080w" alt="Photo">')
        self.assertEqual(parsed.image_candidates,
                         ["photo-720.webp", "photo-1080.webp"])

    def test_video_captions_exist_for_every_locale(self):
        for locale in LANGUAGES:
            parsed = page((DOCS / locale / "index.html").read_text())
            self.assertEqual(len(parsed.video_sources), 3)
            self.assertEqual(len(parsed.caption_tracks), 3)
            self.assertIn("../assets/site-refresh-en-20261021/watch-time-machine-30s.mp4", parsed.video_sources)
            for source, language in parsed.caption_tracks:
                with self.subTest(locale=locale, source=source):
                    self.assertEqual(language, locale)
                    captions = DOCS / locale / source
                    self.assertTrue(captions.is_file())
                    self.assertTrue(captions.read_text().startswith("WEBVTT\n"))

    def test_arabic_page_direction_is_read(self):
        parsed = page('<html lang="ar" dir="rtl"><body>مرحبا</body></html>')
        self.assertEqual((parsed.lang, parsed.direction), ("ar", "rtl"))

    def test_wallet_widget_retains_localized_labels(self):
        for locale in LANGUAGES:
            content = (DOCS / locale / "index.html").read_text()
            for attribute in ("copy-label", "copied-label", "copy-failed-label",
                              "show-qr-label", "qr-code-label", "qr-instruction"):
                with self.subTest(locale=locale, attribute=attribute):
                    match = re.search(r'data-' + attribute + r'="([^"]+)"', content)
                    self.assertIsNotNone(match)
                    if attribute == "copy-label":
                        self.assertNotEqual(match.group(1), "Copy")

    def test_tip_cards_keep_app_store_as_a_store_name(self):
        for locale in LANGUAGES:
            content = (DOCS / locale / "index.html").read_text()
            labels = re.findall(
                r'<span class="development-support-option">[^<]*<strong>([^<]*)</strong>',
                content,
            )
            with self.subTest(locale=locale):
                self.assertEqual(labels, ["App Store"] * 3)

    def test_score_examples_do_not_glue_words_to_digits(self):
        spaced_languages = ("de", "es", "fr", "it", "nl", "pt-BR", "ru", "tr", "ar")
        for locale in spaced_languages:
            for page_name in ("index", "help", "privacy"):
                content = (DOCS / locale / f"{page_name}.html").read_text()
                with self.subTest(locale=locale, page=page_name):
                    self.assertNotRegex(
                        content,
                        r'<span class="score-nowrap">[^<]+</span>[^\W\d_]',
                    )

    def test_arabic_language_picker_opens_into_the_viewport(self):
        css = (DOCS / "release-1-1.css").read_text()
        self.assertRegex(
            css,
            r'html\[dir="rtl"\] \.language-options\s*\{[^}]*'
            r'left:\s*0\s*!important;[^}]*right:\s*auto\s*!important;',
        )
        for page_name in ("index", "whats-new", "help", "privacy"):
            with self.subTest(page=page_name):
                content = (DOCS / "ar" / f"{page_name}.html").read_text()
                self.assertIn('release-1-1.css?v=20261007-rtl-language-menu-2', content)
                self.assertIn('<details class="language-menu">', content)

    def test_localized_link_matches_english_destination(self):
        self.assertTrue(matching_link(
            DOCS / "index.html", DOCS / "es" / "index.html",
            "help.html#period-recaps", "help.html#period-recaps"))

    def test_wrong_store_link_is_detected(self):
        self.assertFalse(matching_link(
            DOCS / "index.html", DOCS / "es" / "index.html",
            "https://apps.apple.com/app/id6789285015",
            "https://apps.apple.com/app/id6782709004"))

    def test_readme_versions_must_follow_english(self):
        self.assertEqual(readme_releases(
            "Current website versions: Pro 1.8 · Standalone 1.11\n"),
            ("Pro 1.8", "Standalone 1.11"))
        self.assertEqual(readme_releases("Old website versions: Pro 1.7"), ())

    def test_current_release_record_uses_current_versions(self):
        self.assertEqual(release_record_path(("Pro 1.8", "Standalone 1.11")).name,
                         "RELEASE-1.8-1.11-WEBSITE.md")

    def test_new_locales_do_not_regress_to_known_literal_translation_errors(self):
        forbidden = {
            "pt-BR": (
                "Standalones", "Histórico de Observação", "os partidas",
                "Atribua uma partida de solteiros", "ALTURAIS DESTAQUES",
                "Rel confiabilidade", "uma partida jogado",
                "Complicações do visor do Apple Watch",
            ),
            "nl": (
                "maand- en jaarcijfers", "wedstrijdvideo's die zijn opgenomen",
                "spelletalletjes", "Gevonden wedstrijden",
                "Spel gespeelde wedstrijden", "Rechtscontext",
                "Optionele ontwikkelingsondersteuning", "beslissingsrondes",
            ),
            "ar": (
                "سجل المشاهدة", "ماذا يفعل السل", "عائلات المضاعفات",
                "المباريات التي لعبتهاا", "ربطة عنق", "خَدَمَ",
                "عَوْدة", "مَسار", "الدورة الشهرية", "نصيحة صغيرة",
                "مراجعة للمحترفين", "مراجعة مستقلة", "دبوس Tennis",
                "مجموعات مزايا ست مباريات", "· السل",
            ),
            "zh-Hant": (
                "雙屏呈現", "網站訪問統計", "鍛鍊可靠性", "許可權",
                "證即時", "將精美卡片釋出", "自願支援開發",
            ),
        }
        for locale, phrases in forbidden.items():
            for page_name in ("index", "whats-new", "help", "privacy"):
                content = (DOCS / locale / f"{page_name}.html").read_text()
                for phrase in phrases:
                    with self.subTest(locale=locale, page=page_name, phrase=phrase):
                        self.assertNotIn(phrase, content)

    def test_watch_time_machine_copy_matches_reviewed_localizations(self):
        translations = json.loads((DOCS.parent / "scripts" / "site_2_0_translations.json").read_text())
        for locale in LANGUAGES:
            content = (DOCS / locale / "index.html").read_text()
            updates = (DOCS / locale / "whats-new.html").read_text()
            data = translations[locale]
            with self.subTest(locale=locale):
                self.assertTrue(f'<h3>{escape(data["spot_replay_title"], quote=False)}</h3>' in content,
                                f"{locale}: spotlight replay title differs from translation source")
                self.assertTrue(f'<p>{escape(data["spot_replay_copy"], quote=False)}</p>' in content,
                                f"{locale}: spotlight replay copy differs from translation source")
                self.assertTrue(f'<h3>{escape(data["tm_watch_title"], quote=False)}</h3>' in content,
                                f"{locale}: Watch replay title differs from translation source")
                self.assertIn(data["updates_pro_media2_caption"], updates)

    def test_awkward_literal_watch_copy_does_not_return(self):
        forbidden = {
            "ru": ("Каждое очко снова на запястье", "Повтор прямо на запястье",
                   "Всё, что вам нужно. Прямо на вашем запястье"),
            "zh-Hans": ("再见那场难忘的比赛",),
            "tr": ("Bileğinizde saklandı.",),
            "ar": ("على كلتا ساعتي التطبيق", "القصة تناسب معصمك"),
        }
        for locale, phrases in forbidden.items():
            for page_name in ("index", "whats-new", "help", "privacy"):
                content = (DOCS / locale / f"{page_name}.html").read_text()
                for phrase in phrases:
                    with self.subTest(locale=locale, page=page_name, phrase=phrase):
                        self.assertNotIn(phrase, content)

    def test_stopped_match_faq_uses_current_rule_without_duplicate(self):
        translations = json.loads((DOCS.parent / "scripts" / "site_2_0_translations.json").read_text())
        for locale in LANGUAGES:
            answer = translations[locale]["help_stopped_a"]
            detail_answer = translations[locale]["help_stopped_detail_a"]
            home = unescape((DOCS / locale / "index.html").read_text())
            help_page = unescape((DOCS / locale / "help.html").read_text())
            history_help = re.search(r'<section id="match-history">.*?</section>', help_page, re.S)
            with self.subTest(locale=locale):
                self.assertIsNotNone(history_help)
                self.assertTrue(f"<p>{answer}</p>" in home,
                                f"{locale}: homepage stopped-match answer differs")
                self.assertTrue(f"<p>{detail_answer}</p>" in history_help.group(),
                                f"{locale}: Help stopped-match answer differs")
                self.assertEqual(history_help.group().count('<div class="help-item">'), 13)

    def test_localized_stat_examples_keep_the_english_numerators(self):
        for locale in ("pt-BR", "nl", "ar", "zh-Hant"):
            content = (DOCS / locale / "index.html").read_text()
            for score in ("3/10", "6/11", "4/11", "6/13"):
                with self.subTest(locale=locale, score=score):
                    self.assertIn(score, content)

    def test_support_email_is_not_translated(self):
        for locale in ("pt-BR", "nl", "ar", "zh-Hant"):
            content = (DOCS / locale / "index.html").read_text()
            self.assertIn("tennisscorewizard@gmail.com", content)


if __name__ == "__main__":
    unittest.main()
