import pathlib
import sys

import pytest

pytest.importorskip("flask")

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import build_app
from typography import TypographyPrompt, offline_fallback


def test_offline_fallback_has_sections():
    prompt = TypographyPrompt(
        text="Sample headline",
        mood="playful",
        font_preferences="Use Avenir",
        layout_notes="Billboard layout"
    )
    output = offline_fallback(prompt)

    expected_sections = [
        "### Title treatment",
        "### Font pairing",
        "### Color palette",
        "### Hierarchy",
        "### Layout tips",
        "### Typesetting details",
        "### Accessibility considerations",
    ]

    for section in expected_sections:
        assert section in output


def test_build_app_creates_flask_app():
    app = build_app()
    assert app.name == "app"
    assert app.url_map is not None
