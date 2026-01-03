from src.utils.schemas import ParsedData

#for evaluating SEO rules on parsed data
def run_seo_checks(parsed: ParsedData, keyword: str | None = None) -> list[str]:
    """Evaluate basic on-page SEO heuristics."""

    issues: list[str] = []  #to collect identified issues

    title_len = len(parsed.title.strip())    #checking title length
    if title_len < 30 or title_len > 60:
        issues.append("Title length should be between 30-60 characters")

    h1_count = len([h for h in parsed.headings if h.tag == "h1"])   #counting H1 tags
    if h1_count != 1:    
        issues.append("Page should contain exactly one H1")

    if not parsed.meta_description:      #checking meta description presence
        issues.append("Meta description is missing")
    elif len(parsed.meta_description) > 160:
        issues.append("Meta description should be 160 characters or fewer")

    if parsed.word_count < 500:
        issues.append("Content is thin (less than 500 words)")    #checking word count of content

    if keyword and keyword.lower() not in parsed.title.lower():   #checking keyword in title
        issues.append("Target keyword missing from title")   #checking keyword in title

    return issues   #returning list of identified SEO issues