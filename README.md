# CTF Assistant

> A lightweight command-line assistant and library for solving common CTF tasks: format detection, hash cracking with mutation strategies, and LLM-assisted challenge analysis.

## Features
- Detects common encodings and formats: Base64, Hex, Binary, Caesar cipher.
- Identifies common hash algorithms (MD5, SHA-1, SHA-256) by length and format.
- Offline hash cracking using wordlists with candidate mutation strategies (suffixes, years, symbols, case variants).
- Integrates with local or cloud LLM endpoints to generate challenge analyses and exploit templates.
- Small, testable codebase intended for interactive use and automation.

## Requirements
- Python 3.10+
- Install runtime dependencies from `requirements.txt`.

## Installation
1. Clone the repository:

```bash
git clone <repo-url>
cd ctf-assistant
```

2. Create and activate a virtual environment (Windows example):

```powershell
python -m venv venv
venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration
- `ctf/config.py` contains the following configurable values:
  - `WORDLIST_PATH`: default path to the wordlist (adjust to your local `rockyou` or other dictionary).
  - `LMSTUDIO_BASE_URL` and `LMSTUDIO_MODEL`: local LLM endpoint settings.
  - `OPENROUTER_BASE_URL`, `OPENROUTER_MODEL`, `OPENROUTER_API_KEY`: cloud LLM settings.
  - `SYSTEM_PROMPT`: system prompt sent to the LLM (careful; it instructs exploit generation).

If you plan to use the cloud backend, set `OPENROUTER_API_KEY` as an environment variable:

```powershell
setx OPENROUTER_API_KEY "your_api_key_here"
```

## Usage

### Interactive CLI
Run the main interactive interface:

```bash
python -m ctf.main
```

- Type a text string or hash at the prompt to detect its format.
- Type `ai` to paste a multi-line CTF challenge. Finish input with a line containing only `END`.
  - You will be prompted to choose `local` or `cloud` backend.
- Type `exit` to quit.

### Analyze a file

```bash
python -m ctf.main -f path/to/file.txt
```

### Typical workflow
1. Use the detector to identify the format (Base64, Hex, Binary, Caesar, or Hash).
2. If a hash is detected, opt to crack it. If no wordlist is set, you will be prompted to provide one.
3. For CTF challenges, use `ai` to request an LLM-powered analysis or exploit template.

## Modules and Public API
Below is a concise reference of the main modules and their primary functions/classes.

- [ctf/ai_client.py](ctf/ai_client.py)
  - `call_api(base_url, model, messages, api_key="") -> str` — low-level API call to chat/completions.
  - `ask_local(prompt) -> str` — call configured local LLM.
  - `ask_cloud(prompt) -> str` — call configured cloud LLM.
  - `analyze_challenge(description, backend="local") -> str` — convenience wrapper to analyze a challenge.

- [ctf/config.py](ctf/config.py)
  - Configuration constants: `WORDLIST_PATH`, LLM endpoints and `SYSTEM_PROMPT`.

- [ctf/detectors.py](ctf/detectors.py)
  - `DetectionResult`, `HashDetectionResult` dataclasses.
  - `detect_base64(text)`, `detect_hex(text)`, `detect_binary(text)`, `detect_caesar(text)` — return `DetectionResult`.
  - `identify_hash(text) -> HashDetectionResult` — identifies MD5, SHA-1, SHA-256 by length/format.

- [ctf/file_use.py](ctf/file_use.py)
  - `FileReadResult` dataclass.
  - `read_file_input(filepath) -> FileReadResult` — safe file reading with error reporting.

- [ctf/password_cracking.py](ctf/password_cracking.py)
  - `HashCrackResult` dataclass.
  - `PasswordCracker` class with methods:
    - `set_wordlist(path)` — set a `Path` to a wordlist.
    - `iter_candidates()` — iterate raw words from the wordlist.
    - `mutate(word)` — generate candidate variants (case, numeric suffixes, years, symbols).
    - `crack_hash(target_hash, algorithm)` — attempt to crack using supported algorithms (`md5`, `sha1`, `sha256`).

- [ctf/main.py](ctf/main.py)
  - CLI entrypoint and interactive loop.
  - Helpers: `analyze_text`, `handle_hash`, `handle_ai`, `ensure_wordlist`.

## Testing
- The repository includes test artifacts and example scripts: `test_all.py`, `test_detectors.py`, and multiple `test_*.txt` files.
- Run tests locally using `pytest` (recommended):

```bash
pytest -q
```

Or run the provided test script (if applicable):

```bash
python test_all.py
```

## Security and Responsible Use
- The LLM prompt (`SYSTEM_PROMPT`) is designed to produce exploit code. Use the tool only in legal, ethical contexts (e.g., CTFs, educational labs with permission).
- Do not commit secrets or API keys to the repository.

## Contributing
- Fork the repository and open a pull request with a clear description and tests.
- Add unit tests for any new detector or mutation behavior.

## License
Add a `LICENSE` file to indicate the intended license (e.g., MIT, Apache-2.0). If none is present, clarify licensing before publishing.

---

If you want, I can:
- commit this `README.md` to the repository (I already created it),
- run the test suite now, or
- add a brief `CONTRIBUTING.md` and `LICENSE` template.
