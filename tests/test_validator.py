"""Tests for robots-txt-validator. Run with: python3 -m unittest discover tests"""

import sys
import unittest
from pathlib import Path

# Make validator.py importable from the project root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from validator import evaluate, CRAWLERS


class TestEvaluate(unittest.TestCase):
    def test_all_allowed_by_default(self):
        """An empty robots.txt allows everything."""
        results = evaluate("", "https://example.com/", "/")
        for r in results:
            self.assertTrue(r["allowed"], f"{r['user_agent']} should be allowed by empty robots.txt")

    def test_global_block(self):
        """A global Disallow: / blocks every crawler in CRAWLERS."""
        robots = "User-agent: *\nDisallow: /\n"
        results = evaluate(robots, "https://example.com/", "/")
        for r in results:
            self.assertFalse(r["allowed"], f"{r['user_agent']} should be disallowed by global block")

    def test_gptbot_specifically_blocked(self):
        """A GPTBot-specific block only affects GPTBot."""
        robots = "User-agent: GPTBot\nDisallow: /\n\nUser-agent: *\nAllow: /\n"
        results = evaluate(robots, "https://example.com/", "/")
        results_by_ua = {r["user_agent"]: r["allowed"] for r in results}
        self.assertFalse(results_by_ua["GPTBot"])
        self.assertTrue(results_by_ua["ClaudeBot"])
        self.assertTrue(results_by_ua["PerplexityBot"])

    def test_path_specific_block(self):
        """A path-specific block only affects that path."""
        robots = "User-agent: *\nDisallow: /private/\n"
        results_root = evaluate(robots, "https://example.com/", "/")
        results_priv = evaluate(robots, "https://example.com/", "/private/page")
        for r in results_root:
            self.assertTrue(r["allowed"])
        for r in results_priv:
            self.assertFalse(r["allowed"])

    def test_crawler_list_shape(self):
        """Every CRAWLERS entry is a (token, note) tuple of two non-empty strings."""
        for entry in CRAWLERS:
            self.assertEqual(len(entry), 2)
            ua, note = entry
            self.assertIsInstance(ua, str)
            self.assertIsInstance(note, str)
            self.assertTrue(ua)
            self.assertTrue(note)


if __name__ == "__main__":
    unittest.main()
