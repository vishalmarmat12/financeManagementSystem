"""
Utilities Module
Provides validation, formatting, and helper functions for the Personal Finance Manager.
"""

import os
from datetime import datetime
from typing import Tuple, List

# Predefined standard expense categories
DEFAULT_CATEGORIES: List[str] = [
    "Food",
    "Transport",
    "Entertainment",
    "Shopping",
    "Utilities",
    "Healthcare",
    "Education",
    "Other"
]

CURRENCY_SYMBOL = "₹"


def clear_screen() -> None:
    """Clears the console screen cross-platform."""
    os.system("cls" if os.name == "nt" else "clear")


def press_enter_to_continue() -> None:
    """Prompts the user to press Enter to continue."""
    try:
        input("\nPress Enter to continue...")
    except (KeyboardInterrupt, EOFError):
        pass


def validate_amount(amount_input: str) -> Tuple[bool, float, str]:
    """
    Validates expense amount.
    Must be a positive float greater than 0.

    Returns:
        (is_valid, parsed_amount, error_message)
    """
    cleaned = amount_input.strip()
    if not cleaned:
        return False, 0.0, "Amount cannot be empty."

    # Remove possible currency symbols or commas
    cleaned = cleaned.replace("₹", "").replace("$", "").replace(",", "")

    try:
        amount = float(cleaned)
        if amount <= 0:
            return False, 0.0, "Amount must be strictly greater than 0."
        if amount > 100_000_000:
            return False, 0.0, "Amount is unrealistically large (max: 100,000,000)."
        return True, round(amount, 2), ""
    except ValueError:
        return False, 0.0, f"Invalid number format: '{amount_input}'. Please enter a valid numerical value."


def validate_date(date_input: str, allow_blank_for_today: bool = True) -> Tuple[bool, str, str]:
    """
    Validates date string format (YYYY-MM-DD) and logical validity.
    Optionally allows leaving blank to automatically use today's date.

    Returns:
        (is_valid, formatted_date_str, error_message)
    """
    cleaned = date_input.strip()
    if not cleaned:
        if allow_blank_for_today:
            today_str = datetime.now().strftime("%Y-%m-%d")
            return True, today_str, ""
        return False, "", "Date cannot be empty."

    try:
        parsed = datetime.strptime(cleaned, "%Y-%m-%d")
        # Ensure year is reasonable
        if parsed.year < 2000 or parsed.year > 2100:
            return False, "", "Year must be between 2000 and 2100."
        return True, cleaned, ""
    except ValueError:
        return False, "", f"Invalid date '{date_input}'. Format must be strictly YYYY-MM-DD (e.g. 2024-01-15)."


def validate_category(category_input: str, allowed_categories: List[str] = DEFAULT_CATEGORIES) -> Tuple[bool, str, str]:
    """
    Validates category input. Matches case-insensitively with allowed list,
    or allows user to pick by number or custom category.

    Returns:
        (is_valid, matched_category_name, error_message)
    """
    cleaned = category_input.strip()
    if not cleaned:
        return False, "", "Category cannot be empty."

    # Check if entered as category number (1-index)
    if cleaned.isdigit():
        idx = int(cleaned) - 1
        if 0 <= idx < len(allowed_categories):
            return True, allowed_categories[idx], ""

    # Match case-insensitively with standard categories
    for cat in allowed_categories:
        if cleaned.lower() == cat.lower():
            return True, cat, ""

    # If it's a valid string of reasonable length, allow as custom category
    if len(cleaned) <= 30:
        return True, cleaned.title(), ""

    return False, "", "Category name must not exceed 30 characters."


def format_currency(amount: float, symbol: str = CURRENCY_SYMBOL) -> str:
    """Formats a float as currency with commas (e.g. ₹1,500.00)."""
    return f"{symbol}{amount:,.2f}"


def create_ascii_bar(percentage: float, width: int = 25) -> str:
    """
    Creates an ASCII progress bar for visualizing distributions.
    E.g. [█████████████           ] 52.0%
    """
    percentage = max(0.0, min(100.0, percentage))
    filled_length = int(round(width * (percentage / 100.0)))
    bar = "█" * filled_length + "░" * (width - filled_length)
    return f"[{bar}] {percentage:>5.1f}%"


def truncate_text(text: str, max_length: int) -> str:
    """Truncates text with ellipsis if it exceeds max_length."""
    if len(text) <= max_length:
        return text
    return text[: max_length - 3] + "..."
