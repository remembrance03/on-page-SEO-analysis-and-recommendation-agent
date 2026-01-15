#this module interacts with GitHub Models to optimize SEO content

from openai import OpenAI

from src.utils.schemas import ParsedData, Suggestions      #for data models
from src.core.config import get_settings                #for configuration
from src.utils.errors import AIResponseError            #for custom AI exception


#for optimizing content using GitHub Models with structured outputs
def optimize_content(parsed: ParsedData, issues: list[str], keyword: str | None) -> Suggestions:
    settings = get_settings()
    if not settings.github_models_token:
        raise AIResponseError("Missing GITHUB_MODELS_TOKEN configuration.")

    client = OpenAI(api_key=settings.github_models_token, base_url=settings.github_models_endpoint)

    prompt = f"""
You are an SEO assistant. Analyze the following webpage data and provide SEO optimization suggestions.
Do NOT rewrite the article - only suggest improvements.

Current Title: {parsed.title}
Meta Description: {parsed.meta_description}
Headings: {[h.model_dump() for h in parsed.headings]}  #list of heading dicts
Word Count: {parsed.word_count}
Issues: {issues}
Target keyword: {keyword}

Provide:
- An improved title (max 60 characters)
- An improved meta description (max 160 characters)
- Semantic keywords related to the content
- FAQ questions that could enhance the page
"""

    #for creating chat completion using structured outputs
    response = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format=Suggestions,
        temperature=0.7,
    )

    #return parsed Suggestions instance directly from the API
    return response.choices[0].message.parsed 
