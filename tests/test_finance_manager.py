"""
Test Suite for Personal Finance Manager
Validates all core functionality and edge cases.
"""

import os
import sys
import shutil
import unittest

# Ensure src/ is in sys.path
SRC_DIR = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))
if SRC_DIR not in sys.path:
    sys.path.insert(0, SRC_DIR)

from expense import Expense
import utils
import reports
import file_manager

TEST_DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_temp")
TEST_CSV = os.path.join(TEST_DATA_DIR, "test_expenses.csv")
TEST_BACKUP_DIR = os.path.join(TEST_DATA_DIR, "backups")


class TestExpenseClass(unittest.TestCase):
    def test_expense_creation(self):
        exp = Expense(1500.5, "food", "2024-01-15", "Dinner at hotel")
        self.assertEqual(exp.amount, 1500.5)
        self.assertEqual(exp.category, "Food")
        self.assertEqual(exp.date, "2024-01-15")
        self.assertEqual(exp.description, "Dinner at hotel")
        self.assertEqual(exp.month_year, "2024-01")
        self.assertIn("₹1500.50", str(exp))

    def test_expense_row_conversion(self):
        exp = Expense(250.0, "Transport", "2024-02-10", "Bus ticket")
        row = exp.to_row()
        self.assertEqual(row, ["2024-02-10", "Transport", "250.00", "Bus ticket"])
        reconstructed = Expense.from_row(row)
        self.assertEqual(reconstructed.amount, exp.amount)
        self.assertEqual(reconstructed.category, exp.category)
        self.assertEqual(reconstructed.date, exp.date)
        self.assertEqual(reconstructed.description, exp.description)


class TestUtilsValidation(unittest.TestCase):
    def test_amount_validation(self):
        valid, val, _ = utils.validate_amount("1500")
        self.assertTrue(valid)
        self.assertEqual(val, 1500.0)

        valid, val, _ = utils.validate_amount("₹ 2,450.50")
        self.assertTrue(valid)
        self.assertEqual(val, 2450.5)

        valid, _, err = utils.validate_amount("-50")
        self.assertFalse(valid)
        self.assertIn("greater than 0", err)

        valid, _, err = utils.validate_amount("abc")
        self.assertFalse(valid)

    def test_date_validation(self):
        valid, val, _ = utils.validate_date("2024-05-20")
        self.assertTrue(valid)
        self.assertEqual(val, "2024-05-20")

        # Invalid date format
        valid, _, _ = utils.validate_date("20-05-2024")
        self.assertFalse(valid)

        # Invalid day for month
        valid, _, _ = utils.validate_date("2024-02-31")
        self.assertFalse(valid)

        # Empty string with allow_blank_for_today=True
        valid, val, _ = utils.validate_date("", allow_blank_for_today=True)
        self.assertTrue(valid)
        self.assertEqual(len(val), 10)

    def test_category_validation(self):
        valid, val, _ = utils.validate_category("food")
        self.assertTrue(valid)
        self.assertEqual(val, "Food")

        # Category by number
        valid, val, _ = utils.validate_category("1")
        self.assertTrue(valid)
        self.assertEqual(val, "Food")

        # Custom category
        valid, val, _ = utils.validate_category("Freelance Tools")
        self.assertTrue(valid)
        self.assertEqual(val, "Freelance Tools")


class TestReportsCalculations(unittest.TestCase):
    def setUp(self):
        self.sample_expenses = [
            Expense(100.0, "Food", "2024-01-10", "Lunch"),
            Expense(200.0, "Food", "2024-01-15", "Dinner"),
            Expense(300.0, "Transport", "2024-02-05", "Fuel"),
            Expense(400.0, "Shopping", "2024-02-12", "Clothes"),
        ]

    def test_totals_and_averages(self):
        self.assertEqual(reports.calculate_total(self.sample_expenses), 1000.0)
        self.assertEqual(reports.calculate_average(self.sample_expenses), 250.0)

    def test_category_summary(self):
        cat_summary = reports.get_category_summary(self.sample_expenses)
        self.assertIn("Food", cat_summary)
        self.assertEqual(cat_summary["Food"]["total"], 300.0)
        self.assertEqual(cat_summary["Food"]["count"], 2)
        self.assertEqual(cat_summary["Food"]["percentage"], 30.0)
        self.assertEqual(cat_summary["Shopping"]["total"], 400.0)

    def test_monthly_summary(self):
        monthly = reports.get_monthly_summary(self.sample_expenses)
        self.assertIn("2024-01", monthly)
        self.assertIn("2024-02", monthly)
        self.assertEqual(monthly["2024-01"]["total"], 300.0)
        self.assertEqual(monthly["2024-02"]["total"], 700.0)

    def test_filter_expenses(self):
        filtered_cat = reports.filter_expenses(self.sample_expenses, category="Transport")
        self.assertEqual(len(filtered_cat), 1)
        self.assertEqual(filtered_cat[0].description, "Fuel")

        filtered_kw = reports.filter_expenses(self.sample_expenses, keyword="lunch")
        self.assertEqual(len(filtered_kw), 1)

        filtered_amt = reports.filter_expenses(self.sample_expenses, min_amount=250.0)
        self.assertEqual(len(filtered_amt), 2)


class TestFileManagerOperations(unittest.TestCase):
    def setUp(self):
        os.makedirs(TEST_DATA_DIR, exist_ok=True)
        os.makedirs(TEST_BACKUP_DIR, exist_ok=True)

    def tearDown(self):
        if os.path.exists(TEST_DATA_DIR):
            shutil.rmtree(TEST_DATA_DIR)

    def test_save_load_append(self):
        expenses = [
            Expense(500.0, "Food", "2024-03-01", "Groceries"),
            Expense(120.0, "Transport", "2024-03-02", "Bus"),
        ]
        save_res = file_manager.save_expenses(expenses, TEST_CSV)
        self.assertTrue(save_res)

        loaded = file_manager.load_expenses(TEST_CSV)
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].amount, 500.0)

        new_exp = Expense(80.0, "Entertainment", "2024-03-03", "Cinema snack")
        append_res = file_manager.append_expense(new_exp, TEST_CSV)
        self.assertTrue(append_res)

        reloaded = file_manager.load_expenses(TEST_CSV)
        self.assertEqual(len(reloaded), 3)

    def test_backup_and_restore(self):
        expenses = [Expense(500.0, "Food", "2024-03-01", "Groceries")]
        file_manager.save_expenses(expenses, TEST_CSV)

        success, backup_path = file_manager.create_backup(TEST_CSV, TEST_BACKUP_DIR)
        self.assertTrue(success)
        self.assertTrue(os.path.exists(backup_path))

        # Overwrite file with different data
        modified_expenses = [Expense(999.0, "Shopping", "2024-03-05", "Watch")]
        file_manager.save_expenses(modified_expenses, TEST_CSV)
        self.assertEqual(file_manager.load_expenses(TEST_CSV)[0].amount, 999.0)

        # Restore from backup
        restore_res, _ = file_manager.restore_backup(backup_path, TEST_CSV, TEST_BACKUP_DIR)
        self.assertTrue(restore_res)
        restored_data = file_manager.load_expenses(TEST_CSV)
        self.assertEqual(len(restored_data), 1)
        self.assertEqual(restored_data[0].amount, 500.0)


if __name__ == "__main__":
    unittest.main()
