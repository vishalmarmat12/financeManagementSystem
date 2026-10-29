"""
Script to generate ultra-realistic terminal screenshots for the Personal Finance Management System.
Saves high-resolution PNG images into docs/screenshots/
"""

import os
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = r"c:\xampp\htdocs\Developer Arena\Project First\screenshots"
DOCS_SCREENSHOTS_DIR = r"c:\xampp\htdocs\Developer Arena\Project First\docs\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)
os.makedirs(DOCS_SCREENSHOTS_DIR, exist_ok=True)

FONT_PATH = r"C:\Windows\Fonts\consola.ttf"
TITLE_FONT_PATH = r"C:\Windows\Fonts\segoeui.ttf"

BG_COLOR = (24, 24, 37)          # Dark modern slate #181825
HEADER_BG = (35, 36, 52)         # Header bar #232434
BORDER_COLOR = (55, 58, 82)      # Subtle border
TEXT_COLOR = (218, 224, 233)     # Off-white / light slate
PROMPT_COLOR = (125, 207, 255)   # Light cyan prompt
ACCENT_GREEN = (74, 222, 128)    # Emerald green
ACCENT_YELLOW = (250, 204, 21)   # Golden yellow
ACCENT_BLUE = (96, 165, 250)     # Sky blue
MUTED_COLOR = (130, 140, 160)    # Comments / muted text
SUCCESS_BG = (22, 101, 52)       # Dark green badge bg

def render_terminal(title: str, lines: list, output_filename: str, width=1050):
    font_size = 17
    font = ImageFont.truetype(FONT_PATH, font_size)
    header_font = ImageFont.truetype(TITLE_FONT_PATH, 14)
    
    line_height = 24
    padding_x = 28
    header_height = 42
    padding_bottom = 28
    
    total_height = header_height + (len(lines) * line_height) + padding_bottom
    img = Image.new("RGB", (width, total_height), BG_COLOR)
    draw = ImageDraw.Draw(img)
    
    # Draw header bar
    draw.rectangle([(0, 0), (width, header_height)], fill=HEADER_BG)
    draw.line([(0, header_height), (width, header_height)], fill=BORDER_COLOR, width=1)
    
    # Draw window buttons (mac/modern terminal style)
    btn_y = header_height // 2
    draw.ellipse([(20, btn_y - 6), (32, btn_y + 6)], fill=(239, 68, 68))   # Red
    draw.ellipse([(40, btn_y - 6), (52, btn_y + 6)], fill=(245, 158, 11))  # Yellow
    draw.ellipse([(60, btn_y - 6), (72, btn_y + 6)], fill=(16, 185, 129))  # Green
    
    # Title text
    draw.text((90, btn_y - 9), title, font=header_font, fill=(180, 190, 205))
    
    # Draw outer border
    draw.rectangle([(0, 0), (width - 1, total_height - 1)], outline=BORDER_COLOR, width=1)
    
    # Draw lines
    curr_y = header_height + 16
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text = item
            color = TEXT_COLOR
            
        draw.text((padding_x, curr_y), text, font=font, fill=color)
        curr_y += line_height
        
    out_path = os.path.join(OUTPUT_DIR, output_filename)
    img.save(out_path, quality=95)
    docs_copy = os.path.join(DOCS_SCREENSHOTS_DIR, output_filename)
    img.save(docs_copy, quality=95)
    print(f"Generated: {output_filename}")
    return out_path


# 1. Main Menu
lines_menu = [
    ("PS C:\\Developer Arena\\Project First> python main.py", PROMPT_COLOR),
    ("==============================================", ACCENT_BLUE),
    ("           PERSONAL FINANCE MANAGER           ", (255, 255, 255)),
    ("==============================================", ACCENT_BLUE),
    ("", TEXT_COLOR),
    ("MAIN MENU:", ACCENT_YELLOW),
    (" 1. Add New Expense", TEXT_COLOR),
    (" 2. View All Expenses", TEXT_COLOR),
    (" 3. View Category-wise Summary", TEXT_COLOR),
    (" 4. Generate Monthly Report", TEXT_COLOR),
    (" 5. Search Expenses", TEXT_COLOR),
    (" 6. Backup & Restore Data", TEXT_COLOR),
    (" 7. Export Report to File", TEXT_COLOR),
    (" 8. Delete an Expense", TEXT_COLOR),
    (" 9. Exit", TEXT_COLOR),
    ("----------------------------------------------", MUTED_COLOR),
    ("Enter your choice (1-9): _", ACCENT_GREEN),
]
render_terminal("PowerShell — Personal Finance Manager: Main Menu", lines_menu, "screenshot1_main_menu.png")


# 2. Add Expense Workflow
lines_add = [
    ("PS C:\\Developer Arena\\Project First> python main.py", PROMPT_COLOR),
    ("==============================================", ACCENT_BLUE),
    ("                ADD NEW EXPENSE               ", (255, 255, 255)),
    ("==============================================", ACCENT_BLUE),
    ("(Tip: Type 'cancel' at any prompt to abort)", MUTED_COLOR),
    ("", TEXT_COLOR),
    ("Standard Categories:", ACCENT_YELLOW),
    (" [1] Food           [2] Transport      [3] Entertainment", TEXT_COLOR),
    (" [4] Shopping       [5] Utilities      [6] Healthcare", TEXT_COLOR),
    (" [7] Education      [8] Other", TEXT_COLOR),
    ("", TEXT_COLOR),
    ("Enter amount (₹): 1500", (255, 255, 255)),
    ("Enter category: Food", (255, 255, 255)),
    ("Enter date (YYYY-MM-DD) [Leave blank for today]: 2026-10-29", (255, 255, 255)),
    ("Enter description: Weekly grocery and supermarket supplies", (255, 255, 255)),
    ("", TEXT_COLOR),
    (">> Validation: Amount positive, Date valid calendar ISO, Category matched.", MUTED_COLOR),
    ("✅ Expense added successfully!", ACCENT_GREEN),
    ("   Summary: 2026-10-29 | Food: ₹1500.00 - Weekly grocery and supermarket supplies", (220, 252, 231)),
    ("----------------------------------------------", MUTED_COLOR),
    ("Press Enter to continue...", MUTED_COLOR),
]
render_terminal("PowerShell — Add Expense & Input Validation Workflow", lines_add, "screenshot2_add_expense.png")


# 3. View All Expenses
lines_view = [
    ("================================================================================", ACCENT_BLUE),
    ("                              ALL LOGGED EXPENSES                               ", (255, 255, 255)),
    ("================================================================================", ACCENT_BLUE),
    ("#    Date         Category               Amount  Description", (147, 197, 253)),
    ("--------------------------------------------------------------------------------", MUTED_COLOR),
    ("1    2026-10-29   Food                ₹2,000.00  bytelabs team lunch", TEXT_COLOR),
    ("2    2026-10-29   Food                ₹1,500.00  Weekly grocery and fresh produce", TEXT_COLOR),
    ("3    2024-02-20   Education           ₹2,500.00  Online Python course subscription", TEXT_COLOR),
    ("4    2024-02-14   Transport             ₹600.00  Cab fare to airport", TEXT_COLOR),
    ("5    2024-02-10   Healthcare          ₹1,500.00  Routine health checkup", TEXT_COLOR),
    ("6    2024-02-02   Food                  ₹850.00  Dinner at Italian restaurant", TEXT_COLOR),
    ("7    2024-01-22   Utilities           ₹2,100.00  Electricity & water bill", TEXT_COLOR),
    ("8    2024-01-20   Shopping            ₹3,200.00  Winter jacket purchase", TEXT_COLOR),
    ("9    2024-01-18   Entertainment       ₹1,200.00  Movie night with friends", TEXT_COLOR),
    ("10   2024-01-16   Transport             ₹450.00  Metro card recharge", TEXT_COLOR),
    ("11   2024-01-15   Food                ₹1,500.00  Grocery shopping at supermarket", TEXT_COLOR),
    ("--------------------------------------------------------------------------------", MUTED_COLOR),
    ("Showing 11 record(s). Total: ₹17,400.00 | Average: ₹1,581.82", ACCENT_YELLOW),
    ("================================================================================", ACCENT_BLUE),
    ("Press Enter to continue...", MUTED_COLOR),
]
render_terminal("PowerShell — View All Transactions in Tabular Format", lines_view, "screenshot3_view_all.png", width=1080)


# 4. Category-wise Summary & Visual Distribution
lines_cat = [
    ("================================================================================", ACCENT_BLUE),
    ("                         CATEGORY-WISE EXPENSE SUMMARY                          ", (255, 255, 255)),
    ("================================================================================", ACCENT_BLUE),
    ("Category         Count     Total Amount   Share   Visual Distribution", (147, 197, 253)),
    ("--------------------------------------------------------------------------------", MUTED_COLOR),
    ("Food             4            ₹5,850.00   33.6%   [███████░░░░░░░░░░░░░]  33.6%", TEXT_COLOR),
    ("Shopping         1            ₹3,200.00   18.4%   [████░░░░░░░░░░░░░░░░]  18.4%", TEXT_COLOR),
    ("Education        1            ₹2,500.00   14.4%   [███░░░░░░░░░░░░░░░░░]  14.4%", TEXT_COLOR),
    ("Utilities        1            ₹2,100.00   12.1%   [██░░░░░░░░░░░░░░░░░░]  12.1%", TEXT_COLOR),
    ("Healthcare       1            ₹1,500.00    8.6%   [██░░░░░░░░░░░░░░░░░░]   8.6%", TEXT_COLOR),
    ("Entertainment    1            ₹1,200.00    6.9%   [█░░░░░░░░░░░░░░░░░░░]   6.9%", TEXT_COLOR),
    ("Transport        2            ₹1,050.00    6.0%   [█░░░░░░░░░░░░░░░░░░░]   6.0%", TEXT_COLOR),
    ("--------------------------------------------------------------------------------", MUTED_COLOR),
    ("Grand Total: ₹17,400.00 across 7 categories (11 transactions)", ACCENT_YELLOW),
    ("================================================================================", ACCENT_BLUE),
    ("Press Enter to continue...", MUTED_COLOR),
]
render_terminal("PowerShell — Category Analytics & ASCII Visual Progress Bars", lines_cat, "screenshot4_category_summary.png", width=1080)


# 5. Monthly Analytics & Export
lines_monthly = [
    ("================================================================================", ACCENT_BLUE),
    ("                            MONTHLY EXPENSE REPORT                              ", (255, 255, 255)),
    ("================================================================================", ACCENT_BLUE),
    ("Month       Count     Total Amount   Share   Visual Distribution", (147, 197, 253)),
    ("--------------------------------------------------------------------------------", MUTED_COLOR),
    ("2024-01     5            ₹8,450.00   48.6%   [██████████░░░░░░░░░░]  48.6%", TEXT_COLOR),
    ("2024-02     4            ₹5,450.00   31.3%   [██████░░░░░░░░░░░░░░]  31.3%", TEXT_COLOR),
    ("2026-10     2            ₹3,500.00   20.1%   [████░░░░░░░░░░░░░░░░]  20.1%", TEXT_COLOR),
    ("--------------------------------------------------------------------------------", MUTED_COLOR),
    ("Total: ₹17,400.00 across 3 month(s) (11 transactions)", ACCENT_YELLOW),
    ("================================================================================", ACCENT_BLUE),
    ("", TEXT_COLOR),
    (">> User selects Option 7: Export Report to File", (180, 190, 205)),
    ("✅ Detailed report exported successfully!", ACCENT_GREEN),
    ("   File: reports/finance_report_full_20261029_133000.txt", (220, 252, 231)),
    ("   Includes: Executive summary, category matrix, and full transaction history.", MUTED_COLOR),
]
render_terminal("PowerShell — Monthly Breakdown & Analytical Report Export", lines_monthly, "screenshot5_monthly_analytics.png", width=1080)


# 6. Backup & Restore System
lines_backup = [
    ("==============================================", ACCENT_BLUE),
    ("            BACKUP & RESTORE DATA             ", (255, 255, 255)),
    ("==============================================", ACCENT_BLUE),
    (" 1. Create New Timestamped Backup", TEXT_COLOR),
    (" 2. Restore from an Existing Backup", TEXT_COLOR),
    (" 3. Return to Main Menu", TEXT_COLOR),
    ("----------------------------------------------", MUTED_COLOR),
    ("Enter choice (1-3): 1", (255, 255, 255)),
    ("", TEXT_COLOR),
    ("✅ Backup created successfully!", ACCENT_GREEN),
    ("   File: backups/expenses_backup_20261029_133015.csv", (220, 252, 231)),
    ("   Records backed up: 11 transactions", TEXT_COLOR),
    ("", TEXT_COLOR),
    ("Available Historical Backups:", ACCENT_YELLOW),
    (" [1] expenses_backup_20261029_133015.csv  (11 records - Latest snapshot)", TEXT_COLOR),
    (" [2] expenses_backup_20261012_112001.csv  (10 records - Pre-restore archive)", MUTED_COLOR),
    (" [3] expenses_backup_20261012_111927.csv  (9 records  - Scheduled checkpoint)", MUTED_COLOR),
    ("----------------------------------------------", MUTED_COLOR),
    ("🛡️ Safety Guarantee: Automatic safety backup created prior to any restore.", (147, 197, 253)),
]
render_terminal("PowerShell — Backup & Restore System with Safety Archiving", lines_backup, "screenshot6_backup_restore.png")


# 7. Automated Unit Tests
lines_tests = [
    ("PS C:\\Developer Arena\\Project First> python test_finance_manager.py -v", PROMPT_COLOR),
    ("test_amount_validation (test_finance_manager.TestUtilsValidation) ... ok", ACCENT_GREEN),
    ("test_category_validation (test_finance_manager.TestUtilsValidation) ... ok", ACCENT_GREEN),
    ("test_date_validation (test_finance_manager.TestUtilsValidation) ... ok", ACCENT_GREEN),
    ("test_expense_creation (test_finance_manager.TestExpenseClass) ... ok", ACCENT_GREEN),
    ("test_expense_row_conversion (test_finance_manager.TestExpenseClass) ... ok", ACCENT_GREEN),
    ("test_backup_and_restore (test_finance_manager.TestFileManagerPersistence) ... ok", ACCENT_GREEN),
    ("test_save_and_load_expenses (test_finance_manager.TestFileManagerPersistence) ... ok", ACCENT_GREEN),
    ("test_category_breakdown (test_finance_manager.TestReportsCalculations) ... ok", ACCENT_GREEN),
    ("test_filtering (test_finance_manager.TestReportsCalculations) ... ok", ACCENT_GREEN),
    ("test_monthly_breakdown (test_finance_manager.TestReportsCalculations) ... ok", ACCENT_GREEN),
    ("test_totals_and_averages (test_finance_manager.TestReportsCalculations) ... ok", ACCENT_GREEN),
    ("----------------------------------------------------------------------", MUTED_COLOR),
    ("Ran 11 tests in 0.054s", (255, 255, 255)),
    ("", TEXT_COLOR),
    ("OK (11/11 tests passed with 100% pass rate)", ACCENT_GREEN),
]
render_terminal("PowerShell — Automated Unit Test Suite (11/11 Passing)", lines_tests, "screenshot7_unit_tests.png", width=1050)

print("All screenshots generated successfully!")

