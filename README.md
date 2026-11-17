# ⚡ WebPulse Analytics

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/1Nilesh0837/WebPulse-Analytics)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/1Nilesh0837/WebPulse-Analytics/pulls)

> **WebPulse Analytics** is a high-performance, modular Python engine designed to audit, analyze, and score on-page SEO elements, website health, and technical compliance in real-time.

---

## 🚀 Overview

Whether you are optimizing a personal blog, auditing client web apps, or integrating automated SEO checks into your CI/CD pipeline, **WebPulse Analytics** delivers instant, actionable feedback on key ranking factors:

- **Metadata Verification**: In-depth analysis of `<title>` tags, meta descriptions, viewport configurations, and canonical links.
- **Content Hierarchy**: Full examination of heading tags (`<h1>` through `<h6>`) with structure validation.
- **Media Optimization**: Pinpoints images missing critical `alt` attributes with asset URL diagnostics.
- **Link Auditing**: Aggregates internal, external, and `nofollow` link distributions.
- **Social Graph Readiness**: Audits Open Graph (`og:*`) and Twitter Card (`twitter:*`) tags for rich social previews.
- **Scoring & Recommendations**: Generates a weighted 0–100 health score, letter grade (A+ to F), and prioritized action steps.
- **Multi-Format Reports**: Beautiful terminal dashboard, JSON data export, and responsive standalone HTML reports.

---

## 📋 Features

| Feature | Description |
| :--- | :--- |
| **Title Tag Optimization** | Validates presence and optimal character length (50–60 characters). |
| **Meta Description Audit** | Ensures presence and SERP-friendly snippet length (140–160 characters). |
| **Heading Structure** | Validates semantic H1 presence and maps heading tags H1 through H6. |
| **Image Alt Audit** | Scans all `<img>` tags and flags missing alt texts with source URLs. |
| **Link Profiling** | Detects total, internal, external, and nofollow link distribution. |
| **Social Metadata** | Checks Open Graph (`og:title`, `og:image`, `og:description`) and Twitter Cards. |
| **Technical Health** | Inspects SSL / HTTPS enforcement, canonical URLs, robots meta tags, and favicons. |
| **Performance Metrics** | Measures server response time (TTFB / download latency) in milliseconds. |
| **HTML / JSON Export** | Generates standalone HTML dashboards and structured JSON reports. |

---

## 🛠️ Project Structure

```
WebPulse-Analytics/
├── webpulse/
│   ├── __init__.py         # Package exports
│   ├── analyzer.py         # Core SEO auditing engine & scoring logic
│   ├── reporter.py         # Terminal output, JSON & HTML report builders
│   └── cli.py              # CLI argument parsing and execution
├── tests/
│   ├── __init__.py
│   └── test_analyzer.py    # Unit tests for audit rules and mock HTML
├── app.py                  # Main entry point (interactive & scriptable)
├── requirements.txt        # Production dependencies
├── .gitignore              # Clean environment ignore rules
├── LICENSE                 # MIT License
└── README.md               # Documentation
```

---

## 📦 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/1Nilesh0837/WebPulse-Analytics.git
   cd WebPulse-Analytics
   ```

2. **Create and activate a virtual environment:**
   ```bash
   # On macOS/Linux:
   python3 -m venv venv
   source venv/bin/activate

   # On Windows:
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 💻 Usage

### 1. Interactive Mode
Run the analyzer without arguments to be prompted for a website URL:
```bash
python app.py
```
```text
Enter the URL of the website: https://example.com
```

### 2. Direct CLI Audit
Pass the URL directly on the command line:
```bash
python app.py https://example.com
```

### 3. Generate HTML & JSON Reports
Generate modern, standalone reports for client presentations or archiving:
```bash
# Generate a styled HTML report:
python app.py https://example.com --html audit_report.html

# Generate a JSON dataset:
python app.py https://example.com --json audit_report.json

# Generate both quietly without terminal verbose output:
python app.py https://example.com --html report.html --json report.json --quiet
```

### 4. Programmatic Python API
Integrate WebPulse Analytics directly into your Python scripts or web crawlers:
```python
from webpulse import SEOAnalyzer

analyzer = SEOAnalyzer()
result = analyzer.audit_url("https://example.com")

print(f"Health Score: {result.score}/100 ({result.grade})")
print(f"Title: {result.title}")
print(f"Missing Alt Images: {len(result.missing_alt_images)}")
for rec in result.recommendations:
    print(f"- {rec}")
```

---

## 🧪 Running Tests

WebPulse Analytics includes unit tests that validate analysis rules using mock HTML templates:

```bash
python -m unittest discover tests
```

---

## 📊 Example Terminal Output

```text
=================================================================
   ⚡ WEBPULSE ANALYTICS - SEO AUDIT REPORT ⚡
=================================================================
 Target URL:     https://example.com
 HTTP Status:    200
 Response Time:  142.30 ms
 SSL / HTTPS:    Secure (HTTPS)
 SEO Health:     95/100 (Grade A+)
-----------------------------------------------------------------

[1] Title Tag:
   Value:  "Example Domain"
   Length: 14 characters (Too Short)
   Tip:    Consider expanding to 50-60 characters for better search relevance.

[2] Meta Description:
   Value:  "This domain is for use in illustrative examples..."
   Length: 152 characters (Optimal)
   Tip:    Meta description length is optimal (140-160 characters).

[3] Heading Hierarchy:
   H1 Count: 1 (Optimal - Single H1 found)
   H1: 1 -> "Example Domain"

[4] Image Optimization:
   Total Images:         3
   With Alt Attribute:   3
   ✔ All images have descriptive alt attributes!

[5] Link Profile:
   Total Links:    1
   Internal Links: 0
   External Links: 1
   Nofollow Links: 0

[6] Technical & Social Metadata:
   Canonical Tag:  https://example.com/
   Robots Meta:    Default (index, follow)
   Mobile Viewport: Configured
   Favicon:        Present
   Open Graph:     4 tags
   Twitter Card:   2 tags

[7] Actionable Recommendations:
   1. Title is 14 characters. Consider expanding to 50-60 characters for better search relevance.

=================================================================
```

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
Feel free to check the [issues page](https://github.com/1Nilesh0837/WebPulse-Analytics/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License. See [`LICENSE`](LICENSE) for more details.

---

## 👤 Author

**Nilesh Sahoo**
- GitHub: [@1Nilesh0837](https://github.com/1Nilesh0837)
- Repository: [WebPulse-Analytics](https://github.com/1Nilesh0837/WebPulse-Analytics)
