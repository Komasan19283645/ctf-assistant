import base64
from dataclasses import dataclass
import string
import re

STARTUP_MESSAGE = "CTF Assistant started."
EXIT_HINT_MESSAGE = "Type 'exit' to close the program."
PROMPT_MESSAGE = "Enter the text to analyze: "
EXIT_MESSAGE = "Closing the assistant..."
SEPARATOR_MESSAGE = "-" * 40


@dataclass(frozen=True)
class DetectionResult:
    matched: bool
    label: str
    details: str = ""

def detect_base64(text: str) -> DetectionResult:
    text = text.strip() # Remove leading/trailing whitespace
    
    # Base64 only uses A-Z, a-z, 0-9, +, /, and = for padding
    if not re.fullmatch(r'[A-Za-z0-9+/]*={0,2}', text):
        return DetectionResult(False, "Base64")
    
    # The length must be a multiple of 4
    if len(text) % 4 != 0 or len(text) == 0:
        return DetectionResult(False, "Base64")
    
    try:
        # Decode and re-encode to validate the format
        decoded = base64.b64decode(text, validate=True)
        return DetectionResult(base64.b64encode(decoded).decode() == text, "Base64")
    except Exception:
        return DetectionResult(False, "Base64")

def detect_hex(text: str) -> DetectionResult:
    text = text.strip()  # Remove leading/trailing whitespace

    # Hexadecimal can optionally start with '0x' or '#', followed by hex digits
    if not re.fullmatch(r'^(0x|#)?[0-9a-fA-F]+$', text):
        return DetectionResult(False, "Hexadecimal")
    
    if text.startswith("0x"):
        text = text[2:]  # Remove the "0x" prefix
    elif text.startswith("#"):
        text = text[1:]  # Remove the leading "#"

    try:
        bytes.fromhex(text)  # Validate hex string
        return DetectionResult(True, "Hexadecimal")
    except ValueError:
        return DetectionResult(False, "Hexadecimal")

def detect_caesar(text: str) -> DetectionResult:

    common_english_words = [
        "the", "is", "and", "you", "this", "that", "with", "for",
        "are", "was", "have", "hello", "world", "what", "flag",
        "to", "of", "in", "it", "not", "on", "be", "as", "at",
        "word", "text", "code", "cipher", "secret",
    ]
    common_spanish_words = [
        "el", "la", "los", "las", "un", "una", "unos", "unas", "este", "esta", "eso",
        "yo", "tu", "el", "ella", "nosotros", "ellos", "que", "su", "sus", "me", "te", "se",
        "de", "en", "con", "por", "para", "sin", "sobre", "entre", "hasta", "desde",
        "y", "o", "pero", "porque", "si", "no", "como", "cuando", "donde",
        "es", "son", "esta", "estan", "hay", "ser", "estar", "tener", "hacer",
        "puede", "puedes", "quiero", "vamos", "fue", "era",
        "flag", "bandera", "contrasena", "clave", "hola", "mundo", "secreto",
        "mensaje", "texto", "codigo", "encontrar", "buscar",
    ]

    for char in text:
        if char in string.ascii_lowercase or char in string.ascii_uppercase or char == " ":
            continue
        return DetectionResult(False, "Caesar cipher")
    
    relevant_positions = 0
    best_shift = 0
    for i in range(1, 26): # Shift values from 1 to 25
        cont = 0
        decrypted_text = ""

        for char in text:
            if char in string.ascii_lowercase:
                decrypted_text += chr((ord(char) - ord('a') - i) % 26 + ord('a'))
            elif char in string.ascii_uppercase:
                decrypted_text += chr((ord(char) - ord('A') - i) % 26 + ord('A'))
            else:
                decrypted_text += char  # Non-alphabetic characters remain unchanged
        
        split_text = decrypted_text.split()

        for word in split_text:
            if word.lower() in common_english_words or word.lower() in common_spanish_words:
                cont += 1
        
        if cont > relevant_positions:
            relevant_positions = cont
            best_shift = i

    if relevant_positions >= 1:
        return DetectionResult(True, "Caesar cipher", f"rotated {best_shift} positions")
    return DetectionResult(False, "Caesar cipher")

def detect_binary(text: str) -> DetectionResult:
    text = text.strip()

    for char in text:
        if char == "0" or char == "1" or char == " ":
            continue
        return DetectionResult(False, "binary")

    bits = text.replace(" ", "")
    if len(bits) < 8 or len(bits) % 8 != 0:
        return DetectionResult(False, "binary")

    try:
        decoded_bytes = bytes(
            int(bits[index:index + 8], 2)
            for index in range(0, len(bits), 8)
        )
        decoded_text = decoded_bytes.decode("utf-8")
    except (ValueError, UnicodeDecodeError):
        return DetectionResult(False, "binary")

    if not decoded_text.isprintable():
        return DetectionResult(False, "binary")

    return DetectionResult(True, "binary", f"decodes to {decoded_text!r}")

if __name__ == "__main__":
    print(STARTUP_MESSAGE)
    print(EXIT_HINT_MESSAGE + "\n")

    # Infinite loop to keep prompting for text until you type exit
    while True:
        # input() pauses the program and waits for the user to type and press Enter
        user_text = input(PROMPT_MESSAGE)

        # Exit condition
        if user_text.lower() == "exit":
            print(EXIT_MESSAGE)
            break
        
        # Skip empty input if you press Enter by accident
        if not user_text.strip():
            continue

        # Run the text through our detectors
        if (binary_result := detect_binary(user_text)).matched:
            print(f"[Result] The text appears to be {binary_result.label} and {binary_result.details}.")
        elif (hex_result := detect_hex(user_text)).matched:
            print(f"[Result] The text appears to be {hex_result.label}.")
        elif (base64_result := detect_base64(user_text)).matched:
            print(f"[Result] The text appears to be {base64_result.label}.")
        elif (caesar_result := detect_caesar(user_text)).matched:
            print(f"[Result] The text appears to be {caesar_result.label} and is likely {caesar_result.details}.")
        else:
            print("[Result] Unknown format.")

        print(SEPARATOR_MESSAGE)
        print()
            

