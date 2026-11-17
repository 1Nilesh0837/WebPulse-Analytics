"""
WebPulse Analytics - Advanced SEO & Web Health Audit Suite
Author: Nilesh Sahoo (https://github.com/1Nilesh0837)
"""

__version__ = "1.0.0"
__author__ = "Nilesh Sahoo"

from .analyzer import SEOAnalyzer, SEOAuditResult
from .reporter import print_audit_report, generate_json_report, generate_html_report

__all__ = [
    "SEOAnalyzer",
    "SEOAuditResult",
    "print_audit_report",
    "generate_json_report",
    "generate_html_report",
]
