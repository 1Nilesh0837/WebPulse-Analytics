"""
Command Line Interface for WebPulse Analytics.
"""

import argparse
import sys
from .analyzer import SEOAnalyzer
from .reporter import print_audit_report, generate_json_report, generate_html_report


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="webpulse",
        description="WebPulse Analytics - Fast, in-depth SEO and web audit engine.",
    )
    parser.add_argument(
        "url",
        nargs="?",
        default=None,
        help="Target website URL to analyze (e.g., https://example.com)",
    )
    parser.add_argument(
        "--json",
        dest="json_output",
        metavar="FILE",
        help="Export full audit result to a JSON file.",
    )
    parser.add_argument(
        "--html",
        dest="html_output",
        metavar="FILE",
        help="Export a styled HTML audit dashboard report.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=15,
        help="HTTP request timeout in seconds (default: 15).",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress terminal output (useful when exporting to file).",
    )
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    target_url = args.url
    if not target_url:
        try:
            target_url = input("Enter the URL of the website: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nAudit aborted.")
            sys.exit(0)

    if not target_url:
        print("Error: No URL provided.")
        sys.exit(1)

    analyzer = SEOAnalyzer()
    print(f"Auditing '{target_url}' with WebPulse Analytics...")

    try:
        result = analyzer.audit_url(target_url, timeout=args.timeout)
    except Exception as exc:
        print(f"Error executing audit: {exc}")
        sys.exit(1)

    if not args.quiet:
        print_audit_report(result)

    if args.json_output:
        generate_json_report(result, args.json_output)
        print(f"✔ JSON report saved to: {args.json_output}")

    if args.html_output:
        generate_html_report(result, args.html_output)
        print(f"✔ HTML report saved to: {args.html_output}")


if __name__ == "__main__":
    main()
