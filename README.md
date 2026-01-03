# on page SEO analysis and recommendation agent

A FastAPI-based service that retrieves web pages, performs rule-based on-page SEO analysis, relies on GPT-4 mini model accessed via GitHub Models to generate content improvement recommendations, and returns results as both a structured JSON response and a styled HTML report. 
---

## Features
- Fetches a web page and extracts key SEO elements: title, meta description, headings, and word count
- Performs basic on-page SEO checks: title length, H1 usage, meta description presence/length, content length, and keyword in title
- Uses GPT-4 Mini (via GitHub Models) to suggest improved titles, meta descriptions, related keywords, and FAQs
- Generates a clean HTML SEO report; `/optimize/save` automatically saves it as `report.html` and opens it in your browser

---

## Project Layout
- `main.py` — FastAPI app & routes
- `src/core/config.py` — settings loader (.env)
- `src/utils/parser.py` — fetch & parse HTML
- `src/service/seo_rules.py` — SEO heuristics
- `src/service/ai_optimizer.py` — LLM call (GitHub Models via OpenAI client)
- `src/utils/report_generator.py` — HTML report builder
- `src/utils/optimizer.py` — orchestrates fetch → checks → AI → report
- `src/utils/schemas.py` — Pydantic models

---

## Environment

Create `.env` in the project root:

```
GITHUB_MODELS_TOKEN= your token here
REQUEST_TIMEOUT=10
USER_AGENT=SEO-Optimizer/1.0
```

---

## Execution

1. Clone the repository:

```
   git clone https://github.com/remembrance03/on-page-SEO-analysis-and-recommendation-agent.git
   cd on-page-SEO-analysis-and-recommendation-agent
   ```

2. Install dependencies
   
   ```
   pip install -r requirements.txt
   ```

3. Runnn.. 🏃‍♀️‍➡️

```bash
uvicorn main:app --reload
```
App runs at http://127.0.0.1:8000 (docs at /docs).

---

**Notes** 
- `report.html` is generated automatically and is listed in `.gitignore`.
- LLM calls require your GitHub Models token; no OpenAI key is needed.
- Make sure your `.env` is correctly set before running the app.

---

## Endpoints
- `POST /optimize` → JSON with parsed_data, issues, suggestions, report (HTML string)
- `POST /optimize/html` → Returns the HTML report directly
- `POST /optimize/save` → Returns JSON and also writes `report.html` (opened in your default browser)