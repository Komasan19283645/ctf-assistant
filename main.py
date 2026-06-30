import base64
import string

def detect_base64(text):
    try:
        base64.b64decode(text, validate=True)
        return True
    except Exception:
        return False

def detect_hex(text):
    try:
        bytes.fromhex(text)
        return True
    except ValueError:
        return False

def detect_ascii(text):
    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def detect_rot13(text):
    for char in text:
        if char in string.ascii_lowercase or char in string.ascii_uppercase or char == " ":
            continue
        return False
    return True

def detect_morse(text):
    for char in text:
        if char == "." or char == "-" or char == " ":
            continue
        return False
    return True

def datect_binary(text):
    for char in text:
        if char == "0" or char == "1" or char == " ":
            continue
        return False
    return True

if __name__ == "__main__":
    print("=== CTF Assistant Started ===")
    print("Type 'exit' to close the program.\n")

    # Infinite loop to keep prompting for text until you type exit
    while True:
        # input() pauses the program and waits for the user to type and press Enter
        user_text = input("Enter the CTF text: ")

        # Exit condition
        if user_text.lower() == "exit":
            print("Closing the assistant...")
            break
        
        # Skip empty input if you press Enter by accident
        if not user_text.strip():
            continue

        # Run the text through our detectors
        if detect_base64(user_text):
            print("[+] Result: The text appears to be Base64.")
        elif detect_hex(user_text):
            print("[+] Result: The text appears to be Hexadecimal.")
        elif detect_rot13(user_text):
            print("[+] Result: The text appears to be ROT13.")
        elif detect_morse(user_text):
            print("[+] Result: The text appears to be Morse code.")
        else:
            print("[-] Result: Unknown format.")
            
        print("-" * 40)  # Visual separator for the next attempt
