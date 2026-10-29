"""
Reports Module
Handles financial calculations, category analysis, monthly summaries,
tabular displays, ASCII charts, and report file export.
"""

import os
from datetime import datetime
from typing import List, Dict, Any, Optional
from expense import Expense
from utils import format_currency, create_ascii_bar, truncate_text

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORTS_DIR = os.path.join(BASE_DIR, "reports")


def calculate_total(expenses: List[Expense]) -> float:
    """Calculates total sum of all expenses."""
    return round(sum(exp.amount for exp in expenses), 2)


def calculate_average(expenses: List[Expense]) -> float:
    """Calculates mean expense amount."""
    if not expenses:
        return 0.0
    return round(calculate_total(expenses) / len(expenses), 2)


def get_category_summary(expenses: List[Expense]) -> Dict[str, Dict[str, Any]]:
    """
    Computes category-wise aggregated statistics.

    Returns:
        Dictionary mapping category name to:
        { 'total': float, 'count': int, 'percentage': float, 'average': float }
        Sorted by total amount descending.
    """
    grand_total = calculate_total(expenses)
    cat_data: Dict[str, Dict[str, Any]] = {}

    for exp in expenses:
        cat = exp.category
        if cat not in cat_data:
            cat_data[cat] = {"total": 0.0, "count": 0}
        cat_data[cat]["total"] = round(cat_data[cat]["total"] + exp.amount, 2)
        cat_data[cat]["count"] += 1

    # Add percentages and averages
    for cat, vals in cat_data.items():
        vals["percentage"] = round((vals["total"] / grand_total * 100), 1) if grand_total > 0 else 0.0
        vals["average"] = round(vals["total"] / vals["count"], 2) if vals["count"] > 0 else 0.0

    # Sort by total descending
    sorted_summary = dict(sorted(cat_data.items(), key=lambda item: item[1]["total"], reverse=True))
    return sorted_summary


def get_monthly_summary(expenses: List[Expense]) -> Dict[str, Dict[str, Any]]:
    """
    Groups expenses by YYYY-MM.

    Returns:
        Dictionary mapping 'YYYY-MM' to { 'total': float, 'count': int, 'expenses': List[Expense] }
        Sorted by month ascending.
    """
    monthly: Dict[str, Dict[str, Any]] = {}
    for exp in sorted(expenses, key=lambda x: x.date):
        m = exp.month_year
        if m not in monthly:
            monthly[m] = {"total": 0.0, "count": 0, "expenses": []}
        monthly[m]["total"] = round(monthly[m]["total"] + exp.amount, 2)
        monthly[m]["count"] += 1
        monthly[m]["expenses"].append(exp)

    return monthly


def get_summary_stats(expenses: List[Expense]) -> Dict[str, Any]:
    """Generates a high-level summary overview."""
    if not expenses:
        return {
            "count": 0,
            "total": 0.0,
            "average": 0.0,
            "highest": None,
            "lowest": None,
            "top_category": None,
        }

    highest_exp = max(expenses, key=lambda x: x.amount)
    lowest_exp = min(expenses, key=lambda x: x.amount)
    cat_summary = get_category_summary(expenses)
    top_cat = next(iter(cat_summary.items())) if cat_summary else None

    return {
        "count": len(expenses),
        "total": calculate_total(expenses),
        "average": calculate_average(expenses),
        "highest": highest_exp,
        "lowest": lowest_exp,
        "top_category": (top_cat[0], top_cat[1]["total"]) if top_cat else None,
    }


def filter_expenses(
    expenses: List[Expense],
    keyword: Optional[str] = None,
    category: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
) -> List[Expense]:
    """Filters expenses matching all provided criteria."""
    filtered = expenses

    if keyword:
        kw = keyword.lower()
        filtered = [e for e in filtered if kw in e.description.lower() or kw in e.category.lower()]

    if category:
        cat_lower = category.lower()
        filtered = [e for e in filtered if e.category.lower() == cat_lower]

    if start_date:
        filtered = [e for e in filtered if e.date >= start_date]

    if end_date:
        filtered = [e for e in filtered if e.date <= end_date]

    if min_amount is not None:
        filtered = [e for e in filtered if e.amount >= min_amount]

    if max_amount is not None:
        filtered = [e for e in filtered if e.amount <= max_amount]

    return filtered


def display_expenses_table(expenses: List[Expense], title: str = "ALL EXPENSES") -> None:
    """Renders a clean tabular list of expenses in the console."""
    print("=" * 80)
    print(f" {title.center(78)} ")
    print("=" * 80)

    if not expenses:
        print("\n  No expense records found.\n")
        print("=" * 80)
        return

    # Table Header
    print(f"{'#':<4} {'Date':<12} {'Category':<16} {'Amount':>12}  {'Description':<32}")
    print("-" * 80)

    # Sort by date descending
    sorted_expenses = sorted(expenses, key=lambda x: x.date, reverse=True)

    for idx, exp in enumerate(sorted_expenses, start=1):
        desc = truncate_text(exp.description, 30)
        formatted_amt = format_currency(exp.amount)
        print(f"{idx:<4} {exp.date:<12} {exp.category:<16} {formatted_amt:>12}  {desc:<32}")

    print("-" * 80)
    total_str = format_currency(calculate_total(expenses))
    avg_str = format_currency(calculate_average(expenses))
    print(f"Total Transactions: {len(expenses):<5} | Average: {avg_str:<12} | Grand Total: {total_str}")
    print("=" * 80)


def display_category_summary(expenses: List[Expense]) -> None:
    """Renders category-wise breakdown with ASCII distribution bars."""
    print("=" * 80)
    print(f" {'CATEGORY-WISE EXPENSE SUMMARY':^78} ")
    print("=" * 80)

    if not expenses:
        print("\n  No expense records found.\n")
        print("=" * 80)
        return

    summary = get_category_summary(expenses)
    grand_total = calculate_total(expenses)

    print(f"{'Category':<16} {'Count':<7} {'Total Amount':>14} {'Share':>7}   {'Visual Distribution'}")
    print("-" * 80)

    for cat, data in summary.items():
        amt_str = format_currency(data["total"])
        pct = data["percentage"]
        bar = create_ascii_bar(pct, width=20)
        print(f"{cat:<16} {data['count']:<7} {amt_str:>14} {pct:>6.1f}%   {bar}")

    print("-" * 80)
    print(f"Grand Total: {format_currency(grand_total)} across {len(summary)} categories ({len(expenses)} transactions)")
    print("=" * 80)


def display_monthly_report(expenses: List[Expense]) -> None:
    """Renders a month-by-month financial report."""
    print("=" * 80)
    print(f" {'MONTHLY EXPENSE REPORT':^78} ")
    print("=" * 80)

    if not expenses:
        print("\n  No expense records found.\n")
        print("=" * 80)
        return

    monthly = get_monthly_summary(expenses)
    grand_total = calculate_total(expenses)

    print(f"{'Month (YYYY-MM)':<18} {'Transactions':<14} {'Monthly Total':>16} {'% of Overall':>14}")
    print("-" * 80)

    for month, data in monthly.items():
        m_amt = format_currency(data["total"])
        pct = (data["total"] / grand_total * 100) if grand_total > 0 else 0.0
        print(f"{month:<18} {data['count']:<14} {m_amt:>16} {pct:>13.1f}%")

    print("-" * 80)
    print(f"Total Across All Months: {format_currency(grand_total)}")
    print("=" * 80)


def export_report_to_file(expenses: List[Expense], report_type: str = "full") -> str:
    """
    Exports summary report to a formatted text file in reports/ directory.

    Returns:
        Exported file path.
    """
    os.makedirs(REPORTS_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filepath = os.path.join(REPORTS_DIR, f"finance_report_{report_type}_{timestamp}.txt")

    stats = get_summary_stats(expenses)
    cat_summary = get_category_summary(expenses)
    monthly_summary = get_monthly_summary(expenses)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 80 + "\n")
        f.write("               PERSONAL FINANCE MANAGER - FINANCIAL REPORT\n")
        f.write(f" Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 80 + "\n\n")

        # Overview Stats
        f.write("1. EXECUTIVE SUMMARY\n")
        f.write("-" * 40 + "\n")
        f.write(f"Total Transactions : {stats['count']}\n")
        f.write(f"Grand Total Spent  : {format_currency(stats['total'])}\n")
        f.write(f"Average Expense    : {format_currency(stats['average'])}\n")
        if stats["highest"]:
            f.write(f"Highest Expense    : {format_currency(stats['highest'].amount)} ({stats['highest'].category} - {stats['highest'].description} on {stats['highest'].date})\n")
        if stats["lowest"]:
            f.write(f"Lowest Expense     : {format_currency(stats['lowest'].amount)} ({stats['lowest'].category} - {stats['lowest'].description} on {stats['lowest'].date})\n")
        if stats["top_category"]:
            f.write(f"Top Category       : {stats['top_category'][0]} ({format_currency(stats['top_category'][1])})\n")
        f.write("\n")

        # Category Breakdown
        f.write("2. CATEGORY BREAKDOWN\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Category':<18} {'Count':<8} {'Total Amount':>14} {'Share':>8}\n")
        f.write("-" * 80 + "\n")
        for cat, data in cat_summary.items():
            f.write(f"{cat:<18} {data['count']:<8} {format_currency(data['total']):>14} {data['percentage']:>7.1f}%\n")
        f.write("-" * 80 + "\n\n")

        # Monthly Breakdown
        f.write("3. MONTHLY BREAKDOWN\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Month':<18} {'Count':<8} {'Total Amount':>14}\n")
        f.write("-" * 80 + "\n")
        for month, data in monthly_summary.items():
            f.write(f"{month:<18} {data['count']:<8} {format_currency(data['total']):>14}\n")
        f.write("-" * 80 + "\n\n")

        # Transaction Log
        f.write("4. COMPLETE TRANSACTION LOG\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'#':<4} {'Date':<12} {'Category':<16} {'Amount':>12}  {'Description'}\n")
        f.write("-" * 80 + "\n")
        for idx, exp in enumerate(sorted(expenses, key=lambda x: x.date, reverse=True), start=1):
            f.write(f"{idx:<4} {exp.date:<12} {exp.category:<16} {format_currency(exp.amount):>12}  {exp.description}\n")
        f.write("-" * 80 + "\n")

    return filepath
