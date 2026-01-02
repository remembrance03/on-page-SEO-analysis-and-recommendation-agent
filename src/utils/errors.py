"""Custom exceptions for the SEO optimizer service."""

class FetchError(RuntimeError):
    """Raised when a page cannot be fetched."""


class ParseError(RuntimeError):
    """Raised when HTML parsing fails or returns unusable data."""


class AIResponseError(RuntimeError):
    """Raised when the AI service returns an invalid or unusable response."""
