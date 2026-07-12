from detectors import (
    detect_base64,
    detect_binary,
    detect_caesar,
    detect_hex,
    identify_hash,
)
from password_cracking import PasswordCracker

STARTUP_MESSAGE = "CTF Assistant started."
EXIT_HINT_MESSAGE = "Type 'exit' to close the program."
PROMPT_MESSAGE = "Enter the text to analyze: "
EXIT_MESSAGE = "Closing the assistant..."
SEPARATOR_MESSAGE = "-" * 40


def analyze_text(text: str) -> str:
    # Order matters: check most specific formats first, then general ones
    
    # 1. Caesar cipher (only letters and spaces)
    if (caesar_result := detect_caesar(text)).matched:
        return f"[Result] The text appears to be {caesar_result.label} and is likely {caesar_result.details}."

    # 2. Binary (only 0s, 1s and spaces)
    if (binary_result := detect_binary(text)).matched:
        return f"[Result] The text appears to be {binary_result.label} and {binary_result.details}."

    # 3. Hash detection (checks exact length: 32, 40, 64 chars in hex)
    if (hash_result := identify_hash(text)).matched:
        return f"[Result] The text appears to be {hash_result.label}."

    # 4. Base64 (specific pattern with +, /, = and valid length)
    if (base64_result := detect_base64(text)).matched:
        return f"[Result] The text appears to be {base64_result.label}."

    # 5. Hexadecimal (most general - any hex string)
    if (hex_result := detect_hex(text)).matched:
        return f"[Result] The text appears to be {hex_result.label}."

    return "[Result] Unknown format."


def main() -> None:
    print(STARTUP_MESSAGE)
    print(EXIT_HINT_MESSAGE + "\n")

    while True:
        user_text = input(PROMPT_MESSAGE)

        if user_text.lower() == "exit":
            print(EXIT_MESSAGE)
            break

        if not user_text.strip():
            continue

        print(analyze_text(user_text))
        print(SEPARATOR_MESSAGE)
        print()


if __name__ == "__main__":
    main()
            

