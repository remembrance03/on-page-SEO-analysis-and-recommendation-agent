#this module interacts with GitHub Models to optimize SEO content

import json
from json import JSONDecodeError    #for handling JSON parsing errors
from typing import Any

from openai import OpenAI

from src.utils.schemas import ParsedData, Suggestions      #for data models
from src.core.config import get_settings                #for configuration


#for extracting JSON from model response
def _extract_json_text(raw: str) -> dict[str, Any]:
    """Attempt to coerce the model response into JSON."""

    cleaned = raw.strip()   #for removing leading/trailing whitespace
    if cleaned.startswith("```"):
        cleaned = cleaned.strip("`").strip()
        if cleaned.lower().startswith("json"):     #for ```json blocks
            cleaned = cleaned[4:].strip()

    try:
        return json.loads(cleaned)
    except JSONDecodeError as exc:        #if JSON parsing fails
        raise ValueError("Model response was not valid JSON") from exc



#for optimizing content using GitHub Models
def optimize_content(parsed: ParsedData, issues: list[str], keyword: str | None) -> Suggestions:
    settings = get_settings()
    if not settings.github_models_token:
        raise RuntimeError("Missing GITHUB_MODELS_TOKEN configuration.")

    client = OpenAI(api_key=settings.github_models_token, base_url=settings.github_models_endpoint)

    prompt = f"""
You are an SEO assistant. Do NOT rewrite the article. Respond with ONLY valid JSON using this schema:
{{
  "improved_title": "string (<=60 chars)",
  "improved_meta_description": "string (<=160 chars)",
  "semantic_keywords": ["string", "string", "string"],
  "faqs": ["string", "string", "string"]
}}

Current Title: {parsed.title}
Meta Description: {parsed.meta_description}
Headings: {[h.model_dump() for h in parsed.headings]}
Word Count: {parsed.word_count}
Issues: {issues}
Target keyword: {keyword}
"""

    #for creating chat completion using GitHub Models
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    #for extracting JSON payload from model response
    #payload is a dict matching the Suggestions schema
    payload = _extract_json_text(response.choices[0].message.content)   #extract JSON from response and parse it

    #return Suggestions instance created from payload
    return Suggestions(**payload) 
