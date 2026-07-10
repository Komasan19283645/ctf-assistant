from __future__ import annotations

from dataclasses import dataclass
from hashlib import md5, sha1, sha256
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class HashCrackResult:
    matched: bool
    label: str
    password: str = ""
    algorithm: str = ""
    details: str = ""


class PasswordCracker:
    def __init__(self, wordlist_path: str | Path | None = None) -> None:
        self.wordlist_path = Path(wordlist_path) if wordlist_path is not None else None

    def set_wordlist(self, wordlist_path: str | Path) -> None:
        self.wordlist_path = Path(wordlist_path) if wordlist_path is not None else None

    def iter_candidates(self) -> Iterable[str]:
        with open(self.wordlist_path, "r", encoding="latin-1") as txt:
            for word in txt:
                yield word.strip()

    def crack_hash(self, target_hash, algorythm: str) -> HashCrackResult:
        if algorythm == "md5":
            for word in self.iter_candidates():
                hashed_word = md5(word.encode()).hexdigest()
                if hashed_word == target_hash:
                    return HashCrackResult(True, "MD5 hash", word, "md5")

        if algorythm == "sha1":
            for word in self.iter_candidates():
                hashed_word = sha1(word.encode()).hexdigest()
                if hashed_word == target_hash:
                    return HashCrackResult(True, "SHA-1 hash", word, "sha1")

        if algorythm == "sha256":
            for word in self.iter_candidates():
                hashed_word = sha256(word.encode()).hexdigest()
                if hashed_word == target_hash:
                    return HashCrackResult(True, "SHA-256 hash", word, "sha256")

        return HashCrackResult(False, "Hash", algorithm=algorythm, details="No match found.")
