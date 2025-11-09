"""Flask application for generating typography recommendations using Gemini."""
from __future__ import annotations

import os
from typing import Any, Dict

from flask import Flask, jsonify, render_template, request

from typography import (
    TypographyPrompt,
    configure_gemini as _configure_gemini,
    generate_typography as _generate_typography,
    offline_fallback as _offline_fallback,
)


def build_app() -> Flask:
    """Application factory so tests can create an app instance."""
    app = Flask(__name__)
    api_key = os.getenv("GEMINI_API_KEY")
    model = _configure_gemini(api_key)

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    @app.route("/api/typography", methods=["POST"])
    def typography() -> Any:
        data: Dict[str, str] = request.get_json(force=True)
        prompt = TypographyPrompt(
            text=data.get("text", ""),
            mood=data.get("mood", ""),
            font_preferences=data.get("fontPreferences", ""),
            layout_notes=data.get("layoutNotes", ""),
        )

        try:
            response = _generate_typography(prompt, model)
        except RuntimeError as exc:
            return jsonify({"error": str(exc)}), 503

        return jsonify({"recommendation": response})

    return app


app = build_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
