def encrypt_char(ch, shift1, shift2):
    if 'a' <= ch <= 'n':
        shift = shift1 * shift2
        start = ord('a')
        size = 14
    elif 'o' <= ch <= 'z':
        shift = -(shift1 + shift2)
        start = ord('o')
        size = 12
    elif 'A' <= ch <= 'M':
        shift = -shift1
        start = ord('A')
        size = 13
    elif 'N' <= ch <= 'Z':
        shift = shift2 * shift2
        start = ord('N')
        size = 13
    elif ch.isdigit():
        shift = shift1 - shift2
        start = ord('0')
        size = 10
    else:
        return ch

    new_pos = (ord(ch) - start + shift) % size
    return chr(start + new_pos)

def decrypt_char(ch, shift1, shift2):
    if 'a' <= ch <= 'n':
        shift = -(shift1 * shift2)
        start = ord('a')
        size = 14
    elif 'o' <= ch <= 'z':
        shift = shift1 + shift2
        start = ord('o')
        size = 12
    elif 'A' <= ch <= 'M':
        shift = shift1
        start = ord('A')
        size = 13
    elif 'N' <= ch <= 'Z':
        shift = -(shift2 * shift2)
        start = ord('N')
        size = 13
    elif ch.isdigit():
        shift = -(shift1 - shift2)
        start = ord('0')
        size = 10
    else:
        return ch

    new_pos = (ord(ch) - start + shift) % size
    return chr(start + new_pos)

def encrypt_file(shift1, shift2, input_path, output_path):
    infile = open(input_path, "r", encoding="utf-8")
    text = infile.read()
    infile.close()

    result = ""
    for ch in text:
        result += encrypt_char(ch, shift1, shift2)

    outfile = open(output_path, "w", encoding="utf-8")
    outfile.write(result)
    outfile.close()

def decrypt_file(shift1, shift2, input_path, output_path):
    infile = open(input_path, "r", encoding="utf-8")
    text = infile.read()
    infile.close()

    result = ""
    for ch in text:
        result += decrypt_char(ch, shift1, shift2)

    outfile = open(output_path, "w", encoding="utf-8")
    outfile.write(result)
    outfile.close()

def verify_files(original_path, decrypted_path):
    f1 = open(original_path, "r", encoding="utf-8")
    original = f1.read()
    f1.close()

    f2 = open(decrypted_path, "r", encoding="utf-8")
    decrypted = f2.read()
    f2.close()

    if original == decrypted:
        print("Success - decrypted text matches the original.")
        return True
    else:
        print("Failed - decrypted text does NOT match the original.")
        return False

def main():
    shift1 = int(input("Enter shift1: "))
    shift2 = int(input("Enter shift2: "))

    encrypt_file(shift1, shift2, "raw_text.txt", "encrypted_text.txt")
    print("Encrypted raw_text.txt -> encrypted_text.txt")

    decrypt_file(shift1, shift2, "encrypted_text.txt", "decrypted_text.txt")
    print("Decrypted encrypted_text.txt -> decrypted_text.txt")

    verify_files("raw_text.txt", "decrypted_text.txt")

if __name__ == "__main__":
    main()
