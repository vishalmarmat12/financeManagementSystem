# 💰 Python Personal Finance Manager

A comprehensive, object-oriented Personal Finance Management System built with Python, featuring file persistence via CSV, data backup & restore, input validation, interactive command-line interface, and analytics with visual ASCII charts and report generation.

---

## 📁 Project Structure

```text
Developer Arena/
│
├── main.py                   # Main application entry point & orchestration
├── expense.py                # Expense class definition & model logic
├── file_manager.py           # CSV persistence, atomic backup & restore
├── menu.py                   # Interactive CLI menu system & user workflows
├── reports.py                # Analytics, statistical calculations & visual charts
├── utils.py                  # Validation, formatting & terminal utilities
├── test_finance_manager.py   # Complete unit test suite (11 unit tests)
│
├── data/
│   └── expenses.csv          # Persistent CSV dataset (Date, Category, Amount, Description)
├── backups/                  # Automatic and manual timestamped CSV backups
└── reports/                  # Exported detailed summary reports (.txt)
```

---

## 🛠️ Key Technical Features

1. **Object-Oriented Design (`expense.py`)**:
   - `Expense` model with `amount`, `category`, `date`, `description`, and derived properties like `month_year` and `parsed_date`.
   - Bidirectional serialization with CSV rows and dictionary conversions.
   - Formatted string representation (`__str__`): `YYYY-MM-DD | Category: ₹Amount - Description`.

2. **Data Persistence & File Operations (`file_manager.py`)**:
   - Built-in `csv` module integration with safe header management.
   - Automatic directory bootstrap (`data/`, `backups/`, `reports/`).
   - Append-only or batch write operations.
   - **Backup & Restore System**: Generates timestamped snapshots (`expenses_backup_YYYYMMDD_HHMMSS.csv`) and allows interactive restoration with automatic pre-restore safety archiving.

3. **Input Validation & Error Handling (`utils.py`)**:
   - **Amount Validation**: Ensures strictly positive floating-point values, removes currency symbols/commas, and guards against overflow.
   - **Date Validation**: Enforces strict `YYYY-MM-DD` calendar formatting (validates leap years and month boundaries) with optional quick-entry (blank = today's date).
   - **Category Validation**: Allows case-insensitive matching against standard categories or numeric selection, with support for custom category naming.
   - Cross-platform Windows UTF-8 terminal handling to prevent codepage encoding issues.

4. **Analytics & Visual Reporting (`reports.py`)**:
   - Calculations: Total expenditure, average expense, highest/lowest transactions, category shares.
   - **ASCII Visual Distribution Bars**: Terminal progress bars showing category spending percentages.
   - **Monthly Reports**: Chronological breakdown by `YYYY-MM` with percentage contribution.
   - **Multi-criteria Filtering**: Search by keyword, category, date range, or amount range.
   - **File Export**: Generates timestamped `.txt` executive summaries in `reports/`.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.8+ (tested and verified with Python 3.14)

### Running the Application
```bash
python main.py
```

### Running the Test Suite
```bash
python test_finance_manager.py
```

---

## 📋 Interactive CLI Menu

```text
==============================================
           PERSONAL FINANCE MANAGER           
==============================================

MAIN MENU:
 1. Add New Expense
 2. View All Expenses
 3. View Category-wise Summary
 4. Generate Monthly Report
 5. Search Expenses
 6. Backup & Restore Data
 7. Export Report to File
 8. Delete an Expense
 9. Exit
----------------------------------------------
Enter your choice (1-9):
```

---

## 📊 Sample Workflows

### 1. Adding an Expense
```text
==============================================
                ADD NEW EXPENSE               
==============================================
(Tip: Type 'cancel' at any prompt to abort)

Enter amount: 1500
Enter category (Food/Transport/Entertainment/Shopping/Utilities/Other or custom): Food
Enter date (YYYY-MM-DD) [Leave blank for today]: 2024-01-15
Enter description: Grocery shopping

✅ Expense added successfully!
   Summary: 2024-01-15 | Food: ₹1500.00 - Grocery shopping
```

### 2. Category Breakdown & Visual Distribution
```text
================================================================================
                         CATEGORY-WISE EXPENSE SUMMARY                          
================================================================================
Category         Count     Total Amount   Share   Visual Distribution
--------------------------------------------------------------------------------
Food             2            ₹2,350.00   17.5%   [███░░░░░░░░░░░░░░░░░]  17.5%
Shopping         1            ₹3,200.00   23.9%   [█████░░░░░░░░░░░░░░░]  23.9%
Education        1            ₹2,500.00   18.7%   [████░░░░░░░░░░░░░░░░]  18.7%
Utilities        1            ₹2,100.00   15.7%   [███░░░░░░░░░░░░░░░░░]  15.7%
Healthcare       1            ₹1,500.00   11.2%   [██░░░░░░░░░░░░░░░░░░]  11.2%
Entertainment    1            ₹1,200.00    9.0%   [██░░░░░░░░░░░░░░░░░░]   9.0%
Transport        2            ₹1,050.00    7.8%   [█░░░░░░░░░░░░░░░░░░░]   7.8%
--------------------------------------------------------------------------------
Grand Total: ₹13,900.00 across 7 categories (9 transactions)
================================================================================
```

---

## 📅 6-Week Project Roadmap Checklist

- [x] **Week 1: Foundation & Setup** — Project structure, module layout, version control setup.
- [x] **Week 2: Core Classes & Data Structures** — `Expense` model, properties, list and dictionary representation.
- [x] **Week 3: File Operations & Persistence** — CSV reader/writer, auto directory generation, data persistence.
- [x] **Week 4: User Interface & Features** — Menu interface, input loops, cancellation handling, table views.
- [x] **Week 5: Advanced Features** — Category analytics, monthly aggregations, ASCII visual distribution bars, report exports.
- [x] **Week 6: Testing & Deployment** — 100% passing unit tests, Windows UTF-8 encoding support, full documentation.
