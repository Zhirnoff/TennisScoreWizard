#!/usr/bin/env python3
"""Check that localized website pages keep the English page structure."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
from urllib.parse import urlsplit


REPOSITORY = Path(__file__).resolve().parents[1]
DOCS = REPOSITORY / "docs"
LANGUAGES = ("de", "es", "fr", "it", "ja", "ko", "ru", "tr", "zh-Hans")
PAGES = ("index", "whats-new", "help", "privacy")
STRUCTURAL_TAGS = ("section", "article", "h1", "h2", "h3", "a", "li", "img")
STRUCTURAL_CLASSES = ("badge", "version-card", "season-recap-card", "app-store-button")


class SitePage(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tags = Counter()
        self.classes = Counter()
        self.ids = []
        self.images = []
        self.image_alts = []
        self.image_alt_presence = []
        self.links = []
        self.card_items = []
        self._article_stack = []
        self.meta = {}
        self.aria_count = 0
        self.aria_labels = []
        self.aria_sites = []
        self.lang = None
        self.canonical = None
        self.hreflangs = {}

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag in STRUCTURAL_TAGS:
            self.tags[tag] += 1
        for name in attrs.get("class", "").split():
            if name in STRUCTURAL_CLASSES:
                self.classes[name] += 1
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        if attrs.get("aria-label"):
            self.aria_count += 1
            self.aria_labels.append(attrs["aria-label"])
            self.aria_sites.append((tag, tuple(attrs.get("class", "").split())))
        if tag == "html":
            self.lang = attrs.get("lang")
        if tag == "img":
            self.images.append(attrs.get("src", ""))
            self.image_alts.append(attrs.get("alt", ""))
            self.image_alt_presence.append(bool(attrs.get("alt")))
        if tag == "a":
            self.links.append(attrs.get("href", ""))
        if tag == "article":
            self._article_stack.append([attrs.get("id", ""), 0])
        if tag == "li" and self._article_stack:
            self._article_stack[-1][1] += 1
        if tag == "link":
            if attrs.get("rel") == "canonical":
                self.canonical = attrs.get("href")
            if attrs.get("rel") == "alternate" and attrs.get("hreflang"):
                self.hreflangs[attrs["hreflang"]] = attrs.get("href")
        if tag == "meta":
            key = attrs.get("property") or attrs.get("name")
            if key:
                self.meta[key] = attrs.get("content", "")

    def handle_endtag(self, tag):
        if tag == "article" and self._article_stack:
            self.card_items.append(tuple(self._article_stack.pop()))


def parse(path):
    page = SitePage()
    page.feed(path.read_text(encoding="utf-8"))
    return page


def local_target(page_path, url):
    parsed = urlsplit(url)
    if parsed.scheme or parsed.netloc or not parsed.path and not parsed.fragment:
        return None
    target = (page_path.parent / parsed.path).resolve() if parsed.path else page_path
    return target, parsed.fragment


def matching_link(english_path, localized_path, english_href, localized_href):
    english = urlsplit(english_href)
    localized = urlsplit(localized_href)
    if english.scheme or english.netloc or localized.scheme or localized.netloc:
        return english_href == localized_href
    if english.fragment != localized.fragment or english.query != localized.query:
        return False
    english_target = local_target(english_path, english_href)
    localized_target = local_target(localized_path, localized_href)
    if not english_target or not localized_target:
        return english_href == localized_href
    source, _ = english_target
    actual, _ = localized_target
    if actual == source:
        return True  # Language switcher or shared asset.
    return source.is_relative_to(DOCS) and actual == localized_path.parent / source.relative_to(DOCS)


def readme_releases(markdown):
    match = re.search(
        r"^Current website versions: (Pro \d+(?:\.\d+)*) · (Standalone \d+(?:\.\d+)*)$",
        markdown, re.MULTILINE)
    return match.groups() if match else ()


def release_record_path(releases):
    versions = [release.split()[-1] for release in releases]
    return REPOSITORY / "release-history" / f"RELEASE-{versions[0]}-{versions[1]}-WEBSITE.md"


def main():
    parsed = {}
    errors = []
    for old_record in REPOSITORY.glob("RELEASE-*.md"):
        errors.append(f"{old_record}: release records belong in release-history/")

    history_index = REPOSITORY / "release-history" / "README.md"
    if not history_index.is_file():
        errors.append(f"{history_index}: missing release history index")
    else:
        index_text = history_index.read_text(encoding="utf-8")
        for record in (REPOSITORY / "release-history").glob("RELEASE-*.md"):
            if f"({record.name})" not in index_text:
                errors.append(f"{record}: missing from release history index")
    for markdown in (REPOSITORY / "README.md", history_index):
        if not markdown.is_file():
            continue
        for href in re.findall(r"\]\(([^)]+)\)", markdown.read_text(encoding="utf-8")):
            if urlsplit(href).scheme:
                continue
            target = (markdown.parent / urlsplit(href).path).resolve()
            if not target.is_file():
                errors.append(f"{markdown}: broken file link {href}")

    def get(path):
        if path not in parsed:
            parsed[path] = parse(path)
        return parsed[path]

    for name in PAGES:
        english_path = DOCS / f"{name}.html"
        english = get(english_path)
        releases = tuple(re.findall(r"(?:Pro|Standalone) \d+(?:\.\d+)*",
                                    english.meta.get("og:description", "")))
        if name == "index" and len(releases) != 2:
            errors.append(f"{english_path}: expected Pro and Standalone release numbers")
        if name == "index" and readme_releases(
                (REPOSITORY / "README.md").read_text(encoding="utf-8")) != releases:
            errors.append("README.md: current website versions differ from English")
        if name == "index" and len(releases) == 2:
            current_record = release_record_path(releases)
            if not current_record.is_file():
                errors.append(f"{current_record}: missing current website release record")
            elif str(current_record.relative_to(REPOSITORY)) not in (
                    REPOSITORY / "README.md").read_text(encoding="utf-8"):
                errors.append("README.md: missing link to current website release record")
        for lang in LANGUAGES:
            path = DOCS / lang / f"{name}.html"
            if not path.is_file():
                errors.append(f"{path}: missing page")
                continue
            page = get(path)
            for field in ("ids", "tags", "classes", "aria_count", "aria_sites",
                          "image_alt_presence", "card_items", "hreflangs"):
                if getattr(page, field) != getattr(english, field):
                    errors.append(f"{path}: {field} differs from English")
            if page.lang != lang:
                errors.append(f"{path}: expected lang={lang}, got {page.lang}")
            image_paths = [(path.parent / urlsplit(src).path).resolve() for src in page.images]
            english_images = [(english_path.parent / urlsplit(src).path).resolve()
                              for src in english.images]
            if image_paths != english_images:
                errors.append(f"{path}: image set or order differs from English")
            if len(page.links) != len(english.links):
                errors.append(f"{path}: link count differs from English")
            else:
                for index, (source, actual) in enumerate(zip(english.links, page.links), 1):
                    if not matching_link(english_path, path, source, actual):
                        errors.append(f"{path}: link {index} differs from English: {actual}")
            expected_canonical = (f"https://zhirnoff.github.io/TennisScoreWizard/{lang}/"
                                  if name == "index" else
                                  f"https://zhirnoff.github.io/TennisScoreWizard/{lang}/{name}.html")
            if page.canonical != expected_canonical:
                errors.append(f"{path}: incorrect canonical URL")
            if name == "index":
                for key in ("og:description", "twitter:description"):
                    if not all(release in page.meta.get(key, "") for release in releases):
                        errors.append(f"{path}: {key} is missing a current release")
            if page.meta.get("og:image:alt") == english.meta.get("og:image:alt"):
                errors.append(f"{path}: social image description is untranslated")
            for field in ("aria_labels", "image_alts"):
                source_texts = set(getattr(english, field))
                copied = [text for text in getattr(page, field)
                          if len(text) > 20 and text in source_texts]
                if copied:
                    errors.append(f"{path}: untranslated {field}: {copied[0]}")

    for path, page in list(parsed.items()):
        for src in page.images:
            target, _ = local_target(path, src)
            if target and not target.is_file():
                errors.append(f"{path}: missing image {src}")
        for href in page.links:
            if href == "#toggle-goatcounter":  # Handled by analytics.js.
                continue
            result = local_target(path, href)
            if not result:
                continue
            target, fragment = result
            if not target.is_file():
                errors.append(f"{path}: missing link target {href}")
            elif fragment and fragment not in get(target).ids:
                errors.append(f"{path}: missing anchor {href}")

    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    print(f"OK: {len(LANGUAGES) * len(PAGES)} localized pages match English structure and release metadata")


if __name__ == "__main__":
    main()
