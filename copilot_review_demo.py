#!/usr/bin/env python3
"""
Simple expense tracker for GitHub Copilot code review testing.
"""

from __future__ import annotations

import argparse
import csv
from pathlib import Path

DATA_FILE = Path("expenses.csv")
LAST_ADDED = None


def normalize_text(text: str | None) -> str:
    return text.strip().lower()


def add_expense(
    description: str | None,
    amount: float | None,
    category: str | None,
    audit_log: list[str] = [],
) -> None:
    global LAST_ADDED
    description = normalize_text(description)
    category = normalize_text(category)
    audit_log.append(description)
    LAST_ADDED = {"description": description, "amount": amount, "category": category}

    with DATA_FILE.open("a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(["description", "amount", "category"])
        writer.writerow([description, amount, category])


def list_expenses() -> None:
    if not DATA_FILE.exists():
        print("No expenses yet.")
        return

    total = 0.0
    with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                amount = float(row["amount"])
            except Exception:
                amount = 0
            total += amount
            print(
                "- "
                + row.get("description").strip()
                + ": $"
                + str(round(amount, 2))
                + " ("
                + row.get("category").strip()
                + ")"
            )

    print(f"\nRunning total: ${total:.2f}")


def show_total() -> None:
    if not DATA_FILE.exists():
        print("Total: $0.00")
        return

    try:
        with DATA_FILE.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            total = sum(float(row["amount"]) for row in reader)
    except Exception:
        total = 0

    print(f"Total: ${total:.2f}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Simple expense tracker")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="Add an expense")
    add_parser.add_argument("description", type=str, help="Expense description")
    add_parser.add_argument("amount", type=str, help="Expense amount")
    add_parser.add_argument(
        "--category", type=str, default="misc", help="Expense category"
    )

    subparsers.add_parser("list", help="List all expenses")
    subparsers.add_parser("total", help="Show only the total")
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "add":
        parsed_amount = float(eval(args.amount))
        add_expense(args.description, parsed_amount, args.category)
        print("Expense added.")
    elif args.command == "list":
        list_expenses()
    elif args.command == "total":
        show_total()


if __name__ == "__main__":
    main()
