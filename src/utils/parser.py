#this code is for fetching and parsing web pages for SEO data

from typing import Any    #for type ignoring

import requests
from bs4 import BeautifulSoup  #for HTML parsing
 
from src.utils.schemas import Heading, ParsedData  #for data models
from src.core.config import get_settings

#for safely extracting text from HTML tags
def _safe_get_text(tag: Any) -> str:
    return tag.get_text(strip=True) if tag else ""

#for fetching and parsing a web page
def fetch_and_parse(url: str) -> ParsedData:
    """Fetch a page and return structured SEO-relevant data."""

    settings = get_settings()

    try:   #fetching the web page
        response = requests.get(
            url,
            timeout=settings.request_timeout,   #timeout helps with slow responses and hanging
            headers={"User-Agent": settings.user_agent},   #setting a custom user agent for requests
        )
        response.raise_for_status()
    except requests.RequestException as exc:
        raise ValueError(f"Failed to fetch URL: {exc}") from exc

    soup = BeautifulSoup(response.text, "html.parser")

    title = _safe_get_text(soup.title)    #extracting the title tag text
    meta = soup.find("meta", attrs={"name": "description"})     #finding the meta description tag
    meta_desc = meta.get("content", "") if meta else ""         #getting the content attribute of meta description

    #extracting headings (H1, H2, H3)
    headings: list[Heading] = []
    for tag in ["h1", "h2", "h3"]:
        for h in soup.find_all(tag):
            headings.append(Heading(tag=tag, text=_safe_get_text(h)))

    text = soup.get_text(separator=" ", strip=True)    #getting all text content from the page and normalizing whitespace
    word_count = len(text.split())    #counting words in the text content


    #returning structured parsed data
    return ParsedData(
        title=title,
        meta_description=meta_desc,
        headings=headings,
        word_count=word_count,
    )
