from detectors import (
    detect_base64,
    detect_binary,
    detect_caesar,
    detect_hex,
    identify_hash,
)

STARTUP_MESSAGE = "CTF Assistant started."
EXIT_HINT_MESSAGE = "Type 'exit' to close the program."
PROMPT_MESSAGE = "Enter the text to analyze: "
EXIT_MESSAGE = "Closing the assistant..."
SEPARATOR_MESSAGE = "-" * 40


def analyze_text(text: str) -> str:
    if (binary_result := detect_binary(text)).matched:
        return f"[Result] The text appears to be {binary_result.label} and {binary_result.details}."

    if (hash_result := identify_hash(text)).matched:
        return f"[Result] The text appears to be {hash_result.label}."

    if (hex_result := detect_hex(text)).matched:
        return f"[Result] The text appears to be {hex_result.label}."

    if (base64_result := detect_base64(text)).matched:
        return f"[Result] The text appears to be {base64_result.label}."

    if (caesar_result := detect_caesar(text)).matched:
        return f"[Result] The text appears to be {caesar_result.label} and is likely {caesar_result.details}."

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
            

