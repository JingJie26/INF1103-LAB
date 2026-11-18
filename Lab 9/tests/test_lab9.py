"""Automated tests for Lab 9.

Run from the project folder with:
    python -m unittest discover -s tests -v
"""
import contextlib
import inspect
import io
import os
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from digital_product import DigitalProduct
from discount_strategy import (BulkDiscount, DiscountStrategy, NoDiscount,
                               PercentageDiscount, StudentDiscount)
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from order_line import OrderLine
from physical_product import PhysicalProduct
from product import Product
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier

PRODUCTS_CSV = """product_type,product_id,name,price,stock_quantity
physical,P001,Desk Lamp,25.00,10
digital,D001,Photo Editor,49.90,100
service,S001,Installation,30.00,5
physical,P002,Office Chair,abc,3
physical,P003,Monitor Stand,39.50,7
"""


def make_supplier() -> Supplier:
    return Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")


def make_order_of_250(discount: DiscountStrategy | None = None) -> Order:
    supplier = make_supplier()
    desk = ProductFactory.create("physical", "P010", "Desk", 100.0, 20,
                                 supplier, weight=12.0)
    course = ProductFactory.create("digital", "D010", "Python Course", 50.0,
                                   999, supplier, download_size=800.0)
    order = Order("O001", discount)
    order.add_order_line(desk, 2)
    order.add_order_line(course, 1)
    return order


class TestDiscountStrategies(unittest.TestCase):
    def test_strategy_base_class_is_abstract(self):
        with self.assertRaises(TypeError):
            DiscountStrategy()

    def test_no_discount_returns_total_unchanged(self):
        self.assertEqual(NoDiscount().apply(250), 250)

    def test_percentage_discount(self):
        self.assertAlmostEqual(PercentageDiscount(10).apply(250), 225.0)

    def test_percentage_out_of_range_is_rejected(self):
        for bad in (-1, 101):
            with self.assertRaises(ValueError):
                PercentageDiscount(bad)

    def test_bulk_discount_at_or_above_threshold(self):
        bulk = BulkDiscount(200, 20)
        self.assertEqual(bulk.apply(250), 230)
        self.assertEqual(bulk.apply(200), 180)

    def test_bulk_discount_below_threshold(self):
        self.assertEqual(BulkDiscount(200, 20).apply(199.99), 199.99)

    def test_student_discount_takes_five_percent(self):
        self.assertAlmostEqual(StudentDiscount().apply(200), 190.0)


class TestOrderUsesStrategy(unittest.TestCase):
    def test_default_strategy_is_no_discount(self):
        order = make_order_of_250()
        self.assertIsInstance(order.get_discount(), NoDiscount)
        self.assertEqual(order.calculate_total(), 250)

    def test_total_goes_through_the_strategy(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        self.assertEqual(order.calculate_total(), 230)

    def test_set_discount_changes_strategy_on_existing_order(self):
        order = make_order_of_250(BulkDiscount(200, 20))
        order.set_discount(PercentageDiscount(10))
        self.assertAlmostEqual(order.calculate_total(), 225.0)

    def test_new_strategy_works_without_changing_order(self):
        class HalfPrice(DiscountStrategy):
            def apply(self, total: float) -> float:
                return total / 2

        order = make_order_of_250(HalfPrice())
        self.assertEqual(order.calculate_total(), 125)

    def test_two_orders_can_share_one_strategy(self):
        shared = PercentageDiscount(10)
        first = make_order_of_250(shared)
        second = make_order_of_250(shared)
        self.assertIs(first.get_discount(), second.get_discount())

    def test_order_has_no_discount_type_logic(self):
        source = inspect.getsource(Order.calculate_total)
        self.assertNotIn("elif", source)
        self.assertNotIn("discount_type", source)


class TestProductFactory(unittest.TestCase):
    def setUp(self):
        self.supplier = make_supplier()

    def test_creates_physical_product(self):
        product = ProductFactory.create("physical", "P001", "Desk Lamp",
                                        25.0, 10, self.supplier, weight=1.5)
        self.assertIsInstance(product, PhysicalProduct)
        self.assertIsInstance(product, Product)
        self.assertEqual(product.get_weight(), 1.5)

    def test_creates_digital_product(self):
        product = ProductFactory.create("digital", "D001", "Photo Editor",
                                        49.9, 100, self.supplier,
                                        download_size=250.0)
        self.assertIsInstance(product, DigitalProduct)
        self.assertEqual(product.get_download_size(), 250.0)

    def test_unknown_type_raises_value_error_with_clear_message(self):
        with self.assertRaises(ValueError) as caught:
            ProductFactory.create("service", "S001", "Installation", 30.0, 5,
                                  self.supplier)
        self.assertEqual(str(caught.exception),
                         "Unknown product type: service")


class TestValidation(unittest.TestCase):
    def setUp(self):
        self.supplier = make_supplier()

    def test_price_must_be_greater_than_zero(self):
        for bad_price in (0, -5):
            with self.assertRaises(ValueError):
                ProductFactory.create("physical", "P001", "Lamp", bad_price,
                                      10, self.supplier)

    def test_stock_cannot_be_negative(self):
        with self.assertRaises(ValueError):
            ProductFactory.create("digital", "D001", "Editor", 49.9, -1,
                                  self.supplier)

    def test_zero_stock_is_allowed(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 0,
                                        self.supplier)
        self.assertEqual(product.get_stock(), 0)

    def test_digital_product_keeps_the_stock_rule(self):
        product = ProductFactory.create("digital", "D001", "Editor", 49.9, 5,
                                        self.supplier)
        with self.assertRaises(ValueError):
            product.update_stock(-1)
        self.assertEqual(product.get_stock(), 5)

    def test_order_line_quantity_must_be_greater_than_zero(self):
        product = ProductFactory.create("physical", "P001", "Lamp", 25.0, 10,
                                        self.supplier)
        for bad_quantity in (0, -3):
            with self.assertRaises(ValueError):
                OrderLine(product, bad_quantity)

    def test_order_rejects_bad_quantity_and_keeps_its_lines(self):
        order = make_order_of_250()
        product = order.get_order_lines()[0].get_product()
        with self.assertRaises(ValueError):
            order.add_order_line(product, 0)
        self.assertEqual(len(order.get_order_lines()), 2)


class TestGetPositiveFloat(unittest.TestCase):
    def test_asks_again_until_input_is_valid(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=["abc", "-5", "12.50"]), \
                contextlib.redirect_stdout(output):
            value = get_positive_float("Price: ")
        self.assertEqual(value, 12.5)
        self.assertEqual(output.getvalue().splitlines(), [
            "Please enter a valid number, e.g. 12.50",
            "Please enter a number greater than zero.",
        ])


class TestLoadProducts(unittest.TestCase):
    def setUp(self):
        self.supplier = make_supplier()
        self.inventory = Inventory()
        self.folder = tempfile.TemporaryDirectory()
        self.addCleanup(self.folder.cleanup)
        self.path = os.path.join(self.folder.name, "products.csv")

    def load(self, path: str) -> list[str]:
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            load_products(path, self.inventory, self.supplier)
        return output.getvalue().splitlines()

    def test_valid_rows_load_and_bad_rows_are_skipped(self):
        with open(self.path, "w", newline="") as file:
            file.write(PRODUCTS_CSV)
        lines = self.load(self.path)

        ids = [p.get_product_id() for p in self.inventory.get_products()]
        self.assertEqual(ids, ["P001", "D001", "P003"])
        self.assertEqual(len(lines), 4)
        self.assertIn("Unknown product type: service", lines[0])
        self.assertIn("Office Chair", lines[1])
        self.assertEqual(lines[2], "3 products loaded.")
        self.assertEqual(lines[3], "Load attempt finished.")

    def test_missing_file_is_handled_gracefully(self):
        missing = os.path.join(self.folder.name, "missing.csv")
        lines = self.load(missing)
        self.assertEqual(lines, [
            f"Products file not found: {missing}",
            "Load attempt finished.",
        ])
        self.assertEqual(self.inventory.get_products(), [])

    def test_invalid_price_and_stock_rows_are_skipped(self):
        with open(self.path, "w", newline="") as file:
            file.write("product_type,product_id,name,price,stock_quantity\n"
                       "physical,P001,Lamp,-4.00,10\n"
                       "physical,P002,Chair,20.00,-1\n"
                       "physical,P003,Stand,39.50,7\n")
        lines = self.load(self.path)
        self.assertEqual(len(self.inventory.get_products()), 1)
        self.assertIn("1 products loaded.", lines)


if __name__ == "__main__":
    unittest.main()
