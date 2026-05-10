"""
robots-txt-validator

Checks whether the major LLM crawlers are allowed by a robots.txt file.

Usage:
    python3 validator.py https://example.com/robots.txt
    python3 validator.py https://example.com/robots.txt --json
    python3 validator.py https://example.com/robots.txt --path /blog/

No third-party dependencies. Python 3.9+, standard library only.
"""

import argparse
import json
import sys
import urllib.request
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

# Crawlers covered. User-Agent tokens as documented by their operators
# as of early 2026. Update this list when operators change their strings.
CRAWLERS = [
    ("GPTBot",          "OpenAI search/training crawler"),
    ("ChatGPT-User",    "OpenAI in-session retrieval agent"),
    ("OAI-SearchBot",   "OpenAI search index crawler"),
    ("ClaudeBot",       "Anthropic crawler"),
    ("Claude-Web",      "Anthropic in-session retrieval agent"),
    ("PerplexityBot",   "Perplexity index crawler"),
    ("Perplexity-User", "Perplexity in-session retrieval agent"),
    ("Google-Extended", "Google generative-AI training opt-out token"),
    ("CCBot",           "Common Crawl, used by many model trainers"),
    ("Bytespider",      "ByteDance / Doubao crawler"),
    ("Amazonbot",       "Amazon crawler used by Alexa and Rufus"),
    ("Applebot-Extended", "Apple generative-AI training opt-out token"),
]


def fetch_robots(url: str, timeout: int = 10) -> str:
    """Fetch the raw text of a robots.txt file."""
    req = urllib.request.Request(url, headers={"User-Agent": "robots-txt-validator/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")


def evaluate(robots_text: str, base_url: str, path: str = "/") -> list:
    """Run each crawler against the policy. Return list of result dicts."""
    rp = RobotFileParser()
    rp.parse(robots_text.splitlines())
    target = urljoin(base_url, path)
    results = []
    for ua, note in CRAWLERS:
        allowed = rp.can_fetch(ua, target)
        results.append({
            "user_agent": ua,
            "note": note,
            "path": path,
            "allowed": allowed,
        })
    return results


def render_table(results: list, robots_url: str, path: str) -> str:
    """Format results as a human-readable text table."""
    lines = [
        f"robots.txt: {robots_url}",
        f"path tested: {path}",
        "",
        f"{'Crawler':<22}{'Allowed':<10}Note",
        "-" * 78,
    ]
    for r in results:
        flag = "yes" if r["allowed"] else "DISALLOWED"
        lines.append(f"{r['user_agent']:<22}{flag:<10}{r['note']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate whether major LLM crawlers are allowed by a robots.txt file.",
    )
    parser.add_argument(
        "url",
        help="Full URL to a robots.txt file (e.g. https://example.com/robots.txt).",
    )
    parser.add_argument(
        "--path",
        default="/",
        help="Path on the target site to test against (default: /).",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=10,
        help="HTTP timeout in seconds (default: 10).",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit machine-readable JSON instead of a text table.",
    )
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if not parsed.scheme or not parsed.netloc:
        print("Error: please pass a full URL including scheme.", file=sys.stderr)
        return 2

    try:
        robots_text = fetch_robots(args.url, timeout=args.timeout)
    except Exception as exc:
        print(f"Error fetching robots.txt: {exc}", file=sys.stderr)
        return 1

    results = evaluate(robots_text, args.url, args.path)

    if args.json:
        print(json.dumps({
            "robots_url": args.url,
            "path": args.path,
            "results": results,
        }, indent=2))
    else:
        print(render_table(results, args.url, args.path))

    # Exit non-zero if any crawler is disallowed — useful in CI.
    return 0 if all(r["allowed"] for r in results) else 1


if __name__ == "__main__":
    sys.exit(main())
