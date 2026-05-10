# robots-txt-validator

Validates whether the major LLM crawlers (GPTBot, ChatGPT-User, OAI-SearchBot, ClaudeBot, Claude-Web, PerplexityBot, Perplexity-User, Google-Extended, CCBot, Bytespider, Amazonbot, Applebot-Extended) are allowed by a `robots.txt` file.

No third-party dependencies. Python 3.9 or newer, standard library only.

## Why this exists

A site's `robots.txt` is the single cheapest configuration that decides whether generative engines may include the site in their answer stream. A typo, a stale `Disallow: /` left over from a staging environment, or an opt-out token set without the operator's knowledge can make the site invisible to ChatGPT, Claude, Perplexity, Gemini and Copilot.

`robots-txt-validator` parses a `robots.txt` file and reports, for each of the major LLM crawlers, whether a given path is allowed. It exits with a non-zero status if any crawler is disallowed, so it can be wired into CI.

## Crawlers covered

| Token | Operator role |
|---|---|
| `GPTBot` | OpenAI search/training crawler |
| `ChatGPT-User` | OpenAI in-session retrieval agent |
| `OAI-SearchBot` | OpenAI search index crawler |
| `ClaudeBot` | Anthropic crawler |
| `Claude-Web` | Anthropic in-session retrieval agent |
| `PerplexityBot` | Perplexity index crawler |
| `Perplexity-User` | Perplexity in-session retrieval agent |
| `Google-Extended` | Google generative-AI training opt-out token |
| `CCBot` | Common Crawl, used by many model trainers |
| `Bytespider` | ByteDance / Doubao crawler |
| `Amazonbot` | Amazon crawler used by Alexa and Rufus |
| `Applebot-Extended` | Apple generative-AI training opt-out token |

User-Agent tokens reflect the documented public versions as of early 2026. When operators change their tokens, update `CRAWLERS` in `validator.py`.

## Install

```bash
