# HIT137 Group Assignment 2 — Question 1

## Overview

This program reads a text file (`raw_text.txt`), encrypts its contents using a
custom shift cipher, decrypts the result, and verifies that the decryption
matches the original.

---

## Files

| File | Description |
|------|-------------|
| `question1.py` | Main program — encryption, decryption, verification |
| `raw_text.txt` | Original input text (provided with the assignment) |
| `encrypted_text.txt` | Output of the encryption step |
| `decrypted_text.txt` | Output of the decryption step |

---

## Encryption Rules

The cipher takes two positive integer inputs (`shift1`, `shift2`):

| Character range | Rule |
|----------------|------|
| Lowercase **a–m** | Shift **forward** by `shift1 × shift2` positions (mod 26) |
| Lowercase **n–z** | Shift **backward** by `shift1 + shift2` positions (mod 26) |
| Uppercase **A–M** | Shift **backward** by `shift1` positions (mod 26) |
| Uppercase **N–Z** | Shift **forward** by `shift2²` positions (mod 26) |
| All other characters | Unchanged (spaces, punctuation, numbers, newlines) |

---

## How to Run

Make sure `raw_text.txt` is in the **same directory** as `question1.py`, then:

```bash
python3 question1.py
```

The program will:
1. Prompt you for `shift1` and `shift2`
2. Encrypt `raw_text.txt` → `encrypted_text.txt`
3. Decrypt `encrypted_text.txt` → `decrypted_text.txt`
4. Verify the decrypted file matches the original and print the result

### Example run (shift1=6, shift2=14)

```
=======================================================
  HIT137 Assignment 2 — Question 1: File Encryptor
=======================================================

Step 1: Enter shift values
  Enter shift1 (positive integer): 6
  Enter shift2 (positive integer): 14
  Using shift1 = 6,  shift2 = 14

Step 2: Encrypting 'raw_text.txt' …
[✓] Encryption complete  →  'encrypted_text.txt'

Step 3: Decrypting 'encrypted_text.txt' …
[✓] Decryption complete  →  'decrypted_text.txt'

Step 4: Verifying decryption …
[✓] Verification PASSED — decrypted text matches the original exactly.

All steps complete.
```

> **Recommended shift values for a perfect round-trip:** `shift1=6, shift2=14`
> or `shift1=10, shift2=18` or `shift1=14, shift2=6`.

---

## Requirements

- Python 3.6 or higher
- No external libraries required (standard library only)
