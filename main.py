import argparse
import sys
from pathlib import Path

from detectors import detect_base64, detect_binary, detect_caesar, detect_hex, identify_hash
from password_cracking import PasswordCracker
from config import WORDLIST_PATH
from ai_client import analyze_challenge
from file_use import read_file_input

STARTUP_MESSAGE = "CTF Assistant started."
EXIT_HINT       = "Type 'exit' to quit. Type 'ai' for challenge analysis."
SEPARATOR       = "-" * 40
EXIT_MESSAGE    = "Closing the assistant..."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CTF Assistant")
    parser.add_argument("-f", "--file", help="Path to a text file to analyze")
    return parser.parse_args()


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
    raw = safe_input("Wordlist path [Default]: ")
    if raw is None:
        return False

    path_str = raw.strip().strip('"') or WORDLIST_PATH
    path = Path(path_str)

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


def execute_crack(cracker: PasswordCracker, target_hash: str, algorithm: str) -> None:
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

    execute_crack(cracker, text.strip(), hash_result.algorithm)
    return True


def handle_ai() -> None:
    print("[AI] Enter challenge description (Type 'END' on a new line to submit):")
    lines = []
    while True:
        line = safe_input("> ")
        if line is None:
            return
        if line.strip() == "END":
            break
        lines.append(line)

    description = "\n".join(lines).strip()
    if not description:
        print("[AI] Empty description, aborting.")
        return

    backend = safe_input("Backend (local/cloud) [local]: ")
    if backend is None:
        return
    backend = backend.strip().lower() or "local"

    print(f"[AI] Analyzing with {backend} model...")
    try:
        response = analyze_challenge(description, backend)
        print("\n--- AI Analysis ---\n" + response + "\n-------------------")
    except Exception as e:
        print(f"[AI Error] Failed to reach API: {e}")


def main() -> None:
    args = parse_args()

    if args.file:
        result = read_file_input(args.file)
        if not result.success:
            print(f"Error: {result.error}", file=sys.stderr)
            sys.exit(1)

        print(analyze_text(result.content))
        return

    print(STARTUP_MESSAGE)
    print(EXIT_HINT + "\n")

    cracker = PasswordCracker()

    while True:
        raw = safe_input("Enter text to analyze (or 'exit' / 'ai'): ")
        if raw is None:
            break

        text = raw.strip()

        if text.lower() == "exit":
            print(EXIT_MESSAGE)
            break

        if text.lower() == "ai":
            handle_ai()
            print(SEPARATOR)
            continue

        if not text:
            continue

        if not handle_hash(cracker, text):
            print(analyze_text(text))

        print(SEPARATOR)


if __name__ == "__main__":
    main()