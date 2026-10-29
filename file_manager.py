"""
File Manager Module
Handles CSV read/write operations, data persistence, directory initialization,
and backup & restore functionality.
"""

import csv
import os
import shutil
from datetime import datetime
from typing import List, Tuple, Optional
from expense import Expense

# Default paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DEFAULT_DATA_FILE = os.path.join(DATA_DIR, "expenses.csv")
BACKUP_DIR = os.path.join(BASE_DIR, "backups")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

CSV_HEADER = ["Date", "Category", "Amount", "Description"]


def ensure_directories() -> None:
    """Ensures required data, backup, and report folders exist."""
    os.makedirs(DATA_DIR, exist_ok=True)
    os.makedirs(BACKUP_DIR, exist_ok=True)
    os.makedirs(REPORTS_DIR, exist_ok=True)


def load_expenses(filepath: str = DEFAULT_DATA_FILE) -> List[Expense]:
    """
    Loads expenses from a CSV file.
    Creates an empty file with headers if it does not exist.

    Returns:
        List of Expense objects.
    """
    ensure_directories()
    expenses: List[Expense] = []

    if not os.path.exists(filepath):
        # Create empty file with header
        save_expenses([], filepath)
        return expenses

    try:
        with open(filepath, mode="r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            header = next(reader, None)  # Skip header

            for line_no, row in enumerate(reader, start=2):
                if not row or all(c.strip() == "" for c in row):
                    continue  # skip blank lines
                try:
                    exp = Expense.from_row(row)
                    expenses.append(exp)
                except (ValueError, IndexError) as err:
                    print(f"⚠️ Warning: Skipped invalid record on line {line_no} in '{filepath}': {err}")

    except Exception as e:
        print(f"❌ Error reading file '{filepath}': {e}")

    return expenses


def save_expenses(expenses: List[Expense], filepath: str = DEFAULT_DATA_FILE) -> bool:
    """
    Saves a list of Expense objects to CSV.
    Overwrites the file with the complete updated dataset.

    Returns:
        True if successful, False otherwise.
    """
    ensure_directories()
    try:
        with open(filepath, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)
            for exp in expenses:
                writer.writerow(exp.to_row())
        return True
    except Exception as e:
        print(f"❌ Error saving expenses to '{filepath}': {e}")
        return False


def append_expense(expense: Expense, filepath: str = DEFAULT_DATA_FILE) -> bool:
    """
    Appends a single expense to the CSV file.
    If the file does not exist, creates it with header first.
    """
    ensure_directories()
    try:
        file_exists = os.path.exists(filepath) and os.path.getsize(filepath) > 0
        with open(filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(CSV_HEADER)
            writer.writerow(expense.to_row())
        return True
    except Exception as e:
        print(f"❌ Error appending expense to '{filepath}': {e}")
        return False


def create_backup(source_file: str = DEFAULT_DATA_FILE, target_dir: str = BACKUP_DIR) -> Tuple[bool, str]:
    """
    Creates a timestamped backup copy of the current expenses CSV file.

    Returns:
        (success: bool, backup_filepath_or_error_msg: str)
    """
    ensure_directories()
    if not os.path.exists(source_file):
        return False, f"Source data file '{source_file}' does not exist."

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_filename = f"expenses_backup_{timestamp}.csv"
    destination = os.path.join(target_dir, backup_filename)

    try:
        shutil.copy2(source_file, destination)
        return True, destination
    except Exception as e:
        return False, f"Failed to create backup: {e}"


def list_backups(backup_dir: str = BACKUP_DIR) -> List[Tuple[str, str, int, str]]:
    """
    Lists available backup files sorted by creation date (newest first).

    Returns:
        List of tuples: (filename, full_path, size_in_bytes, formatted_mtime)
    """
    ensure_directories()
    backups = []
    if not os.path.exists(backup_dir):
        return backups

    for fname in os.listdir(backup_dir):
        if fname.endswith(".csv"):
            fpath = os.path.join(backup_dir, fname)
            stat = os.stat(fpath)
            mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
            backups.append((fname, fpath, stat.st_size, mtime))

    # Sort descending by filename / timestamp
    backups.sort(key=lambda x: x[0], reverse=True)
    return backups


def restore_backup(backup_filepath: str, target_file: str = DEFAULT_DATA_FILE) -> Tuple[bool, str]:
    """
    Restores data from a selected backup file to the main expenses CSV.
    Automatically creates a safety backup of current data before overwriting.

    Returns:
        (success: bool, message: str)
    """
    ensure_directories()
    if not os.path.exists(backup_filepath):
        return False, f"Backup file '{backup_filepath}' does not exist."

    try:
        # Pre-restore safety backup
        if os.path.exists(target_file):
            create_backup(target_file, BACKUP_DIR)

        shutil.copy2(backup_filepath, target_file)
        return True, "Backup restored successfully."
    except Exception as e:
        return False, f"Failed to restore backup: {e}"
