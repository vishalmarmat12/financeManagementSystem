# 📘 Personal Finance Management System — User Guide & Manual

Welcome to the comprehensive User Guide for the **Personal Finance Management System**. This guide provides an end-to-end operational walkthrough of all interactive workflows, validation mechanisms, analytics, and safety features.

---

## 📑 Table of Contents
1. [Introduction & Purpose](#1-introduction--purpose)
2. [Installation & Requirements](#2-installation--requirements)
3. [Quick Start Guide](#3-quick-start-guide)
4. [Detailed Feature Walkthrough](#4-detailed-feature-walkthrough)
   - [Menu Option 1: Add New Expense](#menu-option-1-add-new-expense)
   - [Menu Option 2: View All Expenses](#menu-option-2-view-all-expenses)
   - [Menu Option 3: Category-wise Summary & ASCII Charts](#menu-option-3-category-wise-summary--ascii-charts)
   - [Menu Option 4: Generate Monthly Report](#menu-option-4-generate-monthly-report)
   - [Menu Option 5: Search & Filter Expenses](#menu-option-5-search--filter-expenses)
   - [Menu Option 6: Backup & Restore Data](#menu-option-6-backup--restore-data)
   - [Menu Option 7: Export Detailed Report to File](#menu-option-7-export-detailed-report-to-file)
   - [Menu Option 8: Delete an Expense](#menu-option-8-delete-an-expense)
   - [Menu Option 9: Exit](#menu-option-9-exit)
5. [Data Validation Rules](#5-data-validation-rules)
6. [Data Persistence & Safety Mechanisms](#6-data-persistence--safety-mechanisms)
7. [Running Unit Tests](#7-running-unit-tests)
8. [Troubleshooting & FAQs](#8-troubleshooting--faqs)

---

## 1. Introduction & Purpose

The Personal Finance Management System is an offline, non-volatile financial tracking tool built with Python. It allows users to record, categorize, inspect, and analyze personal expenses with automated statistical calculations and visual distribution charts directly in the terminal.

---

## 2. Installation & Requirements

- **Python Version:** Python 3.8+ (Compatible with Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14+)
- **Operating System:** Windows, macOS, Linux
- **Dependencies:** Standard Library only for core app. Optional packages in `requirements.txt` (`reportlab`, `pillow`) are used for documentation and screenshot generation.

### Setup Steps:
```bash
# 1. Clone repository
git clone https://github.com/vishalmarmat12/financeManagementSystem.git
cd financeManagementSystem

# 2. (Optional) Install documentation dependencies
pip install -r requirements.txt
```

---

## 3. Quick Start Guide

Launch the application directly from the root directory:
```bash
python main.py
```

Upon launch, the application verifies the directory structure (`data/`, `backups/`, `reports/`) and presents the primary interactive menu:

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

## 4. Detailed Feature Walkthrough

### Menu Option 1: Add New Expense
Captures a new financial transaction with real-time field validation:
1. **Amount:** Accepts integer or decimal numbers (e.g., `1500`, `2450.50`). Currency symbols (`₹`, `$`) and formatting commas (`1,500`) are automatically parsed and stripped.
2. **Category:** Choose by number (`1-8`) or type the category name (`Food`, `Shopping`, etc.). Custom category names are also supported.
3. **Date:** Input `YYYY-MM-DD` (e.g., `2026-10-29`). Leaving the date field blank automatically inputs today's date.
4. **Description:** Brief memo describing the transaction.
> **Note:** Type `cancel` at any prompt to safely abort the entry.

### Menu Option 2: View All Expenses
Displays all logged expenses in a structured tabular view sorted in reverse chronological order:
- Index number (`#`)
- Date (`YYYY-MM-DD`)
- Category
- Formatted Amount (`₹X,XXX.XX`)
- Description
- Footer with transaction count, grand total, and arithmetic average.

### Menu Option 3: Category-wise Summary & ASCII Charts
Calculates expenditure by category and renders proportional text progress bars in the console:
```text
Food             4            ₹5,850.00   33.6%   [███████░░░░░░░░░░░░░]  33.6%
Shopping         1            ₹3,200.00   18.4%   [████░░░░░░░░░░░░░░░░]  18.4%
Education        1            ₹2,500.00   14.4%   [███░░░░░░░░░░░░░░░░░]  14.4%
```

### Menu Option 4: Generate Monthly Report
Aggregates expenses by month (`YYYY-MM`), computing total amount spent and percentage share of the annual budget per month.

### Menu Option 5: Search & Filter Expenses
Allows multi-criteria filtering across:
- **Keyword Search:** Case-insensitive search matching description text.
- **Category Filter:** Filter by specific category.
- **Date Range:** Filter between start date and end date.
- **Amount Range:** Filter between minimum and maximum amounts.

### Menu Option 6: Backup & Restore Data
- **Create Backup:** Generates an immediate timestamped CSV snapshot in `backups/expenses_backup_YYYYMMDD_HHMMSS.csv`.
- **Restore Backup:** Allows selecting any previous snapshot. **Safety Guarantee:** Automatically generates a safety backup of your active data before performing any restoration.

### Menu Option 7: Export Detailed Report to File
Generates a comprehensive executive summary text file saved into `reports/finance_report_full_YYYYMMDD_HHMMSS.txt`. Includes summary metrics, category breakdown, monthly aggregates, and full transaction history.

### Menu Option 8: Delete an Expense
Displays transactions with their index numbers and prompts for confirmation before permanently removing the record and updating the CSV file.

### Menu Option 9: Exit
Safely closes the application.

---

## 5. Data Validation Rules

| Field | Rule Enforced | Error Recovery |
| :--- | :--- | :--- |
| **Amount** | Must be a strictly positive float (`> 0`). Currency symbols & commas permitted. | Re-prompts user with descriptive error message. |
| **Date** | Strict ISO calendar format (`YYYY-MM-DD`). Leap years verified (e.g., `2024-02-29` is valid, `2023-02-29` rejected). | Re-prompts user. Pressing Enter selects current date. |
| **Category** | Standard categories or custom string. | Matches case-insensitively or assigns custom name. |

---

## 6. Data Persistence & Safety Mechanisms

- **File Path:** `data/expenses.csv`
- **File Format:** RFC 4180 standard CSV (`Date,Category,Amount,Description`)
- **Safety Archiving:** Every restore action archives the active ledger into `backups/` before applying changes.

---

## 7. Running Unit Tests

The test suite validates 11 discrete operational criteria:
```bash
# Run unit tests directly
python tests/test_finance_manager.py -v

# Or run via Python unittest discovery
python -m unittest discover tests
```

---

## 8. Troubleshooting & FAQs

**Q: Why do I see encoding errors in Windows Command Prompt?**  
A: `main.py` automatically reconfigures standard I/O streams to UTF-8 on Windows. Ensure your console supports UTF-8 (such as Windows Terminal or PowerShell).

**Q: Where are backups stored?**  
A: Backups are stored in the `backups/` directory located at the project root.

