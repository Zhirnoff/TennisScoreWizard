#!/usr/bin/env python3
"""Write manually translated captions for the two release videos."""

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDIA = ROOT / "docs/assets/release-2-0-en"
DATA = json.loads(Path(__file__).with_name("site_2_0_captions.json").read_text())
TIMES = {
    "watch": [(0, 6), (6, 12), (12, 14), (14, 18), (18, 21)],
    "phone": [(0, 5), (5, 11), (11, 19), (19, 22), (22, 30)],
}
STEMS = {"watch": "watch-score-flip", "phone": "iphone-time-machine"}


def stamp(seconds):
    return f"00:00:{seconds:02d}.000"


for lang, videos in DATA.items():
    for kind, stem in STEMS.items():
        captions = videos[kind]
        assert len(captions) == len(TIMES[kind]), (lang, kind)
        cues = [f"{stamp(start)} --> {stamp(end)}\n{caption}"
                for (start, end), caption in zip(TIMES[kind], captions)]
        (MEDIA / f"{stem}.{lang}.vtt").write_text("WEBVTT\n\n" + "\n\n".join(cues) + "\n")

print(f"Wrote {len(DATA) * len(STEMS)} localized caption files")
