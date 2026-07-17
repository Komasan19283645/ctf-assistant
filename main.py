import argparse
import sys
from pathlib import Path

from rich.console import Console
from rich.rule import Rule

from detectors import detect_base64, detect_binary, detect_caesar, detect_hex, identify_hash
from password_cracking import PasswordCracker
from config import WORDLIST_PATH
from ai_client import analyze_challenge
from file_use import read_file_input

console = Console(highlight=False)

EXIT_MESSAGE = "Bye."


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="CTF Assistant")
    parser.add_argument("-f", "--file", help="Path to a text file to analyze")
    return parser.parse_args()


def safe_input(prompt: str) -> str | None:
    try:
        return input(prompt)
    except EOFError:
        console.print(f"\n[dim]{EXIT_MESSAGE}[/dim]")
        return None


def analyze_text(text: str) -> str:
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
            details = f" · {result.details}" if result.details else ""
            return f"{result.label}{details}"

    return "Unknown format"


def prompt_wordlist(cracker: PasswordCracker) -> bool:
    raw = safe_input("  wordlist path [default]: ")
    if raw is None:
        return False

    path_str = raw.strip().strip('"') or WORDLIST_PATH
    path = Path(path_str)

    if not path.is_file():
        console.print("[red]  error[/red]  file not found")
        return False

    cracker.set_wordlist(path)
    console.print(f"[dim]  loaded  {path}[/dim]")
    return True


def ensure_wordlist(cracker: PasswordCracker) -> bool:
    if cracker.wordlist_path is not None:
        return True
    console.print("[dim]  no wordlist set[/dim]")
    return prompt_wordlist(cracker)


def execute_crack(cracker: PasswordCracker, target_hash: str, algorithm: str) -> None:
    result = cracker.crack_hash(target_hash, algorithm)
    if result.matched:
        console.print(f"[green]  found[/green]   {result.password}  [dim]({result.label})[/dim]")
    else:
        console.print(f"[dim]  {result.details or 'no match found'}[/dim]")


def handle_hash(cracker: PasswordCracker, text: str) -> bool:
    hash_result = identify_hash(text)
    if not hash_result.matched:
        return False

    console.print(f"[cyan]  hash[/cyan]    {hash_result.label}")

    raw = safe_input("  crack? (y/n): ")
    if raw is None or raw.strip().lower() not in {"y", "yes", "s", "si"}:
        return True

    if not ensure_wordlist(cracker):
        return True

    execute_crack(cracker, text.strip(), hash_result.algorithm)
    return True


def handle_ai() -> None:
    console.print("[dim]  paste challenge · type END to submit[/dim]")
    lines = []
    while True:
        line = safe_input("  > ")
        if line is None:
            return
        if line.strip() == "END":
            break
        lines.append(line)

    description = "\n".join(lines).strip()
    if not description:
        console.print("[dim]  empty, aborting[/dim]")
        return

    backend = safe_input("  backend (local/cloud) [local]: ")
    if backend is None:
        return
    backend = backend.strip().lower() or "local"

    console.print(f"[dim]  querying {backend}...[/dim]")
    try:
        response = analyze_challenge(description, backend)
        console.print()
        console.rule("[dim]ai analysis[/dim]", style="dim")
        console.print(response)
        console.rule(style="dim")
    except Exception as e:
        console.print(f"[red]  error[/red]   {e}")


def main() -> None:
    args = parse_args()

    if args.file:
        result = read_file_input(args.file)
        if not result.success:
            console.print(f"[red]error[/red]  {result.error}", file=sys.stderr)
            sys.exit(1)

        label = analyze_text(result.content)
        console.print(f"[cyan]result[/cyan]  {label}")
        return

    console.print("[bold cyan]ctf-assistant[/bold cyan]  [dim]exit · ai[/dim]")
    console.rule(style="dim")

    cracker = PasswordCracker()

    while True:
        raw = safe_input("\n> ")
        if raw is None:
            break

        text = raw.strip()

        if text.lower() == "exit":
            console.print(f"[dim]{EXIT_MESSAGE}[/dim]")
            break

        if text.lower() == "ai":
            handle_ai()
            continue

        if not text:
            continue

        if not handle_hash(cracker, text):
            label = analyze_text(text)
            console.print(f"[cyan]result[/cyan]  {label}")

        console.rule(style="dim")


if __name__ == "__main__":
    main()