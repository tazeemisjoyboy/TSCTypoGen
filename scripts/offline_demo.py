"""Print a sample offline typography recommendation."""
from __future__ import annotations

import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from typography import TypographyPrompt, offline_fallback


if __name__ == "__main__":
    prompt = TypographyPrompt(
        text="Sample hero line for a creative agency",
        mood="futuristic but friendly",
        font_preferences="Pair a geometric sans with a warm serif",
        layout_notes="Homepage hero section",
    )
    print(offline_fallback(prompt))
