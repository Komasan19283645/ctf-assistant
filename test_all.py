from detectors import detect_base64, detect_hex, detect_caesar, detect_binary, identify_hash
from password_cracking import PasswordCracker, HashCrackResult

# Test detectors
print("=== DETECTOR TESTS ===\n")

# Test base64
print("1. Base64 (valid):")
result = detect_base64("SGVsbG8gV29ybGQh")
print(f"   {result}\n")

# Test hex
print("2. Hexadecimal:")
result = detect_hex("1234abcd")
print(f"   {result}\n")

# Test Caesar cipher
print("3. Caesar cipher (plaintext - should be False):")
result = detect_caesar("KAT IS AWESOME")
print(f"   {result}\n")

print("4. Caesar cipher (rotated):")
result = detect_caesar("LBU JT BXFTPNF")  # "KAT IS AWESOME" rotated by 1
print(f"   {result}\n")

# Test binary
print("5. Binary (valid UTF-8):")
result = detect_binary("01001000 01100101 01101100 01101100 01101111")  # "Hello"
print(f"   {result}\n")

# Test hash
print("6. MD5 Hash:")
result = identify_hash("5f4dcc3b5aa765d61d8327deb882cf99")
print(f"   {result}\n")

print("=== PASSWORD CRACKING TEST ===\n")

# Test PasswordCracker initialization
print("7. PasswordCracker initialization (no wordlist):")
pc = PasswordCracker()
print(f"   Wordlist path: {pc.wordlist_path}\n")

# Test mutate function
print("8. Mutate function (first 10 variants of 'test'):")
pc = PasswordCracker()
variants = list(pc.mutate("test"))[:10]
for v in variants:
    print(f"   - {v}")
print()

print("✅ All basic function tests completed!")
