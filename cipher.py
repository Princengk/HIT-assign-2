"""
HIT137 Assignment 2 - Question 1
Custom substitution cipher.

DESIGN NOTE (read this before you submit):
The brief says letters "shift forward/backward" but never says what happens
when a shift pushes a letter past the end of its range. For the cipher to be
DECRYPTABLE, each letter must stay inside the same group it started in
(lowercase-first-half, lowercase-second-half, uppercase-first-half,
uppercase-second-half, digit) after encryption. Otherwise decrypt_file()
would not know which rule to reverse.

So every shift here wraps around WITHIN its own group, not around the full
26-letter alphabet:
    a-n (14 letters)   -> wraps mod 14
    o-z (12 letters)   -> wraps mod 12
    A-M (13 letters)   -> wraps mod 13
    N-Z (13 letters)   -> wraps mod 13
    0-9 (10 digits)    -> wraps mod 10

This is a reasonable, defensible assumption but it IS an assumption. If your
sample_output.txt (from assignment2.zip, which wasn't available to me when I
built this) shows different wrapping behaviour, tell me and I'll adjust the
shift_in_range() calls below - the rest of the program doesn't need to change.
"""

LOWER_FIRST = "abcdefghijklmn"      # a-n, 14 letters
LOWER_SECOND = "opqrstuvwxyz"       # o-z, 12 letters
UPPER_FIRST = "ABCDEFGHIJKLM"       # A-M, 13 letters
UPPER_SECOND = "NOPQRSTUVWXYZ"      # N-Z, 13 letters
DIGITS = "0123456789"               # 0-9, 10 digits


def shift_in_range(ch: str, group: str, amount: int) -> str:
    """Shift ch by `amount` positions within `group`, wrapping around."""
    idx = group.index(ch)
    new_idx = (idx + amount) % len(group)
    return group[new_idx]


def encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    if ch in LOWER_FIRST:
        return shift_in_range(ch, LOWER_FIRST, shift1 * shift2)
    if ch in LOWER_SECOND:
        return shift_in_range(ch, LOWER_SECOND, -(shift1 + shift2))
    if ch in UPPER_FIRST:
        return shift_in_range(ch, UPPER_FIRST, -shift1)
    if ch in UPPER_SECOND:
        return shift_in_range(ch, UPPER_SECOND, shift2 ** 2)
    if ch in DIGITS:
        return shift_in_range(ch, DIGITS, shift1 - shift2)
    return ch  # spaces, tabs, newlines, punctuation, symbols


def decrypt_char(ch: str, shift1: int, shift2: int) -> str:
    if ch in LOWER_FIRST:
        return shift_in_range(ch, LOWER_FIRST, -(shift1 * shift2))
    if ch in LOWER_SECOND:
        return shift_in_range(ch, LOWER_SECOND, shift1 + shift2)
    if ch in UPPER_FIRST:
        return shift_in_range(ch, UPPER_FIRST, shift1)
    if ch in UPPER_SECOND:
        return shift_in_range(ch, UPPER_SECOND, -(shift2 ** 2))
    if ch in DIGITS:
        return shift_in_range(ch, DIGITS, -(shift1 - shift2))
    return ch


def encrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads from input_path (raw_text.txt) and writes encrypted content to output_path."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    encrypted = "".join(encrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(encrypted)


def decrypt_file(shift1: int, shift2: int, input_path: str, output_path: str) -> None:
    """Reads from input_path (encrypted_text.txt) and writes decrypted content to output_path."""
    with open(input_path, "r", encoding="utf-8") as f:
        text = f.read()
    decrypted = "".join(decrypt_char(ch, shift1, shift2) for ch in text)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(decrypted)


def verify_files(original_path: str, decrypted_path: str) -> bool:
    """Compares original_path (raw_text.txt) with decrypted_path (decrypted_text.txt)."""
    with open(original_path, "r", encoding="utf-8") as f:
        original = f.read()
    with open(decrypted_path, "r", encoding="utf-8") as f:
        decrypted = f.read()
    success = original == decrypted
    if success:
        print("Verification successful: decrypted text matches the original.")
    else:
        print("Verification FAILED: decrypted text does not match the original.")
    return success


def main():
    shift1 = int(input("Enter shift1 (non-negative integer): "))
    shift2 = int(input("Enter shift2 (non-negative integer): "))
    if shift1 < 0 or shift2 < 0:
        raise ValueError("shift1 and shift2 must be non-negative integers")

    raw_path = "raw_text.txt"
    encrypted_path = "encrypted_text.txt"
    decrypted_path = "decrypted_text.txt"

    encrypt_file(shift1, shift2, raw_path, encrypted_path)
    print(f"Encrypted '{raw_path}' -> '{encrypted_path}'")

    decrypt_file(shift1, shift2, encrypted_path, decrypted_path)
    print(f"Decrypted '{encrypted_path}' -> '{decrypted_path}'")

    verify_files(raw_path, decrypted_path)


if __name__ == "__main__":
    main()
