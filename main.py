from pathlib import Path

from detectors import detect_base64, detect_binary, detect_caesar, detect_hex, identify_hash
from password_cracking import PasswordCracker

STARTUP_MESSAGE  = "CTF Assistant started."
EXIT_HINT        = "Type 'exit' to quit."
SEPARATOR        = "-" * 40
EXIT_MESSAGE     = "Closing the assistant..."


def safe_input(prompt: str) -> str | None:
    try:
        return input(prompt)
    except EOFError:
        print("\n" + EXIT_MESSAGE)
        return None


def analyze_text(text: str) -> str:
    # Order matters: most specific first, most general last
    checks = [
        detect_caesar,
        detect_binary,
        identify_hash,
        detect_base64,
        detect_hex,
    ]
    for detect in checks:
        result = detect(text)
        if result.matched:
            details = f" and {result.details}" if result.details else ""
            return f"[Result] {result.label}{details}."

    return "[Result] Unknown format."


def prompt_wordlist(cracker: PasswordCracker) -> bool:
    raw = safe_input("Wordlist path: ")
    if raw is None:
        return False

    path = Path(raw.strip().strip('"'))
    if not path.is_file():
        print("[Wordlist] File not found.")
        return False

    cracker.set_wordlist(path)
    print(f"[Wordlist] Loaded: {path}")
    return True


def ensure_wordlist(cracker: PasswordCracker) -> bool:
    if cracker.wordlist_path is not None:
        return True
    print("[Crack] No wordlist loaded. Set one now.")
    return prompt_wordlist(cracker)


def crack_hash(cracker: PasswordCracker, target_hash: str, algorithm: str) -> None:
    result = cracker.crack_hash(target_hash, algorithm)
    if result.matched:
        print(f"[Crack] Match found: {result.password} ({result.label})")
    else:
        print(f"[Crack] {result.details or 'No match found.'}")


def handle_hash(cracker: PasswordCracker, text: str) -> bool:
    hash_result = identify_hash(text)
    if not hash_result.matched:
        return False

    print(f"[Result] {hash_result.label}.")

    raw = safe_input("Crack it now? (y/n): ")
    if raw is None or raw.strip().lower() not in {"y", "yes", "s", "si"}:
        return True

    if not ensure_wordlist(cracker):
        return True

    crack_hash(cracker, text.strip(), hash_result.algorithm)
    return True


def main() -> None:
    print(STARTUP_MESSAGE)
    print(EXIT_HINT + "\n")

    cracker = PasswordCracker()

    while True:
        raw = safe_input("Enter text to analyze (or 'exit'): ")
        if raw is None:
            break

        text = raw.strip()

        if text.lower() == "exit":
            print(EXIT_MESSAGE)
            break

        if not text:
            continue

        if not handle_hash(cracker, text):
            print(analyze_text(text))

        print(SEPARATOR)


if __name__ == "__main__":
    main()