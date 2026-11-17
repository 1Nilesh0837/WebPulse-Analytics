"""
Core SEO Analysis Engine for WebPulse Analytics.
Evaluates on-page SEO factors, technical compliance, and web health.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse, urljoin
import time
import requests
from bs4 import BeautifulSoup


@dataclass
class SEOAuditResult:
    """Holds the complete result of an SEO audit."""
    url: str
    status_code: int = 200
    response_time_ms: float = 0.0
    ssl_active: bool = False
    
    # Title Tag
    title: Optional[str] = None
    title_length: int = 0
    title_status: str = "Missing"
    title_recommendation: str = ""
    
    # Meta Description
    meta_description: Optional[str] = None
    meta_description_length: int = 0
    meta_description_status: str = "Missing"
    meta_description_recommendation: str = ""
    
    # Headings
    headings: Dict[str, List[str]] = field(default_factory=dict)
    h1_count: int = 0
    h1_status: str = ""
    
    # Images
    total_images: int = 0
    missing_alt_images: List[str] = field(default_factory=list)
    images_with_alt_count: int = 0
    
    # Links
    total_links: int = 0
    internal_links: int = 0
    external_links: int = 0
    nofollow_links: int = 0
    
    # Social Tags
    open_graph: Dict[str, str] = field(default_factory=dict)
    twitter_card: Dict[str, str] = field(default_factory=dict)
    
    # Technical Signals
    canonical_url: Optional[str] = None
    robots_meta: Optional[str] = None
    viewport_meta: Optional[str] = None
    favicon_found: bool = False
    
    # Scoring
    score: int = 0
    grade: str = "N/A"
    recommendations: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert the audit result to a JSON-serializable dictionary."""
        return {
            "url": self.url,
            "status_code": self.status_code,
            "response_time_ms": round(self.response_time_ms, 2),
            "ssl_active": self.ssl_active,
            "score": self.score,
            "grade": self.grade,
            "title": {
                "text": self.title,
                "length": self.title_length,
                "status": self.title_status,
                "recommendation": self.title_recommendation,
            },
            "meta_description": {
                "text": self.meta_description,
                "length": self.meta_description_length,
                "status": self.meta_description_status,
                "recommendation": self.meta_description_recommendation,
            },
            "headings": {
                "structure": self.headings,
                "h1_count": self.h1_count,
                "status": self.h1_status,
            },
            "images": {
                "total": self.total_images,
                "with_alt": self.images_with_alt_count,
                "missing_alt_count": len(self.missing_alt_images),
                "missing_alt_samples": self.missing_alt_images[:10],
            },
            "links": {
                "total": self.total_links,
                "internal": self.internal_links,
                "external": self.external_links,
                "nofollow": self.nofollow_links,
            },
            "social": {
                "open_graph": self.open_graph,
                "twitter_card": self.twitter_card,
            },
            "technical": {
                "canonical_url": self.canonical_url,
                "robots_meta": self.robots_meta,
                "viewport_meta": self.viewport_meta,
                "favicon_found": self.favicon_found,
            },
            "recommendations": self.recommendations,
        }


class SEOAnalyzer:
    """Analyzes a website or HTML string for SEO health and best practices."""

    def __init__(self, user_agent: Optional[str] = None):
        self.user_agent = user_agent or (
            "WebPulseAnalytics/1.0 (+https://github.com/1Nilesh0837/WebPulse-Analytics)"
        )

    def audit_url(self, url: str, timeout: int = 15) -> SEOAuditResult:
        """Fetch and audit a live webpage by URL."""
        if not url.startswith(("http://", "https://")):
            url = f"https://{url}"

        parsed = urlparse(url)
        ssl_active = parsed.scheme.lower() == "https"

        headers = {
            "User-Agent": self.user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }

        start_time = time.perf_counter()
        response = requests.get(url, headers=headers, timeout=timeout, allow_redirects=True)
        response_time_ms = (time.perf_counter() - start_time) * 1000

        soup = BeautifulSoup(response.content, "html.parser")
        return self._evaluate_soup(
            soup=soup,
            url=response.url or url,
            status_code=response.status_code,
            response_time_ms=response_time_ms,
            ssl_active=ssl_active,
        )

    def audit_html(
        self,
        html_content: str,
        base_url: str = "https://example.com",
        response_time_ms: float = 45.0,
        status_code: int = 200,
    ) -> SEOAuditResult:
        """Audit raw HTML content without sending network requests (ideal for local testing/CI)."""
        ssl_active = base_url.startswith("https://")
        soup = BeautifulSoup(html_content, "html.parser")
        return self._evaluate_soup(
            soup=soup,
            url=base_url,
            status_code=status_code,
            response_time_ms=response_time_ms,
            ssl_active=ssl_active,
        )

    def _evaluate_soup(
        self,
        soup: BeautifulSoup,
        url: str,
        status_code: int,
        response_time_ms: float,
        ssl_active: bool,
    ) -> SEOAuditResult:
        """Internal evaluator that coordinates all SEO audits."""
        result = SEOAuditResult(
            url=url,
            status_code=status_code,
            response_time_ms=response_time_ms,
            ssl_active=ssl_active,
        )

        self._analyze_title(soup, result)
        self._analyze_meta_description(soup, result)
        self._analyze_headings(soup, result)
        self._analyze_images(soup, result)
        self._analyze_links(soup, result, url)
        self._analyze_social_meta(soup, result)
        self._analyze_technical(soup, result)
        self._calculate_score(result)

        return result

    def _analyze_title(self, soup: BeautifulSoup, result: SEOAuditResult) -> None:
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            title_text = title_tag.string.strip()
            length = len(title_text)
            result.title = title_text
            result.title_length = length

            if 50 <= length <= 60:
                result.title_status = "Optimal"
                result.title_recommendation = "Title length is well-optimized for search engines (50-60 chars)."
            elif length < 50:
                result.title_status = "Too Short"
                result.title_recommendation = f"Title is {length} characters. Consider expanding to 50-60 characters for better search relevance."
            else:
                result.title_status = "Too Long"
                result.title_recommendation = f"Title is {length} characters. Search engines might truncate titles longer than 60 characters."
        else:
            result.title = None
            result.title_length = 0
            result.title_status = "Missing"
            result.title_recommendation = "Add a descriptive <title> tag (50-60 characters)."
            result.recommendations.append("Critical: Missing <title> tag.")

    def _analyze_meta_description(self, soup: BeautifulSoup, result: SEOAuditResult) -> None:
        meta_desc = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "description"})
        if meta_desc and meta_desc.get("content"):
            content = meta_desc["content"].strip()
            length = len(content)
            result.meta_description = content
            result.meta_description_length = length

            if 140 <= length <= 160:
                result.meta_description_status = "Optimal"
                result.meta_description_recommendation = "Meta description length is optimal (140-160 characters)."
            elif length < 140:
                result.meta_description_status = "Too Short"
                result.meta_description_recommendation = f"Meta description is {length} characters. Expand to ~150-160 characters to maximize SERP CTR."
            else:
                result.meta_description_status = "Too Long"
                result.meta_description_recommendation = f"Meta description is {length} characters. Truncation may occur in search results (aim for < 160 chars)."
        else:
            result.meta_description = None
            result.meta_description_length = 0
            result.meta_description_status = "Missing"
            result.meta_description_recommendation = "Add a compelling meta description (140-160 characters) summarizing page content."
            result.recommendations.append("High Priority: Missing meta description.")

    def _analyze_headings(self, soup: BeautifulSoup, result: SEOAuditResult) -> None:
        headers: Dict[str, List[str]] = {}
        for level in range(1, 7):
            tag_name = f"h{level}"
            elements = soup.find_all(tag_name)
            headers[f"H{level}"] = [h.get_text(strip=True) for h in elements if h.get_text(strip=True)]

        result.headings = headers
        result.h1_count = len(headers.get("H1", []))

        if result.h1_count == 1:
            result.h1_status = "Optimal (Single H1 found)"
        elif result.h1_count == 0:
            result.h1_status = "Missing H1"
            result.recommendations.append("High Priority: Add a primary H1 heading to denote the main topic.")
        else:
            result.h1_status = f"Multiple H1 tags ({result.h1_count} found)"
            result.recommendations.append(f"Moderate: Found {result.h1_count} H1 tags. Best practice is one distinct H1 per page.")

    def _analyze_images(self, soup: BeautifulSoup, result: SEOAuditResult) -> None:
        images = soup.find_all("img")
        result.total_images = len(images)
        missing_alt: List[str] = []
        with_alt = 0

        for img in images:
            alt = img.get("alt")
            src = img.get("src") or img.get("data-src") or "unknown_image"
            if alt is not None and alt.strip():
                with_alt += 1
            else:
                missing_alt.append(src)

        result.missing_alt_images = missing_alt
        result.images_with_alt_count = with_alt

        if missing_alt:
            result.recommendations.append(
                f"Moderate: {len(missing_alt)} image(s) are missing descriptive alt attributes."
            )

    def _analyze_links(self, soup: BeautifulSoup, result: SEOAuditResult, base_url: str) -> None:
        parsed_base = urlparse(base_url)
        domain = parsed_base.netloc.lower()

        links = soup.find_all("a", href=True)
        result.total_links = len(links)

        internal = 0
        external = 0
        nofollow = 0

        for a in links:
            href = a["href"].strip()
            rel = [r.lower() for r in a.get("rel", [])] if isinstance(a.get("rel"), list) else [str(a.get("rel", "")).lower()]
            if "nofollow" in rel:
                nofollow += 1

            if not href or href.startswith(("#", "javascript:", "mailto:", "tel:")):
                continue

            parsed_href = urlparse(href)
            if not parsed_href.netloc or parsed_href.netloc.lower() == domain:
                internal += 1
            else:
                external += 1

        result.internal_links = internal
        result.external_links = external
        result.nofollow_links = nofollow

    def _analyze_social_meta(self, soup: BeautifulSoup, result: SEOAuditResult) -> None:
        # Open Graph
        og_tags = {}
        for prop in ["title", "description", "image", "url", "type", "site_name"]:
            tag = soup.find("meta", attrs={"property": f"og:{prop}"})
            if tag and tag.get("content"):
                og_tags[f"og:{prop}"] = tag["content"].strip()
        result.open_graph = og_tags

        # Twitter Card
        tc_tags = {}
        for name in ["card", "title", "description", "image", "site"]:
            tag = soup.find("meta", attrs={"name": f"twitter:{name}"})
            if tag and tag.get("content"):
                tc_tags[f"twitter:{name}"] = tag["content"].strip()
        result.twitter_card = tc_tags

    def _analyze_technical(self, soup: BeautifulSoup, result: SEOAuditResult) -> None:
        # Canonical URL
        canonical = soup.find("link", attrs={"rel": lambda x: x and "canonical" in x})
        if canonical and canonical.get("href"):
            result.canonical_url = canonical["href"].strip()
        else:
            result.recommendations.append("Low Priority: Add a rel='canonical' link to prevent duplicate content.")

        # Robots meta
        robots = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "robots"})
        if robots and robots.get("content"):
            result.robots_meta = robots["content"].strip()

        # Viewport meta
        viewport = soup.find("meta", attrs={"name": lambda x: x and x.lower() == "viewport"})
        if viewport and viewport.get("content"):
            result.viewport_meta = viewport["content"].strip()
        else:
            result.recommendations.append("High Priority: Missing viewport meta tag. Vital for mobile responsiveness.")

        # Favicon
        icon = soup.find("link", attrs={"rel": lambda x: x and any(i in x for i in ["icon", "shortcut icon"])})
        result.favicon_found = bool(icon and icon.get("href"))

    def _calculate_score(self, result: SEOAuditResult) -> None:
        """Calculate a composite SEO score from 0 to 100."""
        score = 100

        # Title Tag (up to -20)
        if result.title_status == "Missing":
            score -= 20
        elif result.title_status in ["Too Short", "Too Long"]:
            score -= 5

        # Meta Description (up to -15)
        if result.meta_description_status == "Missing":
            score -= 15
        elif result.meta_description_status in ["Too Short", "Too Long"]:
            score -= 5

        # Headings (up to -15)
        if result.h1_count == 0:
            score -= 15
        elif result.h1_count > 1:
            score -= 5

        # Image Alt Attributes (up to -15)
        if result.total_images > 0:
            missing_ratio = len(result.missing_alt_images) / result.total_images
            score -= int(missing_ratio * 15)

        # Viewport (up to -15)
        if not result.viewport_meta:
            score -= 15

        # SSL (up to -10)
        if not result.ssl_active:
            score -= 10
            result.recommendations.append("High Priority: Serve your site over secure HTTPS/SSL.")

        # Canonical tag (up to -5)
        if not result.canonical_url:
            score -= 5

        # Social sharing tags (up to -5)
        if not result.open_graph:
            score -= 5

        score = max(0, min(100, score))
        result.score = score

        if score >= 90:
            result.grade = "A+"
        elif score >= 80:
            result.grade = "A"
        elif score >= 70:
            result.grade = "B"
        elif score >= 60:
            result.grade = "C"
        elif score >= 50:
            result.grade = "D"
        else:
            result.grade = "F"
