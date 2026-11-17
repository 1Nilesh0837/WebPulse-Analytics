"""
Reporting module for WebPulse Analytics.
Outputs audit results to Console (Colorized), JSON, or standalone responsive HTML reports.
"""

import json
from typing import Optional
from .analyzer import SEOAuditResult

# ANSI styling helpers (works across modern terminals without mandatory external dependencies)
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"


def print_audit_report(result: SEOAuditResult) -> None:
    """Print an eye-catching, structured terminal summary of the SEO audit."""
    print()
    print(f"{CYAN}{BOLD}{'=' * 65}{RESET}")
    print(f"{CYAN}{BOLD}   ⚡ WEBPULSE ANALYTICS - SEO AUDIT REPORT ⚡{RESET}")
    print(f"{CYAN}{BOLD}{'=' * 65}{RESET}")
    print(f" {BOLD}Target URL:{RESET}     {result.url}")
    print(f" {BOLD}HTTP Status:{RESET}    {result.status_code}")
    print(f" {BOLD}Response Time:{RESET}  {result.response_time_ms:.2f} ms")
    print(f" {BOLD}SSL / HTTPS:{RESET}    {GREEN + 'Secure (HTTPS)' if result.ssl_active else RED + 'Insecure (HTTP)'}{RESET}")
    
    # Grade & Score
    grade_color = GREEN if result.score >= 80 else (YELLOW if result.score >= 60 else RED)
    print(f" {BOLD}SEO Health:{RESET}    {grade_color}{BOLD}{result.score}/100 (Grade {result.grade}){RESET}")
    print(f"{CYAN}{'-' * 65}{RESET}")

    # Title Tag
    print(f"\n{BOLD}[1] Title Tag:{RESET}")
    if result.title:
        status_color = GREEN if result.title_status == "Optimal" else YELLOW
        print(f"   Value:  \"{result.title}\"")
        print(f"   Length: {result.title_length} characters ({status_color}{result.title_status}{RESET})")
        print(f"   Tip:    {result.title_recommendation}")
    else:
        print(f"   {RED}✘ No title tag detected.{RESET}")

    # Meta Description
    print(f"\n{BOLD}[2] Meta Description:{RESET}")
    if result.meta_description:
        status_color = GREEN if result.meta_description_status == "Optimal" else YELLOW
        print(f"   Value:  \"{result.meta_description}\"")
        print(f"   Length: {result.meta_description_length} characters ({status_color}{result.meta_description_status}{RESET})")
        print(f"   Tip:    {result.meta_description_recommendation}")
    else:
        print(f"   {RED}✘ No meta description detected.{RESET}")

    # Headings
    print(f"\n{BOLD}[3] Heading Hierarchy:{RESET}")
    h1_color = GREEN if result.h1_count == 1 else (RED if result.h1_count == 0 else YELLOW)
    print(f"   H1 Count: {h1_color}{result.h1_count}{RESET} ({result.h1_status})")
    for level in range(1, 7):
        key = f"H{level}"
        tags = result.headings.get(key, [])
        if tags:
            sample = f" -> \"{tags[0]}\"" if len(tags) == 1 else f" ({len(tags)} tags)"
            print(f"   {key}: {len(tags)}{sample}")

    # Images
    print(f"\n{BOLD}[4] Image Optimization:{RESET}")
    print(f"   Total Images:         {result.total_images}")
    print(f"   With Alt Attribute:   {GREEN}{result.images_with_alt_count}{RESET}")
    if result.missing_alt_images:
        print(f"   Missing Alt Attribute: {RED}{len(result.missing_alt_images)}{RESET}")
        print(f"   {DIM}Samples missing alt:{RESET}")
        for img in result.missing_alt_images[:4]:
            print(f"     - {img}")
        if len(result.missing_alt_images) > 4:
            print(f"     ... and {len(result.missing_alt_images) - 4} more")
    else:
        print(f"   {GREEN}✔ All images have descriptive alt attributes!{RESET}")

    # Links
    print(f"\n{BOLD}[5] Link Profile:{RESET}")
    print(f"   Total Links:    {result.total_links}")
    print(f"   Internal Links: {result.internal_links}")
    print(f"   External Links: {result.external_links}")
    print(f"   Nofollow Links: {result.nofollow_links}")

    # Technical & Social
    print(f"\n{BOLD}[6] Technical & Social Metadata:{RESET}")
    print(f"   Canonical Tag:  {result.canonical_url or RED + 'Missing' + RESET}")
    print(f"   Robots Meta:    {result.robots_meta or DIM + 'Default (index, follow)' + RESET}")
    print(f"   Mobile Viewport:{GREEN + 'Configured' if result.viewport_meta else RED + 'Missing'}{RESET}")
    print(f"   Favicon:        {GREEN + 'Present' if result.favicon_found else YELLOW + 'Not Found'}{RESET}")
    print(f"   Open Graph:     {GREEN + str(len(result.open_graph)) + ' tags' if result.open_graph else YELLOW + 'None'}{RESET}")
    print(f"   Twitter Card:   {GREEN + str(len(result.twitter_card)) + ' tags' if result.twitter_card else YELLOW + 'None'}{RESET}")

    # Recommendations
    print(f"\n{BOLD}[7] Actionable Recommendations:{RESET}")
    if result.recommendations:
        for idx, tip in enumerate(result.recommendations, 1):
            print(f"   {YELLOW}{idx}.{RESET} {tip}")
    else:
        print(f"   {GREEN}✔ Outstanding! No major SEO bottlenecks identified.{RESET}")

    print(f"\n{CYAN}{'=' * 65}{RESET}\n")


def generate_json_report(result: SEOAuditResult, file_path: Optional[str] = None) -> str:
    """Serialize the audit result to formatted JSON."""
    data = result.to_dict()
    rendered = json.dumps(data, indent=2)
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(rendered)
    return rendered


def generate_html_report(result: SEOAuditResult, file_path: Optional[str] = None) -> str:
    """Generate a sleek, standalone HTML audit dashboard."""
    grade_color = "#10b981" if result.score >= 80 else ("#f59e0b" if result.score >= 60 else "#ef4444")
    
    rec_items = "".join(f"<li>{r}</li>" for r in result.recommendations) if result.recommendations else "<li>No critical issues found!</li>"
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>WebPulse Analytics - SEO Audit Report ({result.url})</title>
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-dim: #94a3b8;
      --primary: #38bdf8;
      --accent: {grade_color};
      --border: #334155;
    }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      margin: 0;
      padding: 2rem 1rem;
    }}
    .container {{
      max-width: 900px;
      margin: 0 auto;
    }}
    .header {{
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 2px solid var(--border);
      padding-bottom: 1.5rem;
      margin-bottom: 2rem;
    }}
    .title h1 {{
      margin: 0 0 0.5rem 0;
      color: var(--primary);
      font-size: 1.75rem;
    }}
    .title p {{
      margin: 0;
      color: var(--text-dim);
      font-size: 0.95rem;
    }}
    .score-badge {{
      text-align: center;
      background: var(--card-bg);
      padding: 1rem 1.5rem;
      border-radius: 12px;
      border: 2px solid var(--accent);
    }}
    .score-number {{
      font-size: 2.5rem;
      font-weight: 800;
      color: var(--accent);
      line-height: 1;
    }}
    .score-grade {{
      font-size: 1rem;
      color: var(--text-dim);
      margin-top: 0.25rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 1.25rem;
      margin-bottom: 2rem;
    }}
    .card {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 1.25rem;
    }}
    .card h3 {{
      margin-top: 0;
      margin-bottom: 0.75rem;
      color: var(--primary);
      font-size: 1.1rem;
    }}
    .metric {{
      display: flex;
      justify-content: space-between;
      padding: 0.4rem 0;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      font-size: 0.9rem;
    }}
    .metric-val {{
      font-weight: 600;
    }}
    .recommendations {{
      background: var(--card-bg);
      border-left: 4px solid var(--accent);
      border-radius: 8px;
      padding: 1.5rem;
    }}
    .recommendations h3 {{
      margin-top: 0;
      color: var(--text);
    }}
    .recommendations ul {{
      margin: 0;
      padding-left: 1.25rem;
      color: var(--text-dim);
      line-height: 1.6;
    }}
    footer {{
      margin-top: 3rem;
      text-align: center;
      color: var(--text-dim);
      font-size: 0.85rem;
    }}
  </style>
</head>
<body>
  <div class="container">
    <div class="header">
      <div class="title">
        <h1>⚡ WebPulse Analytics</h1>
        <p>Target: <strong>{result.url}</strong> | Response: {result.response_time_ms:.1f}ms</p>
      </div>
      <div class="score-badge">
        <div class="score-number">{result.score}</div>
        <div class="score-grade">Grade {result.grade}</div>
      </div>
    </div>

    <div class="grid">
      <div class="card">
        <h3>Metadata Quality</h3>
        <div class="metric"><span>Title Status:</span><span class="metric-val">{result.title_status}</span></div>
        <div class="metric"><span>Title Length:</span><span class="metric-val">{result.title_length} chars</span></div>
        <div class="metric"><span>Meta Desc Status:</span><span class="metric-val">{result.meta_description_status}</span></div>
        <div class="metric"><span>Meta Desc Length:</span><span class="metric-val">{result.meta_description_length} chars</span></div>
      </div>

      <div class="card">
        <h3>Content & Structure</h3>
        <div class="metric"><span>H1 Heading Status:</span><span class="metric-val">{result.h1_status}</span></div>
        <div class="metric"><span>Total Images:</span><span class="metric-val">{result.total_images}</span></div>
        <div class="metric"><span>Images Missing Alt:</span><span class="metric-val" style="color: {'#ef4444' if result.missing_alt_images else '#10b981'}">{len(result.missing_alt_images)}</span></div>
        <div class="metric"><span>Total Links:</span><span class="metric-val">{result.total_links}</span></div>
      </div>

      <div class="card">
        <h3>Technical & Social</h3>
        <div class="metric"><span>SSL Encryption:</span><span class="metric-val">{'Secure (HTTPS)' if result.ssl_active else 'Insecure'}</span></div>
        <div class="metric"><span>Mobile Viewport:</span><span class="metric-val">{'Configured' if result.viewport_meta else 'Missing'}</span></div>
        <div class="metric"><span>Canonical URL:</span><span class="metric-val">{'Specified' if result.canonical_url else 'None'}</span></div>
        <div class="metric"><span>Open Graph:</span><span class="metric-val">{len(result.open_graph)} tags</span></div>
      </div>
    </div>

    <div class="recommendations">
      <h3>Priority Action Items</h3>
      <ul>
        {rec_items}
      </ul>
    </div>

    <footer>
      Generated by <strong>WebPulse Analytics</strong> &bull; Crafted by <a href="https://github.com/1Nilesh0837" style="color: var(--primary); text-decoration: none;">Nilesh Sahoo</a>
    </footer>
  </div>
</body>
</html>
"""
    if file_path:
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html)
    return html
