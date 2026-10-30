"""
Bank Transaction Validator
Python 3 project.

Run:
    python bank_transaction_validator.py
    python bank_transaction_validator.py transactions.txt

Input format: one transaction per line, Type,Amount
Supported types: Deposit, Withdraw
Opening balance: 10000
"""

from pathlib import Path
import sys

OPENING_BALANCE = 10000
MAX_TRANSACTION_AMOUNT = 100000
VALID_TYPES = {"deposit", "withdraw"}


def validate_transaction(transaction_line, balance):
    """Validate one transaction line.

    Returns (is_valid, reason, updated_balance, normalized_transaction).
    Invalid transactions never change the balance.
    """
    parts = transaction_line.strip().split(",")

    if len(parts) != 2:
        return False, "expected format Type,Amount.", balance, None

    transaction_type = parts[0].strip()
    amount_text = parts[1].strip()

    if transaction_type.lower() not in VALID_TYPES:
        return False, f"unknown type '{transaction_type}'.", balance, None

    try:
        amount = float(amount_text)
    except ValueError:
        return False, f"amount '{amount_text}' is not a number.", balance, None

    if not amount_text or not amount_text.strip():
        return False, "amount must be a number.", balance, None

    if amount <= 0:
        return False, "amount must be positive.", balance, None

    if amount > MAX_TRANSACTION_AMOUNT:
        return False, f"exceeds limit of {MAX_TRANSACTION_AMOUNT}.", balance, None

    # Currency transactions are represented as whole numbers in this project.
    if not amount.is_integer():
        return False, "amount must be a whole number.", balance, None

    amount = int(amount)
    normalized_type = transaction_type.strip().capitalize()

    if normalized_type.lower() == "withdraw" and amount > balance:
        return False, "insufficient balance.", balance, None

    if normalized_type.lower() == "deposit":
        new_balance = balance + amount
    else:
        new_balance = balance - amount

    normalized_transaction = f"{normalized_type},{amount}"
    return True, "valid", new_balance, normalized_transaction


def process_transactions(input_file, output_file="valid_transactions.txt"):
    """Read, validate, report, and save valid transactions."""
    balance = OPENING_BALANCE
    valid_count = 0
    invalid_count = 0
    valid_transactions = []

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Error: input file '{input_file}' was not found.")
        print("Create the file or provide its path as a command-line argument.")
        return 1
    except OSError as error:
        print(f"Error reading '{input_file}': {error}")
        return 1

    print(f"Opening balance: {balance}")
    print("-" * 55)

    for line_number, line in enumerate(lines, start=1):
        if not line.strip():
            continue

        is_valid, reason, new_balance, normalized = validate_transaction(line, balance)

        if is_valid:
            balance = new_balance
            valid_count += 1
            valid_transactions.append(normalized)
            print(f"Line {line_number}: Valid | Balance: {balance}")
        else:
            invalid_count += 1
            print(f"Line {line_number}: Invalid - {reason}")

    try:
        with open(output_file, "w", encoding="utf-8") as file:
            for transaction in valid_transactions:
                file.write(transaction + "\n")
    except OSError as error:
        print(f"Error saving valid transactions to '{output_file}': {error}")
        return 1

    print("-" * 55)
    print(f"Valid: {valid_count} | Invalid: {invalid_count}")
    print(f"Final balance: {balance}")
    print(f"Valid transactions saved to: {output_file}")
    return 0


def main():
    input_file = sys.argv[1] if len(sys.argv) > 1 else "transactions.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "valid_transactions.txt"
    raise SystemExit(process_transactions(input_file, output_file))


if __name__ == "__main__":
    main()
