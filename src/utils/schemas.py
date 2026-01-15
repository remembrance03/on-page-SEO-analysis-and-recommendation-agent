#this code is for defining data models used in the SEO optimizer service

from typing import Literal

from pydantic import AnyHttpUrl, BaseModel, Field   #AntHttpUrl for URL validation
                                                    #Field for metadata
                                                    #BaseModel as the base class for data models

#data model for HTML headings
class Heading(BaseModel):
    tag: Literal["h1", "h2", "h3"]   #restricting to specific heading tags for SEO
    text: str

#data model for parsed SEO-relevant data from a webpage
class ParsedData(BaseModel):
    title: str = Field(default="", description="Page title text")   
    meta_description: str = Field(default="", description="Meta description content")
    headings: list[Heading] = Field(default_factory=list)
    word_count: int = Field(default=0, ge=0)

#data model for AI-generated SEO suggestions
class Suggestions(BaseModel):
    improved_title: str = Field(..., max_length=60, description="Optimized page title (max 60 characters)")
    improved_meta_description: str = Field(..., max_length=160, description="Optimized meta description (max 160 characters)")
    semantic_keywords: list[str] = Field(default_factory=list, description="Relevant semantic keywords")
    faqs: list[str] = Field(default_factory=list, description="Suggested FAQ questions")

#data model for optimization request for a given URL to include optional target keyword
class OptimizeRequest(BaseModel):
    url: AnyHttpUrl
    keyword: str | None = None   #optional target keyword for SEO optimization (none=none for no keyword)

#data model for optimization response for a given URL to include report
class OptimizeResponse(BaseModel):
    parsed_data: ParsedData
    issues: list[str]
    suggestions: Suggestions
    report: str = Field(default="", description="Formatted text report")