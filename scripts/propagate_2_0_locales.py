#!/usr/bin/env python3
"""Apply reviewed 2.0 structure and hand-written copy to existing locale pages.

This intentionally retains the previously translated site and historical releases.
It fails before writing if a locale is missing any required copy or the expected
English/locale structure has drifted.
"""

import argparse
from html import escape
import json
from pathlib import Path
import re
import subprocess


ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
LOCALES = ("de", "es", "fr", "it", "ja", "ko", "ru", "tr", "zh-Hans", "pt-BR", "zh-Hant", "nl", "ar")
DATA = Path(__file__).with_name("site_2_0_translations.json")
MATCH_DETAILS_ALTS = {
    "ru": "Детали пятисетового матча, записанного часами: счёт, Time Machine и хайлайты",
    "de": "Details eines auf der Watch aufgezeichneten Matches über fünf Sätze mit Ergebnis, Time Machine und Highlights",
    "fr": "Détails d’un match en cinq sets enregistré sur la Watch, avec score, Time Machine et temps forts",
    "es": "Detalles de un partido a cinco sets registrado con el Watch, con marcador, Time Machine y momentos destacados",
    "it": "Dettagli di un incontro in cinque set registrato su Watch, con punteggio, Time Machine e momenti salienti",
    "pt-BR": "Detalhes de uma partida de cinco sets registrada no Watch, com placar, Time Machine e destaques",
    "nl": "Details van een op de Watch vastgelegde wedstrijd in vijf sets, met score, Time Machine en hoogtepunten",
    "tr": "Watch ile kaydedilen beş setlik maçın skor, Time Machine ve öne çıkan anları içeren ayrıntıları",
    "ja": "Watchで記録した5セットの試合詳細。スコア、Time Machine、ハイライトを表示",
    "ko": "Watch로 기록한 5세트 경기의 점수, Time Machine과 하이라이트가 보이는 상세 화면",
    "zh-Hans": "Watch 记录的五盘比赛详情，包含比分、Time Machine 和精彩瞬间",
    "zh-Hant": "Watch 記錄的五盤比賽詳情，包含比分、Time Machine 和精彩瞬間",
    "ar": "تفاصيل مباراة من خمس مجموعات سُجلت على الساعة، مع النتيجة وTime Machine واللحظات البارزة",
}


def one(pattern, text, label):
    matches = list(re.finditer(pattern, text, re.S))
    if len(matches) != 1:
        raise ValueError(f"{label}: expected one match, found {len(matches)}")
    return matches[0]


def replace_one(pattern, replacement, text, label):
    match = one(pattern, text, label)
    if "\\g<" in replacement:
        replacement = match.expand(replacement)
    return text[:match.start()] + replacement + text[match.end():]


def element(source, tag, element_id):
    start = one(rf'<{tag}\b[^>]*\bid="{re.escape(element_id)}"[^>]*>', source, element_id)
    depth = 1
    for match in re.finditer(rf'</?{tag}\b[^>]*>', source[start.end():], re.I):
        depth += -1 if match.group().startswith("</") else 1
        if depth == 0:
            return source[start.start():start.end() + match.end()]
    raise ValueError(f"unterminated {element_id}")


def attr(tag, name, value):
    quoted = escape(value, quote=True)
    if re.search(rf'\b{re.escape(name)}="[^"]*"', tag):
        return re.sub(rf'\b{re.escape(name)}="[^"]*"', f'{name}="{quoted}"', tag, count=1)
    return tag[:-1] + f' {name}="{quoted}">'


def remove_attr(tag, name):
    return re.sub(rf'\s+{re.escape(name)}="[^"]*"', "", tag)


def media_path(path):
    return "../" + path if path.startswith("assets/") else path


def media_srcset(value):
    return ", ".join(media_path(candidate.strip().split()[0]) +
                     (" " + " ".join(candidate.strip().split()[1:]) if len(candidate.strip().split()) > 1 else "")
                     for candidate in value.split(","))


def sync_tags(local, english, tag, names):
    source_tags = re.findall(rf'<{tag}\b[^>]*>', english, re.I)
    local_tags = list(re.finditer(rf'<{tag}\b[^>]*>', local, re.I))
    if len(source_tags) != len(local_tags):
        raise ValueError(f"{tag} count: English {len(source_tags)}, locale {len(local_tags)}")
    replacements = []
    for match, source in zip(local_tags, source_tags):
        current = match.group()
        if tag == "a":
            source_href = re.search(r'\bhref="([^"]*)"', source)
            if source_href and source_href.group(1).startswith("assets/"):
                current = attr(current, "href", media_path(source_href.group(1)))
        else:
            for name in names:
                source_attr = re.search(rf'\b{re.escape(name)}="([^"]*)"', source)
                current = (attr(current, name, media_srcset(source_attr.group(1)) if name == "srcset" else
                                media_path(source_attr.group(1)) if name == "src" else source_attr.group(1))
                           if source_attr else remove_attr(current, name))
        replacements.append((match.start(), match.end(), current))
    for start, end, replacement in reversed(replacements):
        local = local[:start] + replacement + local[end:]
    return local


def replace_meta(text, kind, key, value):
    if kind == "name":
        pattern = rf'<meta\b(?=[^>]*\bname="{re.escape(key)}")[^>]*>'
    else:
        pattern = rf'<meta\b(?=[^>]*\bproperty="{re.escape(key)}")[^>]*>'
    match = one(pattern, text, key)
    return text[:match.start()] + attr(match.group(), "content", value) + text[match.end():]


def translate(lang, data, key):
    if key not in data:
        raise KeyError(f"{lang}: missing {key}")
    return escape(data[key], quote=True)


def fill_defaults(data):
    """Derive concise, localized accessibility text from reviewed visible copy."""
    data.setdefault("spot_label", data["updates_h1"])
    data.setdefault("meta_home", data["spot_intro"])
    data.setdefault("meta_home_og", "Pro 2.0 · Standalone 2.0: " + data["spot_intro"])
    data.setdefault("meta_home_social", data["spot_label"])
    data.setdefault("meta_updates", data["spot_intro"])
    data.setdefault("meta_updates_og", data["spot_label"])
    data.setdefault("meta_updates_social", data["spot_label"])
    data.setdefault("hero_label", data["tm_new"])
    data.setdefault("badge", data["spot_detail_link"])
    data.setdefault("spot_watch_label", "01 · Apple Watch · " + data["tm_watch_label"])
    data.setdefault("spot_phone_label", "02 · Time Machine · Pro · iPhone")
    data.setdefault("tm_scope", data["tm_watch_label"] + " · Pro · iPhone")
    data.setdefault("tm_watch_link", data["spot_detail_link"])
    data.setdefault("watch_finish", data["tm_finish_title"])
    data.setdefault("updates_pro_title", data["tm_title"])
    data.setdefault("updates_pro_intro", data["spot_intro"])
    data.setdefault("updates_pro_b1_title", data["tm_title"])
    data.setdefault("updates_pro_b1_copy", data["tm_intro"])
    data.setdefault("updates_pro_b2_title", data["spot_watch_title"])
    data.setdefault("updates_pro_b2_copy", data["spot_watch_copy"])
    data.setdefault("updates_pro_b6_title", data["share_result_title"])
    data.setdefault("updates_pro_b6_copy", data["share_intro"])
    data.setdefault("updates_standalone_b1_title", data["tm_watch_title"])
    data.setdefault("updates_standalone_b1_copy", data["tm_watch_copy"])
    data.setdefault("updates_standalone_b2_title", data["updates_pro_b3_title"])
    data.setdefault("updates_standalone_b2_copy", data["updates_pro_b3_copy"])
    data.setdefault("updates_standalone_b3_title", data["spot_watch_title"])
    data.setdefault("updates_standalone_b3_copy", data["spot_watch_copy"])
    data.setdefault("updates_standalone_b4_title", data["updates_pro_b5_title"])
    data.setdefault("updates_standalone_b4_copy", data["updates_pro_b5_copy"])
    data.setdefault("updates_tm_link", data["spot_detail_link"])
    data.setdefault("spot_watch_alt", data["spot_watch_title"] + " · Apple Watch")
    data.setdefault("spot_phone_alt", data["spot_phone_title"] + " · Time Machine")
    data.setdefault("spot_replay_alt", data["spot_replay_title"] + " · Apple Watch Time Machine")
    data.setdefault("watch_video_link", data["spot_watch_title"])
    data.setdefault("phone_video_link", data["spot_phone_title"])
    for key in ("start", "break", "finish"):
        data.setdefault("tm_" + key + "_aria", data["tm_" + key + "_title"])
        data.setdefault("tm_" + key + "_alt", data["tm_" + key + "_title"] + " · Time Machine")
    data.setdefault("tm_watch_aria", data["tm_watch_title"])
    data.setdefault("tm_watch_alt", data["tm_watch_title"] + " · Apple Watch")
    for key in ("result", "match", "manual"):
        data.setdefault("share_" + key + "_aria", data["share_" + key + "_title"])
        data.setdefault("share_" + key + "_alt", data["share_" + key + "_title"] + " · Pro 2.0")
    data.setdefault("updates_pro_gallery_alt", data["updates_pro_title"] + " · Pro 2.0")
    data.setdefault("updates_standalone_gallery_alt", data["updates_standalone_title"] + " · Standalone 2.0")
    for key, title in (("updates_pro_media1", "tm_break_title"), ("updates_pro_media2", "tm_watch_title"), ("updates_pro_media3", "watch_finish"),
                       ("updates_standalone_media1", "spot_watch_title"), ("updates_standalone_media2", "tm_watch_title"), ("updates_standalone_media3", "watch_finish")):
        data.setdefault(key + "_caption", data[title])
        data.setdefault(key + "_alt", data[title] + " · " + ("iPhone" if key == "updates_pro_media1" else "Apple Watch"))
    data.setdefault("updates_tm_link", data["spot_detail_link"])
    return data


def make_fragments(lang, data):
    q = lambda key: translate(lang, data, key)
    hero = f'''<a class="release-hero-teaser" href="#latest-2-0">
  <strong>{q("hero_label")}</strong>
  <span class="release-hero-teaser-copy">{q("hero_copy")}</span>
  <span class="release-hero-teaser-action"><span class="release-hero-teaser-play" aria-hidden="true"><svg viewBox="0 0 12 12" focusable="false"><path d="M2 1.5 10 6 2 10.5Z"/></svg></span>{q("hero_action")}</span>
</a>'''
    spotlight = f'''<section id="latest-2-0" class="release-spotlight" aria-labelledby="latest-2-0-title">
  <div class="release-spotlight-heading"><span class="release-spotlight-kicker">{q("spot_label")}</span><h2 id="latest-2-0-title">{q("spot_title")}</h2><p>{q("spot_intro")}</p></div>
  <div class="release-spotlight-grid">
    <article class="release-spotlight-card"><span>{q("spot_watch_label")}</span><h3>{q("spot_watch_title")}</h3><p>{q("spot_watch_copy")}</p>
      <video controls playsinline preload="none" loading="lazy" poster="../assets/release-2-0-en/watch-score-video-poster.png" width="416" height="496" aria-label="{q("spot_watch_alt")}"><source src="../assets/release-2-0-en/watch-score-flip.mp4" type="video/mp4"><track kind="captions" src="../assets/release-2-0-en/watch-score-flip.{lang}.vtt" srclang="{lang}" label="{q("language_name")}">{q("video_fallback")} <a href="../assets/release-2-0-en/watch-score-flip.mp4">{q("watch_video_link")}</a></video>
    </article>
    <article class="release-spotlight-card"><span>{q("spot_phone_label")}</span><h3>{q("spot_phone_title")}</h3><p>{q("spot_phone_copy")}</p>
      <video controls playsinline preload="none" loading="lazy" poster="../assets/release-2-0-en/iphone-time-machine-video-poster.png" width="1920" height="1080" aria-label="{q("spot_phone_alt")}"><source src="../assets/release-2-0-en/iphone-time-machine.mp4" type="video/mp4"><track kind="captions" src="../assets/release-2-0-en/iphone-time-machine.{lang}.vtt" srclang="{lang}" label="{q("language_name")}">{q("video_fallback")} <a href="../assets/release-2-0-en/iphone-time-machine.mp4">{q("phone_video_link")}</a></video>
    </article>
    <article class="release-spotlight-card"><span>{q("spot_replay_label")}</span><h3>{q("spot_replay_title")}</h3><p>{q("spot_replay_copy")}</p>
      <video controls playsinline preload="none" loading="lazy" poster="../assets/release-2-0-en/watch-time-machine-video-poster.png" width="416" height="496" aria-label="{q("spot_replay_alt")}"><source src="../assets/release-2-0-en/watch-time-machine.mp4" type="video/mp4"><track kind="captions" src="../assets/release-2-0-en/watch-time-machine.{lang}.vtt" srclang="{lang}" label="{q("language_name")}">{q("video_fallback")} <a href="../assets/release-2-0-en/watch-time-machine.mp4">Time Machine</a></video>
    </article>
  </div>
  <div class="release-spotlight-links"><a href="whats-new.html">{q("spot_all_link")} →</a><a href="#time-machine">{q("spot_detail_link")} →</a></div>
</section>'''
    tm_cards = []
    for index, key, photo in ((1,"start","iphone-time-machine-start.jpg"),(2,"break","iphone-time-machine-tiebreak.jpg"),(3,"finish","iphone-time-machine-final.jpg")):
        tm_cards.append(f'''<article class="release-next-card"><span class="release-card-number">0{index} · {q("tm_"+key+"_label")}</span><h3>{q("tm_"+key+"_title")}</h3><p>{q("tm_"+key+"_copy")}</p><a href="../assets/release-2-0-en/{photo}" target="_blank" rel="noopener" aria-label="{q("tm_"+key+"_aria")}"><img src="../assets/release-2-0-en/{photo}" alt="{q("tm_"+key+"_alt")}" width="900" height="1955" loading="lazy" decoding="async"></a></article>''')
    time_machine = f'''<section id="time-machine" class="release-next" aria-labelledby="time-machine-title">
  <div class="release-next-heading"><div class="release-next-kicker"><span>{q("tm_new")}</span><span>{q("tm_scope")}</span></div><h2 id="time-machine-title">{q("tm_title")}</h2><p>{q("tm_intro")}</p></div>
  <div class="release-next-grid">{"".join(tm_cards)}</div>
  <article class="release-watch-proof"><div><div class="release-next-kicker"><span>{q("tm_watch_label")}</span></div><h3>{q("tm_watch_title")}</h3><p>{q("tm_watch_copy")}</p><a href="help.html#time-machine-help">{q("tm_watch_link")} →</a></div><a href="../assets/release-2-0-en/watch-time-machine-start.png" target="_blank" rel="noopener" aria-label="{q("tm_watch_aria")}"><img src="../assets/release-2-0-en/watch-time-machine-start.png" alt="{q("tm_watch_alt")}" width="416" height="496" loading="lazy" decoding="async"></a></article>
</section>'''
    return hero, spotlight, time_machine


def update_index(local, english, lang, data):
    q = lambda key: translate(lang, data, key)
    local = replace_meta(local, "name", "description", data["meta_home"])
    local = replace_meta(local, "property", "og:description", data["meta_home_og"])
    local = replace_meta(local, "name", "twitter:description", data["meta_home_social"])
    css = english[english.index(".release-hero-teaser {"):english.index("@media (max-width: 760px) {\n  .version-grid")]
    local = replace_one(r'(?=@media \(max-width: 760px\) \{\s*\.version-grid)', css, local, "2.0 CSS insertion")
    hero, spotlight, time_machine = make_fragments(lang, data)
    local = replace_one(r'(?=<div class="hero-actions">)', hero + "\n", local, "hero teaser insertion")
    local = replace_one(r'(?=</div>\s*</div>\s*<div[^>]+class="hero-visual")', f'<span class="badge">{q("badge")}</span>\n', local, "Time Machine badge")
    versions = list(re.finditer(r'<span class="version-availability">[^<]+</span>', local))
    if len(versions) != 2:
        raise ValueError("expected two version labels")
    for match in reversed(versions):
        local = local[:match.start()] + f'<span class="version-availability">{q("version")} 2.0</span>' + local[match.end():]
    local = replace_one(r'(?=<section[^>]*\bid="companion-benefits"[^>]*>)', spotlight + "\n", local, "spotlight insertion")
    local = replace_one(r'(?=<section[^>]*\bid="rivalries"[^>]*>)', time_machine + "\n", local, "Time Machine insertion")
    share = element(local, "section", "share-results")
    gallery = one(r'<div class="share-gallery core-sharing-grid">(.*?)</div>\s*<div class="share-destination-callout"', share, "sharing gallery")
    old_cards = re.findall(r'<article class="share-card">.*?</article>', gallery.group(1), re.S)
    if len(old_cards) != 6:
        raise ValueError(f"expected six existing share cards, found {len(old_cards)}")
    cards = []
    for key, image in (("result", "share-set-tiebreak.png"), ("match", "share-match-tiebreak.png"), ("manual", "share-custom-manual.png")):
        cards.append(f'<article class="share-card"><a href="../assets/release-2-0-en/{image}" target="_blank" rel="noopener" aria-label="{q("share_"+key+"_aria")}"><img src="../assets/release-2-0-en/{image}" alt="{q("share_"+key+"_alt")}" width="1320" height="1650" loading="lazy" decoding="async"></a><h3>{q("share_"+key+"_title")}</h3><p>{q("share_"+key+"_copy")}</p></article>')
    gallery_html = '<div class="share-gallery core-sharing-grid">' + "\n".join(cards + old_cards[-2:]) + '</div>\n<div class="share-destination-callout"'
    share = share[:gallery.start()] + gallery_html + share[gallery.end():]
    share = replace_one(r'(<h2>[^<]*</h2>\s*<p class="section-subtitle">).*?(</p>)', rf'\g<1>{q("share_intro")}\g<2>', share, "sharing introduction")
    local = replace_one(re.escape(element(local, "section", "share-results")), share, local, "sharing section")
    local = sync_tags(local, english, "img", ("src", "srcset", "width", "height", "sizes"))
    local = sync_tags(local, english, "a", ())
    match = one(r'<img\b(?=[^>]*src="\.\./assets/release-2-0-en/iphone-match-details\.jpg")[^>]*>', local, "Match Details screenshot")
    local = local[:match.start()] + attr(match.group(), "alt", MATCH_DETAILS_ALTS[lang]) + local[match.end():]
    return local


def update_updates(local, english, lang, data):
    q = lambda key: translate(lang, data, key)
    local = replace_meta(local, "name", "description", data["meta_updates"])
    local = replace_meta(local, "property", "og:description", data["meta_updates_og"])
    local = replace_meta(local, "name", "twitter:description", data["meta_updates_social"])
    local = replace_one(r'(<h1 id="updates-title">).*?(</h1>)', rf'\g<1>{q("updates_h1")}\g<2>', local, "updates heading")
    cards = one(r'<div class="updates-product-grid">.*?</div>', local, "product cards")
    card_html = re.sub(r'<small>[^<]*</small>', f'<small>{q("version")} 2.0</small>', cards.group())
    local = local[:cards.start()] + card_html + local[cards.end():]
    previous_match = re.search(r'<article class="updates-latest-release release-previous"[^>]*>\s*<div class="updates-release-title"><span>([^<]+)</span>', local)
    if not previous_match:
        raise ValueError("missing previous release label")
    old_previous = previous_match.group(1)
    for kind, old_id in (("pro", "companion-1-8"), ("standalone", "standalone-1-11")):
        section_id = "companion-updates" if kind == "pro" else "standalone-updates"
        section = element(local, "section", section_id)
        section = replace_one(r'(<div class="updates-chapter-heading">.*?<h2>).*?(</h2>)', rf'\g<1>{q("updates_"+kind+"_title")}\g<2>', section, kind + " heading")
        section = replace_one(r'(<span class="updates-status">).*?(</span>)', rf'\g<1>{q("version")} 2.0\g<2>', section, kind + " status")
        section = replace_one(r'(<p class="updates-chapter-intro">).*?(</p>)', rf'\g<1>{q("updates_"+kind+"_intro")}\g<2>', section, kind + " intro")
        bullets = ''.join(f'<li><strong>{q("updates_"+kind+"_b"+str(i)+"_title")}</strong> {q("updates_"+kind+"_b"+str(i)+"_copy")}</li>' for i in range(1, 7 if kind == "pro" else 5))
        if kind == "pro":
            media = (("iphone-time-machine-tiebreak.jpg",900,1955,"updates_pro_media1"),("watch-time-machine-start.png",416,496,"updates_pro_media2"),("watch-five-set-finish.png",416,496,"updates_pro_media3"))
            gallery_class = "updates-recap-gallery-pro"
        else:
            media = (("standalone-watch-live-tiebreak.png",416,496,"updates_standalone_media1"),("standalone-watch-time-machine-start.png",416,496,"updates_standalone_media2"),("watch-five-set-finish.png",416,496,"updates_standalone_media3"))
            gallery_class = "updates-recap-gallery-watch"
        media_parts = []
        for file, width, height, key in media:
            image_class = 'class="updates-recap-watch-image" ' if width == 416 else ''
            media_parts.append(f'<a href="../assets/release-2-0-en/{file}" target="_blank" rel="noopener"><img {image_class}src="../assets/release-2-0-en/{file}" alt="{q(key+"_alt")}" width="{width}" height="{height}" loading="lazy" decoding="async"><span>{q(key+"_caption")}</span></a>')
        media_html = ''.join(media_parts)
        release_id = "companion" if kind == "pro" else "standalone"
        article = f'<article class="updates-latest-release" id="{release_id}-2-0"><div class="updates-release-title"><span>{q("latest_release")}</span><h3>{q("version")} 2.0</h3></div><ul>{bullets}</ul><div class="updates-recap-gallery {gallery_class}" aria-label="{q("updates_"+kind+"_gallery_alt")}">{media_html}</div>'
        if kind == "pro":
            article += f'<p><a href="index.html#time-machine">{q("updates_tm_link")} →</a></p>'
        article += '</article>\n'
        old = one(rf'<article class="updates-latest-release" id="{old_id}">', section, "old " + old_id)
        section = section[:old.start()] + article + section[old.start():]
        section = section.replace(f'<article class="updates-latest-release" id="{old_id}">', f'<article class="updates-latest-release release-previous" id="{old_id}">', 1)
        prior = one(rf'(<article class="updates-latest-release release-previous" id="{old_id}">\s*<div class="updates-release-title">\s*<span>).*?(</span>)', section, "prior label")
        section = section[:prior.start()] + prior.group(1) + escape(old_previous) + prior.group(2) + section[prior.end():]
        local = replace_one(re.escape(element(local, "section", section_id)), section, local, section_id)
    local = sync_tags(local, english, "img", ("src", "srcset", "width", "height", "sizes"))
    local = sync_tags(local, english, "a", ())
    return local


def update_help(local, lang, data):
    q = lambda key: translate(lang, data, key)
    questions = ''.join(f'<div class="help-item"><strong>{q("help_tm_q"+str(i))}</strong><p>{q("help_tm_a"+str(i))}</p></div>' for i in range(1,4))
    tm = f'<section id="time-machine-help"><h2>Time Machine</h2><p class="section-subtitle">{q("help_tm_intro")}</p><div class="help">{questions}</div></section>\n'
    local = replace_one(r'(?=<section id="history-files-help">)', tm, local, "Time Machine help insertion")
    for section_id, index, prefix in (("match-highlights",3,"streak"),("match-history",5,"tiebreak"),("match-history",6,"stopped"),("period-recaps",3,"recap")):
        section = element(local, "section", section_id)
        items = list(re.finditer(r'<div class="help-item">.*?</div>', section, re.S))
        if index >= len(items):
            raise ValueError(f"{section_id}: missing help item {index}")
        match = items[index]
        if prefix == "tiebreak":
            html = f'<div class="help-item"><strong>{q("help_tb_q")} <span class="score-nowrap">7–6</span>?</strong><p>{q("help_tb_a1")} <span class="score-nowrap">7–6</span><sup>6</sup> {q("help_tb_a2")} [<span class="score-nowrap">10–7</span>].</p></div>'
        else:
            html = f'<div class="help-item"><strong>{q("help_"+prefix+"_q")}</strong><p>{q("help_"+prefix+"_a")}</p></div>'
        section = section[:match.start()] + html + section[match.end():]
        local = replace_one(re.escape(element(local, "section", section_id)), section, local, section_id)
    return local


def main():
    args = argparse.ArgumentParser()
    args.add_argument("--write", action="store_true")
    args.add_argument("--from-head", action="store_true", help="regenerate only known clean locales from HEAD")
    args.add_argument("--locales", nargs="*", choices=LOCALES, default=LOCALES)
    options = args.parse_args()
    translations = json.loads(DATA.read_text(encoding="utf-8"))
    english = {page: (DOCS / f"{page}.html").read_text(encoding="utf-8") for page in ("index", "whats-new", "help")}
    pending = {}
    for lang in options.locales:
        data = fill_defaults(translations[lang])
        for page, update in (("index", update_index), ("whats-new", update_updates), ("help", update_help)):
            path = DOCS / lang / f"{page}.html"
            original = (subprocess.check_output(["git", "show", f"HEAD:docs/{lang}/{page}.html"], cwd=ROOT).decode("utf-8")
                        if options.from_head else path.read_text(encoding="utf-8"))
            local = update(original, english[page], lang, data) if page != "help" else update(original, lang, data)
            pending[path] = local
    if options.write:
        for path, content in pending.items():
            path.write_text(content, encoding="utf-8")
    print(f"Prepared {len(pending)} localized pages" + (" and wrote them" if options.write else " (dry run)"))


if __name__ == "__main__":
    main()
