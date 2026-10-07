"""Regression tests for the site's English-first localization check."""

import unittest

from check_site_locales import DOCS, SitePage, matching_link, readme_releases, release_record_path


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

    def test_arabic_page_direction_is_read(self):
        parsed = page('<html lang="ar" dir="rtl"><body>مرحبا</body></html>')
        self.assertEqual((parsed.lang, parsed.direction), ("ar", "rtl"))

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
