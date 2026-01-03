#this is for generating an HTML report from optimization results

from src.utils.schemas import OptimizeResponse


def generate_report(response: OptimizeResponse) -> str:
    """generate an HTML report from optimization results."""
    
    #counting H1 tags
    h1_count = sum(1 for h in response.parsed_data.headings if h.tag == 'h1')
    
    #generating HTML for issues section
    issues_html = ""
    if response.issues:
        issues_html = "<ul>"
        for issue in response.issues:
            issues_html += f"<li>{issue}</li>"
        issues_html += "</ul>"
    else:
        issues_html = '<p class="success">✓ No critical issues found!</p>'
    
    keywords_html = "<ul>"
    for keyword in response.suggestions.semantic_keywords:
        keywords_html += f"<li>{keyword}</li>"
    keywords_html += "</ul>"
    
    faqs_html = "<ol>"
    for faq in response.suggestions.faqs:
        faqs_html += f"<li>{faq}</li>"
    faqs_html += "</ol>"
    

    #constructing the full HTML report
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">

    <title>SEO Optimization Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 900px;
            margin: 40px auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .container {{
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #2c3e50;
            border-bottom: 3px solid #3498db;
            padding-bottom: 10px;
        }}
        h2 {{
            color: #34495e;
            margin-top: 30px;
            border-left: 4px solid #3498db;
            padding-left: 10px;
        }}
        .info-grid {{
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
            margin: 20px 0;
        }}
        .info-item {{
            background: #ecf0f1;
            padding: 15px;
            border-radius: 5px;
        }}
        .info-label {{
            font-weight: bold;
            color: #7f8c8d;
            font-size: 0.9em;
        }}
        .info-value {{
            font-size: 1.1em;
            color: #2c3e50;
            margin-top: 5px;
        }}
        .issues {{
            background: #ffe6e6;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #e74c3c;
        }}
        .issues ul {{
            margin: 10px 0;
        }}
        .success {{
            background: #d4edda;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #28a745;
            color: #155724;
        }}
        .suggestion-box {{
            background: #e8f4f8;
            padding: 15px;
            margin: 15px 0;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        .suggestion-label {{
            font-weight: bold;
            color: #2980b9;
            margin-bottom: 8px;
        }}
        ul, ol {{
            margin: 10px 0;
            padding-left: 25px;
        }}
        li {{
            margin: 8px 0;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>SEO Optimization Report</h1>
        
        <h2>Current Page Analysis</h2>
        <div class="info-grid">
            <div class="info-item">
                <div class="info-label">Title</div>
                <div class="info-value">{response.parsed_data.title or '(empty)'}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Word Count</div>
                <div class="info-value">{response.parsed_data.word_count}</div>
            </div>
            <div class="info-item">
                <div class="info-label">H1 Count</div>
                <div class="info-value">{h1_count}</div>
            </div>
            <div class="info-item">
                <div class="info-label">Total Headings</div>
                <div class="info-value">{len(response.parsed_data.headings)}</div>
            </div>
        </div>
        <div class="info-item">
            <div class="info-label">Meta Description</div>
            <div class="info-value">{response.parsed_data.meta_description or '(empty)'}</div>
        </div>
        
        <h2>Issues Identified</h2>
        <div class="{'issues' if response.issues else ''}">
            {issues_html}
        </div>
        
        <h2>Optimization Suggestions</h2>
        
        <div class="suggestion-box">
            <div class="suggestion-label">Improved Title</div>
            <div>{response.suggestions.improved_title}</div>
        </div>
        
        <div class="suggestion-box">
            <div class="suggestion-label">Improved Meta Description</div>
            <div>{response.suggestions.improved_meta_description}</div>
        </div>
        
        <div class="suggestion-box">
            <div class="suggestion-label">Semantic Keywords</div>
            {keywords_html}
        </div>
        
        <div class="suggestion-box">
            <div class="suggestion-label">Recommended FAQs</div>
            {faqs_html}
        </div>
    </div>
</body>
</html>"""
    
    return html
