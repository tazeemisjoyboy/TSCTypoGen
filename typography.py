"""Core typography prompt building and generation helpers."""
from __future__ import annotations

from dataclasses import dataclass
from textwrap import dedent
from typing import Any

try:  # pragma: no cover - optional dependency
    import google.generativeai as genai
except ModuleNotFoundError:  # pragma: no cover - dependency may be missing locally
    genai = None  # type: ignore

try:  # pragma: no cover - optional dependency
    from dotenv import load_dotenv
except ModuleNotFoundError:  # pragma: no cover - optional dependency
    load_dotenv = lambda: None  # type: ignore


load_dotenv()


@dataclass
class TypographyPrompt:
    """Collects parameters needed to describe desired typography."""

    text: str
    mood: str
    font_preferences: str
    layout_notes: str

    def build(self) -> str:
        """Return a detailed prompt for Gemini based on the provided metadata."""
        text = self.text.strip() or "N/A"
        mood = self.mood.strip() or "designer's choice"
        font_preferences = self.font_preferences.strip() or "none provided"
        layout_notes = self.layout_notes.strip() or "none provided"

        sections = [
            "You are an award winning typography and layout designer.",
            "Generate a comprehensive typography direction for the provided content.",
            "Return the result as structured markdown using the following sections:",
            "- Title treatment\n- Font pairing\n- Color palette\n- Hierarchy\n- Layout tips\n- Typesetting details\n- Accessibility considerations",
            "Make sure every section is present even if the user omits details.",
            "Use bullet lists where appropriate and keep recommendations concise but specific.",
            f"Content to typeset: {text}",
            f"Mood or tone: {mood}",
            f"Font preferences or brand guidelines: {font_preferences}",
            f"Layout or usage notes: {layout_notes}",
        ]
        return "\n\n".join(sections)


def configure_gemini(api_key: str | None) -> Any:
    """Configure the Gemini client if possible."""
    if not api_key:
        return None

    if genai is None:
        raise RuntimeError(
            "google-generativeai package is not installed. Install dependencies or "
            "set GEMINI_API_KEY only in environments where the SDK is available."
        )

    genai.configure(api_key=api_key)
    return genai.GenerativeModel("gemini-1.5-flash")


def generate_typography(prompt: TypographyPrompt, model: Any) -> str:
    """Generate typography guidance using Gemini or return an offline fallback."""
    if model is None:
        return offline_fallback(prompt)

    gemini_response = model.generate_content(prompt.build())
    try:
        return gemini_response.text.strip()
    except AttributeError as exc:  # pragma: no cover - defensive
        raise RuntimeError("Gemini did not return text content") from exc


def offline_fallback(prompt: TypographyPrompt) -> str:
    """Provide deterministic typography tips when Gemini is unavailable."""
    mood = prompt.mood or "designer's choice"
    font_preferences = (
        prompt.font_preferences
        or "Explore geometric sans for headings and a modern serif for body."
    )
    layout_notes = (
        prompt.layout_notes
        or "Target a generous 1.4 line height with 120% width for comfortable reading."
    )

    return dedent(
        f"""
    ### Title treatment
    - Craft a lead line that balances {mood} energy with clarity.
    - Consider setting the headline in small caps with tight tracking.

    ### Font pairing
    - Primary: {font_preferences}
    - Secondary: Pair with a workhorse sans-serif like Inter for UI labels.

    ### Color palette
    - Anchor with a deep charcoal (#1F1F1F) and accent using a vivid highlight (#FF5C8D).
    - Use off-white (#F5F1EB) backgrounds to keep contrast comfortable.

    ### Hierarchy
    - Use 1.25× modular scale for headings. Keep body copy at 16–18px.
    - Maintain consistent spacing increments (4px baseline grid).

    ### Layout tips
    - {layout_notes}
    - Align text blocks to a 12-column grid with generous outer margins.

    ### Typesetting details
    - Headline tracking: -15. Body tracking: +5. Ensure optimal kerning for numerals.
    - Rag control: aim for 5–7 words per line to preserve rhythm.

    ### Accessibility considerations
    - Minimum contrast ratio 4.5:1 for text, 3:1 for large display type.
    - Include accessible font size toggles and underline interactive elements.
    """
    ).strip()


__all__ = [
    "TypographyPrompt",
    "configure_gemini",
    "generate_typography",
    "offline_fallback",
]
