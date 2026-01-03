#this module is for the SEO optimization workflow handler

from src.utils.parser import fetch_and_parse    
from src.utils.schemas import OptimizeResponse
from src.service.seo_rules import run_seo_checks
from src.service.ai_optimizer import optimize_content
from src.utils.report_generator import generate_report  


def optimize_page(url: str, keyword: str | None) -> OptimizeResponse:
    """Orchestrate the end-to-end SEO optimization pipeline."""

    parsed = fetch_and_parse(url)    #fetch and parse the webpage content
    issues = run_seo_checks(parsed, keyword)      #evaluate SEO issues
    suggestions = optimize_content(parsed, issues, keyword)       #get AI-driven optimization suggestions

    response = OptimizeResponse(
        parsed_data=parsed,
        issues=issues,
        suggestions=suggestions,
    )
    
    response.report = generate_report(response)  #generate a formatted text report
    
    return response
