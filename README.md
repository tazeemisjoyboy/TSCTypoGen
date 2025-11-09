# TSC TypoGen

TSC TypoGen is a free AI typography direction generator powered by Flask and Google Gemini. It
accepts your copy, mood, and constraints, then crafts a detailed art direction covering font pairings,
color palettes, hierarchy, layout, and accessibility. When Gemini is unavailable, the app falls back to a
curated set of best-practice recommendations so you always receive guidance.

## Features

- ✨ One-click generation of comprehensive typography briefs
- 🤖 Gemini 1.5 Flash integration with offline fallback
- 🧱 Structured markdown output for easy documentation or sharing
- 📋 Copy-to-clipboard helper
- 🎨 Sleek glassmorphism UI built with modern typography in mind

## Getting started

Everything lives in `app.py` at the repository root, with HTML under `templates/` and
styling in `static/css/`. The steps below boot the Flask server locally.

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Export your Gemini API key:

   ```bash
   export GEMINI_API_KEY="your-key"
   ```

   You can obtain a free key from the [Google AI Studio](https://aistudio.google.com/).

4. Start the development server using either the Flask CLI or the convenience `Makefile`:

   ```bash
   # Option A: Flask CLI
   flask --app app run --debug

   # Option B: Makefile helper
   make run
   ```

5. Visit [http://localhost:5000](http://localhost:5000) and start generating typography guidance.

If you just want to sanity-check the offline fallback without installing dependencies,
run `make demo`, which prints the static recommendation bundle in your terminal.

### Environment variables

- `GEMINI_API_KEY`: Required to use Google Gemini. If omitted, the app returns an offline
  best-practice template.
- `PORT`: Optional port override when running `python app.py`.

## Project structure

```
.
├── app.py                # Flask application and Gemini integration
├── typography.py         # Prompt builder and offline fallback helpers
├── templates/
│   └── index.html        # Front-end shell for interacting with the generator
├── static/
│   └── css/
│       └── styles.css    # Styling for the UI
├── scripts/
│   └── offline_demo.py   # Quick CLI to preview the offline output
├── Makefile              # Helper commands (install, run, test, demo)
└── requirements.txt      # Python dependencies
```

## Testing the API without the UI

You can send a POST request directly to the `/api/typography` endpoint:

```bash
curl -X POST http://localhost:5000/api/typography \
  -H 'Content-Type: application/json' \
  -d '{
        "text": "Design the hero copy for a fintech landing page",
        "mood": "trustworthy and innovative",
        "fontPreferences": "Use brand font GT America",
        "layoutNotes": "Desktop and mobile responsive marketing site"
      }'
```

When Gemini is configured, the response will contain the model's markdown guidance.
Otherwise, it returns the offline template.

## License

This project is released under the MIT License.
