"""
WebPulse Analytics - Main Application Entrypoint
Empowering web developers, marketers, and site owners with actionable SEO intelligence.

Author: Nilesh Sahoo (https://github.com/1Nilesh0837)
Repository: https://github.com/1Nilesh0837/WebPulse-Analytics
"""

import sys
from webpulse.analyzer import SEOAnalyzer, SEOAuditResult
from webpulse.reporter import print_audit_report, generate_json_report, generate_html_report
from webpulse.cli import main


# Backward-compatible convenience functions
def analyze_title_tag(soup):
    analyzer = SEOAnalyzer()
    res = SEOAuditResult(url="")
    analyzer._analyze_title(soup, res)
    return f"Title Tag: {res.title}" if res.title else "No Title Tag Found."


def analyze_meta_description(soup):
    analyzer = SEOAnalyzer()
    res = SEOAuditResult(url="")
    analyzer._analyze_meta_description(soup, res)
    return f"Meta Description: {res.meta_description}" if res.meta_description else "No Meta Description Found."


def analyze_header_tags(soup):
    analyzer = SEOAnalyzer()
    res = SEOAuditResult(url="")
    analyzer._analyze_headings(soup, res)
    return res.headings


def analyze_image_alt_tags(soup):
    analyzer = SEOAnalyzer()
    res = SEOAuditResult(url="")
    analyzer._analyze_images(soup, res)
    if res.missing_alt_images:
        return f"Images missing Alt Tags: {res.missing_alt_images}"
    return "All images have Alt Tags."


def seo_analyzer(url: str, output_html: str = None, output_json: str = None):
    """Main audit runner for programmatic and script use."""
    analyzer = SEOAnalyzer()
    try:
        result = analyzer.audit_url(url)
        print_audit_report(result)
        if output_html:
            generate_html_report(result, output_html)
        if output_json:
            generate_json_report(result, output_json)
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == "__main__":
    main()
