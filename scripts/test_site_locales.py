"""Regression tests for the site's English-first localization check."""

import unittest

from check_site_locales import DOCS, SitePage, matching_link, readme_releases


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


if __name__ == "__main__":
    unittest.main()
