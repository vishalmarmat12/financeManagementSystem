"""
Personal Finance Manager
Main Program Entry Point

Authors/Project: Complete Python Personal Finance Manager
"""

import sys
import file_manager
import menu
import utils
from expense import Expense

# Configure UTF-8 streams on Windows to prevent UnicodeEncodeError in cp1252 consoles
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        if sys.stderr and hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        if sys.stdin and hasattr(sys.stdin, "reconfigure"):
            sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def seed_sample_data_if_empty(expenses: list[Expense]) -> None:
    """
    Populates sample data if the file is empty so the user can immediately
    explore reports and features.
    """
    if expenses:
        return

    sample_items = [
        Expense(1500.0, "Food", "2024-01-15", "Grocery shopping at supermarket"),
        Expense(450.0, "Transport", "2024-01-16", "Metro card recharge"),
        Expense(1200.0, "Entertainment", "2024-01-18", "Movie night with friends"),
        Expense(3200.0, "Shopping", "2024-01-20", "Winter jacket purchase"),
        Expense(2100.0, "Utilities", "2024-01-22", "Electricity & water bill"),
        Expense(850.0, "Food", "2024-02-02", "Dinner at Italian restaurant"),
        Expense(1500.0, "Healthcare", "2024-02-10", "Routine health checkup"),
        Expense(600.0, "Transport", "2024-02-14", "Cab fare to airport"),
        Expense(2500.0, "Education", "2024-02-20", "Online Python course subscription"),
    ]

    for item in sample_items:
        expenses.append(item)
    file_manager.save_expenses(expenses)


def main() -> None:
    """Main program execution loop."""
    # Ensure folders and load persisted expenses
    file_manager.ensure_directories()
    expenses = file_manager.load_expenses()

    # Seed sample records if completely blank
    if not expenses:
        seed_sample_data_if_empty(expenses)

    while True:
        try:
            menu.print_banner()
            menu.display_menu()

            choice = input("Enter your choice (1-9): ").strip()

            if choice == "1":
                menu.prompt_add_expense(expenses)
                utils.press_enter_to_continue()

            elif choice == "2":
                menu.prompt_view_all_expenses(expenses)
                utils.press_enter_to_continue()

            elif choice == "3":
                menu.prompt_category_summary(expenses)
                utils.press_enter_to_continue()

            elif choice == "4":
                menu.prompt_monthly_report(expenses)
                utils.press_enter_to_continue()

            elif choice == "5":
                menu.prompt_search_expenses(expenses)
                utils.press_enter_to_continue()

            elif choice == "6":
                menu.prompt_backup_restore(expenses)
                utils.press_enter_to_continue()

            elif choice == "7":
                menu.prompt_export_report(expenses)
                utils.press_enter_to_continue()

            elif choice == "8":
                menu.prompt_delete_expense(expenses)
                utils.press_enter_to_continue()

            elif choice == "9":
                print("\n==========================================")
                print(" Thank you for using Personal Finance Manager!")
                print(" Goodbye & have a great day! 👋")
                print("==========================================\n")
                sys.exit(0)

            else:
                print("⚠️ Invalid choice! Please enter a number between 1 and 9.")
                utils.press_enter_to_continue()

        except KeyboardInterrupt:
            print("\n\nOperation interrupted by user. Returning to main menu...")
            utils.press_enter_to_continue()
        except EOFError:
            print("\nExiting program...")
            break
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
            utils.press_enter_to_continue()


if __name__ == "__main__":
    main()
