# Contributing

Thank you for your interest in contributing to CTF Assistant. This document explains the recommended workflow, code standards, and how to run tests locally.

## How to contribute

1. Fork the repository and create a feature branch named `feat/<short-description>` or a bugfix branch `fix/<short-description>`.
2. Keep changes focused and add tests for new behavior.
3. Open a Pull Request with a clear description, testing steps, and rationale.

## Development setup

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run tests:

```bash
pytest -q
```

## Code style
- Keep consistent with existing repository style. Use `black` (optional) and aim for readable, well-documented code.

## Commit messages
- Use concise, imperative messages: `Add feature X`, `Fix bug Y`, `Update README`.

## Review process
- PRs should include tests where applicable.
- Maintain backward compatibility when possible. Document breaking changes.

## Security
- Do not commit secrets, API keys, or credentials. Report vulnerabilities privately via the repository owner.
