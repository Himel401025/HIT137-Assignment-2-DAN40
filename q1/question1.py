"""
HIT137 Group Assignment 2 — Question 1
=======================================
Encrypt, decrypt, and verify a text file using a custom shift cipher.

Encryption Rules (shift1, shift2 are positive integers supplied by the user):
  Lowercase a–m  : shift forward  by (shift1 * shift2) positions  (mod 13)
  Lowercase n–z  : shift backward by (shift1 + shift2) positions  (mod 13)
  Uppercase A–M  : shift backward by  shift1            positions  (mod 13)
  Uppercase N–Z  : shift forward  by  shift2²           positions  (mod 13)
  All other chars: unchanged (spaces, numbers, punctuation, newlines …)

Each half of the alphabet (a–m / n–z and A–M / N–Z) is kept separate so
the cipher is bijective for ANY choice of shift1 and shift2 — meaning
decryption always perfectly reconstructs the original text.
"""

import os

def _encrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Encrypt a single character according to the cipher rules.

    Each half of the alphabet (13 letters) is treated as its own cycle,
    so a–m always encrypts to a–m and n–z always encrypts to n–z (and
    likewise for uppercase). This guarantees the cipher is bijective for
    every possible shift1 / shift2 pair.

    Args:
        ch:     The character to encrypt.
        shift1: First shift value (positive integer).
        shift2: Second shift value (positive integer).

    Returns:
        The encrypted character (unchanged if not alphabetic).
    """
    if ch.islower():
        i = ord(ch) - ord('a')
        if i <= 12:                                     # a–m: shift forward
            enc_i = (i + shift1 * shift2) % 13
        else:                                           # n–z: shift backward
            enc_i = 13 + (i - 13 - (shift1 + shift2)) % 13
        return chr(ord('a') + enc_i)

    elif ch.isupper():
        i = ord(ch) - ord('A')
        if i <= 12:                                     # A–M: shift backward
            enc_i = (i - shift1) % 13
        else:                                           # N–Z: shift forward by shift2²
            enc_i = 13 + (i - 13 + shift2 ** 2) % 13
        return chr(ord('A') + enc_i)

    else:
        return ch                                       # spaces, punctuation, etc.


def _decrypt_char(ch: str, shift1: int, shift2: int) -> str:
    """
    Decrypt a single character by reversing the encryption rules.

    Because each half of the alphabet maps only to itself, we can
    determine which rule was used simply by looking at the encrypted
    character's position.

    Args:
        ch:     The character to decrypt.
        shift1: First shift value used during encryption.
        shift2: Second shift value used during encryption.

    Returns:
        The decrypted character (unchanged if not alphabetic).
    """
    if ch.islower():
        i = ord(ch) - ord('a')
        if i <= 12:                                     # came from a–m
            orig_i = (i - shift1 * shift2) % 13
        else:                                           # came from n–z
            orig_i = 13 + (i - 13 + (shift1 + shift2)) % 13
        return chr(ord('a') + orig_i)

    elif ch.isupper():
        i = ord(ch) - ord('A')
        if i <= 12:                                     # came from A–M
            orig_i = (i + shift1) % 13
        else:                                           # came from N–Z
            orig_i = 13 + (i - 13 - shift2 ** 2) % 13
        return chr(ord('A') + orig_i)

    else:
        return ch


# ---------------------------------------------------------------------------
# Main functions
# ---------------------------------------------------------------------------

def encrypt_file(input_path: str, output_path: str,
                 shift1: int, shift2: int) -> None:
    """
    Read plaintext from *input_path*, encrypt it, and write to *output_path*.

    Args:
        input_path:  Path to "raw_text.txt".
        output_path: Path to "encrypted_text.txt" (created / overwritten).
        shift1:      First shift value (positive integer).
        shift2:      Second shift value (positive integer).
    """
    with open(input_path, 'r', encoding='utf-8') as fh:
        plaintext = fh.read()

    encrypted = ''.join(_encrypt_char(ch, shift1, shift2) for ch in plaintext)

    with open(output_path, 'w', encoding='utf-8') as fh:
        fh.write(encrypted)

    print(f"[✓] Encryption complete  →  '{output_path}'")


def decrypt_file(input_path: str, output_path: str,
                 shift1: int, shift2: int) -> None:
    """
    Read ciphertext from *input_path*, decrypt it, and write to *output_path*.

    Args:
        input_path:  Path to "encrypted_text.txt".
        output_path: Path to "decrypted_text.txt" (created / overwritten).
        shift1:      First shift value used during encryption.
        shift2:      Second shift value used during encryption.
    """
    with open(input_path, 'r', encoding='utf-8') as fh:
        ciphertext = fh.read()

    decrypted = ''.join(_decrypt_char(ch, shift1, shift2) for ch in ciphertext)

    with open(output_path, 'w', encoding='utf-8') as fh:
        fh.write(decrypted)

    print(f"[✓] Decryption complete  →  '{output_path}'")


def verify_decryption(original_path: str, decrypted_path: str) -> bool:
    """
    Compare *original_path* with *decrypted_path* and print the result.

    Args:
        original_path:  Path to the original "raw_text.txt".
        decrypted_path: Path to "decrypted_text.txt".

    Returns:
        True if the files are identical, False otherwise.
    """
    with open(original_path, 'r', encoding='utf-8') as fh:
        original = fh.read()

    with open(decrypted_path, 'r', encoding='utf-8') as fh:
        decrypted = fh.read()

    if original == decrypted:
        print("[✓] Verification PASSED — decrypted text matches the original exactly.")
        return True

    # Report the first mismatch to help diagnose issues
    for i, (orig_ch, dec_ch) in enumerate(zip(original, decrypted)):
        if orig_ch != dec_ch:
            print(
                f"[✗] Verification FAILED — first mismatch at position {i}: "
                f"original={repr(orig_ch)}, decrypted={repr(dec_ch)}"
            )
            return False

    # Files matched up to the shorter length but differ in length
    print(
        f"[✗] Verification FAILED — length mismatch "
        f"(original={len(original)} chars, decrypted={len(decrypted)} chars)."
    )
    return False


# ---------------------------------------------------------------------------
# Input helper
# ---------------------------------------------------------------------------

def _get_shift_value(prompt: str) -> int:
    """Prompt the user for a positive integer and keep asking until valid."""
    while True:
        try:
            value = int(input(prompt))
            if value >= 1:
                return value
            print("  Please enter a positive integer (≥ 1).")
        except ValueError:
            print("  Invalid input — please enter a whole number.")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    """Run the full encrypt → decrypt → verify pipeline."""
    print("=" * 55)
    print("  HIT137 Assignment 2 — Question 1: File Encryptor")
    print("=" * 55)

    # Resolve file paths relative to this script's location so the program
    # works correctly regardless of the current working directory.
    base_dir       = os.path.dirname(os.path.abspath(__file__))
    raw_file       = os.path.join(base_dir, "raw_text.txt")
    encrypted_file = os.path.join(base_dir, "encrypted_text.txt")
    decrypted_file = os.path.join(base_dir, "decrypted_text.txt")

    # --- Step 1: get shift values ---
    print("\nStep 1: Enter shift values")
    shift1 = _get_shift_value("  Enter shift1 (positive integer): ")
    shift2 = _get_shift_value("  Enter shift2 (positive integer): ")
    print(f"  Using shift1 = {shift1},  shift2 = {shift2}")

    # --- Step 2: encrypt ---
    print("\nStep 2: Encrypting 'raw_text.txt' …")
    encrypt_file(raw_file, encrypted_file, shift1, shift2)

    # --- Step 3: decrypt ---
    print("\nStep 3: Decrypting 'encrypted_text.txt' …")
    decrypt_file(encrypted_file, decrypted_file, shift1, shift2)

    # --- Step 4: verify ---
    print("\nStep 4: Verifying decryption …")
    verify_decryption(raw_file, decrypted_file)

    print("\nAll steps complete.")


if __name__ == "__main__":
    main()
