"""
Expense Module
Defines the Expense class representing individual financial transactions.
"""

from datetime import datetime
from typing import Dict, Any, List


class Expense:
    """
    Represents a single expense transaction.

    Attributes:
        amount (float): The monetary value of the expense.
        category (str): The category the expense belongs to.
        date (str): The date of the expense in 'YYYY-MM-DD' format.
        description (str): A brief description of the expense.
    """

    def __init__(self, amount: float, category: str, date: str, description: str):
        self.amount = round(float(amount), 2)
        self.category = category.strip().title()
        self.date = date.strip()
        self.description = description.strip()

    @property
    def parsed_date(self) -> datetime:
        """Parses the date string into a datetime object for sorting and filtering."""
        try:
            return datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            return datetime.min

    @property
    def month_year(self) -> str:
        """Returns the Year-Month string (YYYY-MM) for monthly grouping."""
        return self.date[:7] if len(self.date) >= 7 else "Unknown"

    def to_row(self) -> List[str]:
        """Converts the expense to a CSV row format."""
        return [self.date, self.category, f"{self.amount:.2f}", self.description]

    @classmethod
    def from_row(cls, row: List[str]) -> "Expense":
        """
        Creates an Expense instance from a CSV row.
        Expected order: [Date, Category, Amount, Description]
        """
        if len(row) < 4:
            raise ValueError(f"Invalid row format. Expected 4 columns, got {len(row)}: {row}")
        date, category, amount_str, description = row[0], row[1], row[2], row[3]
        return cls(amount=float(amount_str), category=category, date=date, description=description)

    def to_dict(self) -> Dict[str, Any]:
        """Converts expense to dictionary representation."""
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "description": self.description,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Expense":
        """Creates an Expense instance from dictionary."""
        return cls(
            amount=float(data["amount"]),
            category=data["category"],
            date=data["date"],
            description=data["description"],
        )

    def __str__(self) -> str:
        """Formatted string representation of the expense."""
        return f"{self.date} | {self.category}: ₹{self.amount:.2f} - {self.description}"

    def __repr__(self) -> str:
        return f"Expense(amount={self.amount}, category='{self.category}', date='{self.date}', description='{self.description}')"
