from __future__ import annotations

import base64
import re
import string
from dataclasses import dataclass


@dataclass(frozen=True)
class DetectionResult:
    matched: bool
    label: str
    details: str = ""


COMMON_ENGLISH_WORDS = frozenset(
    {
        "the", "is", "and", "you", "this", "that", "with", "for",
        "are", "was", "have", "hello", "world", "what", "flag",
        "to", "of", "in", "it", "not", "on", "be", "as", "at",
        "word", "text", "code", "cipher", "secret",
    }
)

COMMON_SPANISH_WORDS = frozenset(
    {
        "el", "la", "los", "las", "un", "una", "unos", "unas", "este", "esta", "eso",
        "yo", "tu", "ella", "nosotros", "ellos", "que", "su", "sus", "me", "te", "se",
        "de", "en", "con", "por", "para", "sin", "sobre", "entre", "hasta", "desde",
        "y", "o", "pero", "porque", "si", "no", "como", "cuando", "donde",
        "es", "son", "estan", "hay", "ser", "estar", "tener", "hacer",
        "puede", "puedes", "quiero", "vamos", "fue", "era",
        "flag", "bandera", "contrasena", "clave", "hola", "mundo", "secreto",
        "mensaje", "texto", "codigo", "encontrar", "buscar",
    }
)


def detect_base64(text: str) -> DetectionResult:
    text = text.strip()

    if not re.fullmatch(r"[A-Za-z0-9+/]*={0,2}", text):
        return DetectionResult(False, "Base64")

    if len(text) % 4 != 0 or len(text) == 0:
        return DetectionResult(False, "Base64")

    try:
        decoded = base64.b64decode(text, validate=True)
        return DetectionResult(base64.b64encode(decoded).decode() == text, "Base64")
    except Exception:
        return DetectionResult(False, "Base64")


def detect_hex(text: str) -> DetectionResult:
    text = text.strip()

    if not re.fullmatch(r"^(0x|#)?[0-9a-fA-F]+$", text):
        return DetectionResult(False, "Hexadecimal")

    if text.startswith("0x"):
        text = text[2:]
    elif text.startswith("#"):
        text = text[1:]

    try:
        bytes.fromhex(text)
        return DetectionResult(True, "Hexadecimal")
    except ValueError:
        return DetectionResult(False, "Hexadecimal")


def detect_caesar(text: str) -> DetectionResult:
    for char in text:
        if char in string.ascii_lowercase or char in string.ascii_uppercase or char == " ":
            continue
        return DetectionResult(False, "Caesar cipher")

    relevant_positions = 0
    best_shift = 0
    for shift in range(1, 26):
        matches = 0
        decrypted_text = ""

        for char in text:
            if char in string.ascii_lowercase:
                decrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            elif char in string.ascii_uppercase:
                decrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            else:
                decrypted_text += char

        for word in decrypted_text.split():
            if word.lower() in COMMON_ENGLISH_WORDS or word.lower() in COMMON_SPANISH_WORDS:
                matches += 1

        if matches > relevant_positions:
            relevant_positions = matches
            best_shift = shift

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
