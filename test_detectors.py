from detectors import detect_binary, detect_caesar

# Test binary
binary_text = "11001000 01100101 01101100 01101100 01101111"
result = detect_binary(binary_text)
print(f"Binary test: {result}")

# Test caesar
caesar_text = "KAT IS AWESOME"
result = detect_caesar(caesar_text)
print(f"Caesar test: {result}")
