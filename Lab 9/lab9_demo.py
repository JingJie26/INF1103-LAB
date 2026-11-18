"""Lab 9 demo: run this to check the 'Predict first' answers."""
from discount_strategy import (BulkDiscount, NoDiscount, PercentageDiscount,
                               StudentDiscount)
from input_helpers import get_positive_float
from inventory import Inventory
from order import Order
from product import Product
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier


def section(title: str) -> None:
    print(f"\n{'=' * 10} {title} {'=' * 10}")


supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")

section("2.3 Strategy: order lines add up to 250")
desk: Product = ProductFactory.create(
    "physical", "P010", "Desk", 100.0, 20, supplier, weight=12.0)
course: Product = ProductFactory.create(
    "digital", "D010", "Python Course", 50.0, 999, supplier,
    download_size=800.0)
order = Order("O001", BulkDiscount(200, 20))
order.add_order_line(desk, 2)
order.add_order_line(course, 1)
print("Subtotal:", order.calculate_subtotal())
print("BulkDiscount(200, 20):", order.calculate_total())
order.set_discount(PercentageDiscount(10))
print("After set_discount(PercentageDiscount(10)):", order.calculate_total())

section("2.4 Extend without modifying Order")
order.set_discount(StudentDiscount())
print("StudentDiscount():", order.calculate_total())
default_order = Order("O002")
default_order.add_order_line(desk, 1)
print("Default strategy:", type(default_order.get_discount()).__name__,
      "->", default_order.calculate_total())
shared = PercentageDiscount(10)
order_a = Order("O003", shared)
order_b = Order("O004", shared)
print("Two orders share one strategy object?",
      order_a.get_discount() is order_b.get_discount())

section("3.2 Factory: unknown product type")
try:
    ProductFactory.create("service", "S001", "Installation", 30.0, 5, supplier)
except ValueError as error:
    print("ValueError:", error)

section("4. Validation")
checks = [
    ("price 0", lambda: ProductFactory.create(
        "physical", "P011", "Free Pen", 0, 5, supplier)),
    ("stock -1", lambda: ProductFactory.create(
        "digital", "D011", "Font Pack", 9.9, -1, supplier)),
    ("digital update_stock(-5)", lambda: course.update_stock(-5)),
    ("order quantity 0", lambda: order.add_order_line(desk, 0)),
]
for label, action in checks:
    try:
        action()
    except ValueError as error:
        print(f"{label}: ValueError: {error}")

section("5.2 load_products('products.csv')")
inventory = Inventory()
load_products("products.csv", inventory, supplier)
for product in inventory.get_products():
    print("-", product.get_product_id(), product.get_name(),
          "|", product.get_fulfilment_info())

section("5.2 load_products('missing.csv')")
load_products("missing.csv", Inventory(), supplier)

section("5.1 get_positive_float (try: abc, then -5, then 12.50)")
try:
    price = get_positive_float("Enter a price: ")
    print("Returned:", price)
except EOFError:
    print("\nNo keyboard input available, skipped.")
