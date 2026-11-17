"""
Unit tests for WebPulse Analytics SEO audit engine.
"""

import unittest
from webpulse.analyzer import SEOAnalyzer


class TestSEOAnalyzer(unittest.TestCase):

    def setUp(self):
        self.analyzer = SEOAnalyzer()

    def test_optimal_page(self):
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>WebPulse Analytics - Fast and Smart Web Audit Engine</title>
            <meta name="description" content="WebPulse Analytics provides in-depth SEO metrics, meta tag validation, and content structure audits for optimal website performance." />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <link rel="canonical" href="https://example.com/" />
            <link rel="icon" href="/favicon.ico" />
            <meta property="og:title" content="WebPulse Analytics" />
        </head>
        <body>
            <h1>Comprehensive SEO Audit for Modern Web Applications</h1>
            <p>Welcome to WebPulse Analytics.</p>
            <h2>Heading Two</h2>
            <img src="/img/logo.png" alt="WebPulse Logo" />
            <a href="/about">About Us</a>
            <a href="https://google.com" rel="nofollow">External Link</a>
        </body>
        </html>
        """
        result = self.analyzer.audit_html(sample_html, base_url="https://example.com")

        self.assertEqual(result.title_status, "Optimal")
        self.assertEqual(result.meta_description_status, "Optimal")
        self.assertEqual(result.h1_count, 1)
        self.assertEqual(result.total_images, 1)
        self.assertEqual(len(result.missing_alt_images), 0)
        self.assertEqual(result.canonical_url, "https://example.com/")
        self.assertTrue(result.ssl_active)
        self.assertGreaterEqual(result.score, 90)
        self.assertIn(result.grade, ["A", "A+"])

    def test_missing_tags(self):
        poor_html = """
        <!DOCTYPE html>
        <html>
        <head></head>
        <body>
            <div>No headings, no title, no meta tags</div>
            <img src="/img/broken.jpg" />
        </body>
        </html>
        """
        result = self.analyzer.audit_html(poor_html, base_url="http://insecure-example.com")

        self.assertIsNone(result.title)
        self.assertEqual(result.title_status, "Missing")
        self.assertIsNone(result.meta_description)
        self.assertEqual(result.h1_count, 0)
        self.assertEqual(len(result.missing_alt_images), 1)
        self.assertFalse(result.ssl_active)
        self.assertLess(result.score, 60)
        self.assertIn("Critical: Missing <title> tag.", result.recommendations)


if __name__ == "__main__":
    unittest.main()
