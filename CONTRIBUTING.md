# Contributing

Thank you for considering a contribution to `robots-txt-validator`.

## Reporting issues

Open a GitHub issue with:

- The `robots.txt` URL you tested (or paste the relevant rules)
- The command you ran and the output you got
- The output you expected and why
- Your Python version (`python3 --version`)
- Operating system

For security-relevant findings, please follow [SECURITY.md](./SECURITY.md) instead.

## Suggesting changes

Open an issue first to discuss substantial changes. Small fixes (typos, additional crawler tokens, clearer error messages) can go straight to a pull request.

## Pull requests

- Fork the repository, create a topic branch from `main`
- Keep changes focused; one concern per pull request
- Match the existing code style (standard library only, no external dependencies, PEP 8)
- Update the README if user-facing behavior changes
- Add or update tests in `tests/` for new logic
- Run `python3 -m unittest discover tests` before submitting

## Adding a crawler token

If you add a User-Agent token to `CRAWLERS` in `validator.py`, include:

- A link to the operator's public documentation of the token
- The date the token was verified
- A one-line description of the operator role

## Code of conduct

Participation in this project is governed by the [Code of Conduct](./CODE_OF_CONDUCT.md).
