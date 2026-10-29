"""
Menu Module
Implements interactive command-line interface, user input handling,
validation loops, and sub-menus for the Personal Finance Manager.
"""

from typing import List
from expense import Expense
import file_manager
import reports
import utils


def print_banner() -> None:
    """Prints the application header banner."""
    print("=" * 46)
    print("           PERSONAL FINANCE MANAGER           ")
    print("=" * 46)


def display_menu() -> None:
    """Displays the main menu choices."""
    print("\nMAIN MENU:")
    print(" 1. Add New Expense")
    print(" 2. View All Expenses")
    print(" 3. View Category-wise Summary")
    print(" 4. Generate Monthly Report")
    print(" 5. Search Expenses")
    print(" 6. Backup & Restore Data")
    print(" 7. Export Report to File")
    print(" 8. Delete an Expense")
    print(" 9. Exit")
    print("-" * 46)


def prompt_add_expense(expenses: List[Expense]) -> None:
    """
    Handles interactive expense creation with validation.
    User can type 'c' or 'cancel' at any prompt to abort.
    """
    print("\n" + "=" * 46)
    print("                ADD NEW EXPENSE               ")
    print("=" * 46)
    print("(Tip: Type 'cancel' at any prompt to abort)\n")

    # 1. Amount
    amount = 0.0
    while True:
        try:
            amt_input = input("Enter amount: ").strip()
            if amt_input.lower() in ("c", "cancel"):
                print("❌ Operation cancelled.")
                return
            valid, val, err = utils.validate_amount(amt_input)
            if valid:
                amount = val
                break
            print(f"⚠️  {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Operation cancelled.")
            return

    # 2. Category
    category = ""
    cat_prompt = (
        "Enter category ("
        + "/".join(utils.DEFAULT_CATEGORIES[:5])
        + "/Other or custom): "
    )
    while True:
        try:
            cat_input = input(cat_prompt).strip()
            if cat_input.lower() in ("c", "cancel"):
                print("❌ Operation cancelled.")
                return
            valid, val, err = utils.validate_category(cat_input)
            if valid:
                category = val
                break
            print(f"⚠️  {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Operation cancelled.")
            return

    # 3. Date
    date_str = ""
    while True:
        try:
            date_input = input("Enter date (YYYY-MM-DD) [Leave blank for today]: ").strip()
            if date_input.lower() in ("c", "cancel"):
                print("❌ Operation cancelled.")
                return
            valid, val, err = utils.validate_date(date_input, allow_blank_for_today=True)
            if valid:
                date_str = val
                break
            print(f"⚠️  {err}")
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Operation cancelled.")
            return

    # 4. Description
    description = ""
    while True:
        try:
            desc_input = input("Enter description: ").strip()
            if desc_input.lower() in ("c", "cancel"):
                print("❌ Operation cancelled.")
                return
            if not desc_input:
                print("⚠️  Description cannot be empty.")
                continue
            description = desc_input
            break
        except (KeyboardInterrupt, EOFError):
            print("\n❌ Operation cancelled.")
            return

    # Create and persist expense
    new_expense = Expense(amount=amount, category=category, date=date_str, description=description)
    expenses.append(new_expense)

    # Persist to CSV
    success = file_manager.append_expense(new_expense)
    if success:
        print("\n✅ Expense added successfully!")
        print(f"   Summary: {new_expense}")
    else:
        print("\n⚠️ Expense added in memory but failed to write to CSV storage.")


def prompt_view_all_expenses(expenses: List[Expense]) -> None:
    """Displays all expenses in a formatted table."""
    reports.display_expenses_table(expenses, title="ALL RECORDED EXPENSES")


def prompt_category_summary(expenses: List[Expense]) -> None:
    """Displays category breakdown with visual charts."""
    reports.display_category_summary(expenses)


def prompt_monthly_report(expenses: List[Expense]) -> None:
    """Displays monthly summary report."""
    reports.display_monthly_report(expenses)


def prompt_search_expenses(expenses: List[Expense]) -> None:
    """Sub-menu to search and filter expenses."""
    print("\n" + "=" * 46)
    print("                SEARCH EXPENSES               ")
    print("=" * 46)
    print("Filter by:")
    print(" 1. Keyword (Description / Category)")
    print(" 2. Category only")
    print(" 3. Date Range (YYYY-MM-DD)")
    print(" 4. Amount Range (Min - Max)")
    print(" 5. Return to Main Menu")

    choice = input("\nEnter search option (1-5): ").strip()
    if choice == "1":
        kw = input("Enter search keyword: ").strip()
        results = reports.filter_expenses(expenses, keyword=kw)
        reports.display_expenses_table(results, title=f"SEARCH RESULTS: '{kw}'")
    elif choice == "2":
        cat = input("Enter category name: ").strip()
        results = reports.filter_expenses(expenses, category=cat)
        reports.display_expenses_table(results, title=f"CATEGORY: '{cat}'")
    elif choice == "3":
        start_d = input("Enter start date (YYYY-MM-DD) [or blank]: ").strip() or None
        end_d = input("Enter end date (YYYY-MM-DD) [or blank]: ").strip() or None
        results = reports.filter_expenses(expenses, start_date=start_d, end_date=end_d)
        reports.display_expenses_table(results, title=f"DATE RANGE: {start_d or 'Earliest'} to {end_d or 'Latest'}")
    elif choice == "4":
        min_a_str = input("Enter minimum amount [or blank]: ").strip()
        max_a_str = input("Enter maximum amount [or blank]: ").strip()
        min_a = float(min_a_str) if min_a_str and utils.validate_amount(min_a_str)[0] else None
        max_a = float(max_a_str) if max_a_str and utils.validate_amount(max_a_str)[0] else None
        results = reports.filter_expenses(expenses, min_amount=min_a, max_amount=max_a)
        reports.display_expenses_table(results, title="AMOUNT RANGE RESULTS")
    elif choice == "5":
        return
    else:
        print("⚠️ Invalid search option.")


def prompt_backup_restore(expenses: List[Expense]) -> None:
    """Sub-menu for backup and restore management."""
    print("\n" + "=" * 46)
    print("            DATA BACKUP & RESTORE             ")
    print("=" * 46)
    print(" 1. Create New Backup")
    print(" 2. View Available Backups")
    print(" 3. Restore Data from Backup")
    print(" 4. Return to Main Menu")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == "1":
        success, info = file_manager.create_backup()
        if success:
            print(f"\n✅ Backup created successfully!")
            print(f"   Saved at: {info}")
        else:
            print(f"\n❌ Backup creation failed: {info}")

    elif choice == "2":
        backups = file_manager.list_backups()
        if not backups:
            print("\nℹ️ No backups found.")
        else:
            print("\nAvailable Backups:")
            print(f"{'#':<4} {'Filename':<35} {'Size (bytes)':<14} {'Created Time'}")
            print("-" * 75)
            for idx, (b_name, _, b_size, b_time) in enumerate(backups, start=1):
                print(f"{idx:<4} {b_name:<35} {b_size:<14} {b_time}")

    elif choice == "3":
        backups = file_manager.list_backups()
        if not backups:
            print("\nℹ️ No backups available to restore from.")
            return

        print("\nSelect a backup to restore:")
        for idx, (b_name, _, _, b_time) in enumerate(backups, start=1):
            print(f" {idx}. {b_name} ({b_time})")

        sel = input(f"\nEnter backup number (1-{len(backups)}) or 'c' to cancel: ").strip()
        if sel.lower() in ("c", "cancel"):
            print("❌ Restore cancelled.")
            return

        if sel.isdigit() and 1 <= int(sel) <= len(backups):
            selected_backup = backups[int(sel) - 1]
            confirm = input(f"⚠️ Are you sure you want to restore '{selected_backup[0]}'? Current data will be safely archived first (y/n): ").strip().lower()
            if confirm == "y":
                success, msg = file_manager.restore_backup(selected_backup[1])
                if success:
                    # Reload memory list
                    reloaded = file_manager.load_expenses()
                    expenses.clear()
                    expenses.extend(reloaded)
                    print(f"\n✅ {msg} Reloaded {len(expenses)} records into active memory.")
                else:
                    print(f"\n❌ Restore error: {msg}")
            else:
                print("❌ Restore cancelled.")
        else:
            print("⚠️ Invalid selection.")

    elif choice == "4":
        return
    else:
        print("⚠️ Invalid choice.")


def prompt_export_report(expenses: List[Expense]) -> None:
    """Exports full financial report to a text file."""
    if not expenses:
        print("\n⚠️ No expense records to export.")
        return

    out_file = reports.export_report_to_file(expenses)
    print("\n✅ Report exported successfully!")
    print(f"   File saved at: {out_file}")


def prompt_delete_expense(expenses: List[Expense]) -> None:
    """Allows user to select and remove an expense record."""
    if not expenses:
        print("\n⚠️ No expense records to delete.")
        return

    reports.display_expenses_table(expenses, title="SELECT EXPENSE TO DELETE")
    # Sort matching the table display (date descending)
    sorted_expenses = sorted(expenses, key=lambda x: x.date, reverse=True)

    choice = input(f"\nEnter item number (1-{len(sorted_expenses)}) to delete or 'c' to cancel: ").strip()
    if choice.lower() in ("c", "cancel"):
        print("❌ Deletion cancelled.")
        return

    if choice.isdigit() and 1 <= int(choice) <= len(sorted_expenses):
        target = sorted_expenses[int(choice) - 1]
        confirm = input(f"Are you sure you want to delete '{target}'? (y/n): ").strip().lower()
        if confirm == "y":
            expenses.remove(target)
            file_manager.save_expenses(expenses)
            print("✅ Expense deleted successfully and file updated.")
        else:
            print("❌ Deletion cancelled.")
    else:
        print("⚠️ Invalid item number.")
