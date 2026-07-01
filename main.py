import base64
import string
import re

rotation_position = 0

def detect_base64(text: str) -> bool:
    text = text.strip() # Remove leading/trailing whitespace
    
    # Base64 only uses A-Z, a-z, 0-9, +, /, and = for padding
    if not re.fullmatch(r'[A-Za-z0-9+/]*={0,2}', text):
        return False
    
    # The length must be a multiple of 4
    if len(text) % 4 != 0 or len(text) == 0:
        return False
    
    try:
        # Decode and re-encode to validate the format
        decoded = base64.b64decode(text, validate=True)
        return base64.b64encode(decoded).decode() == text
    except Exception:
        return False

def detect_hex(text) -> bool:
    text = text.strip()  # Remove leading/trailing whitespace

    # Hexadecimal can optionally start with '0x' or '#', followed by hex digits
    if not re.fullmatch(r'^(0x|#)?[0-9a-fA-F]+$', text):
        return False
    
    if text.startswith("0x"):
        text = text[2:]  # Remove the "0x" prefix
    elif text.startswith("#"):
        text = text[1:]  # Remove the leading "#"

    try:
        bytes.fromhex(text, validate=True)  # Validate hex string
        return True
    except ValueError:
        return False

def detect_ascii(text):
    text = text.strip()  # Remove leading/trailing whitespace

    try:
        text.encode('ascii')
        return True
    except UnicodeEncodeError:
        return False

def detect_cesar(text):
    global rotation_position

    common_words_en = [
    "the", "is", "and", "you", "this", "that", "with", "for",
    "are", "was", "have", "hello", "world", "what", "flag",
    "to", "of", "in", "it", "not", "on", "be", "as", "at"
]
    common_words_es = [
    "el", "la", "los", "las", "un", "una", "unos", "unas", "este", "esta", "eso",
    "yo", "tu", "el", "ella", "nosotros", "ellos", "que", "su", "sus", "me", "te", "se",
    "de", "en", "con", "por", "para", "sin", "sobre", "entre", "hasta", "desde",
    "y", "o", "pero", "porque", "si", "no", "como", "cuando", "donde",
    "es", "son", "esta", "estan", "hay", "ser", "estar", "tener", "hacer",
    "puede", "puedes", "quiero", "vamos", "fue", "era",
    "flag", "bandera", "contrasena", "clave", "hola", "mundo", "secreto",
    "mensaje", "texto", "codigo", "encontrar", "buscar"
]

    for char in text:
        if char in string.ascii_lowercase or char in string.ascii_uppercase or char == " ":
            continue
        return False
    
    relevant_positions = 0
    rotation_position = 0
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
            if word.lower() in common_words_en or word.lower() in common_words_es:
                cont += 1
        
        if cont > relevant_positions:
            relevant_positions = cont
            rotation_position = i
            
    if relevant_positions > 1:
        return True
    return False

def detect_morse(text):
    for char in text:
        if char == "." or char == "-" or char == " ":
            continue
        return False
    return True

def detect_binary(text):
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
        if detect_binary(user_text):
            print("[+] Result: The text appears to be Binary.")
        elif detect_morse(user_text):
            print("[+] Result: The text appears to be Morse code.")
        elif detect_hex(user_text):
            print("[+] Result: The text appears to be Hexadecimal.")
        elif detect_base64(user_text):
            print("[+] Result: The text appears to be Base64.")
        elif detect_cesar(user_text):
            print(f"[+] Result: The text appears to be Caesar cipher and is likely rotated {rotation_position} positions.")
        elif detect_ascii(user_text):
            print("[+] Result: The text appears to be ASCII.")
        else:
            print("[-] Result: Unknown format.")

        print("-" * 40)  # Visual separator for the next attempt
        print()  # Print a blank line for better readability
            

