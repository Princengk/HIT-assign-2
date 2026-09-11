# HIT137 Assignment 2

This repository contains the group work for HIT137 Assignment 2.

## Files

- `cipher.py` - Question 1: encrypts and decrypts `raw_text.txt` using a custom substitution cipher, then verifies the round trip.
- `evaluator.py` - Question 2: recursive descent parser and evaluator for mathematical expressions, reading from `input.txt` and writing results to `output.txt`.
- `test_evaluator.py` - edge-case test suite covering unary negation, exponent associativity, implicit multiplication, division/modulo by zero, and malformed numbers.
- `raw_text.txt` - sample input text for the cipher program.
- `input.txt` - sample expressions for the evaluator.
- `github_link.txt` - link to this repository.

## How to run

# Question 1 - Cipher

```
python cipher.py
```

Prompts for `shift1` and `shift2`, then:
1. Encrypts `raw_text.txt` -> `encrypted_text.txt`
2. Decrypts `encrypted_text.txt` -> `decrypted_text.txt`
3. Verifies `decrypted_text.txt` matches `raw_text.txt`

# Question 2 - Expression evaluator

```
python evaluator.py input.txt
```

Reads expressions from `input.txt` (one per line) and writes a four-line block (`Input`, `Tree`, `Tokens`, `Result`) per expression to `output.txt` in the same folder.

To run the edge-case tests:

```
python test_evaluator.py
```

## Requirements

Python 3, no external packages required.
