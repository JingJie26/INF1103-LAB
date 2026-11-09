from supplier import Supplier
from product import Product
from physical_product import PhysicalProduct
from digital_product import DigitalProduct
from inventory import Inventory
from order import Order


def section(title: str) -> None:
    print(f"\n{'=' * 10} {title} {'=' * 10}")


def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())


section("2. Association")
supplier = Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com")
laptop = PhysicalProduct("P001", "Laptop", 1200.0, 15, supplier, 2.0)
ebook = DigitalProduct("D001", "eBook", 15.0, 50, supplier, 12.5)
laptop.get_supplier().display_information()
ebook.get_supplier().display_information()
print("Same Supplier object?", laptop.get_supplier() is ebook.get_supplier())
del supplier
print("After del supplier:")
laptop.get_supplier().display_information()
ebook.get_supplier().display_information()

section("3. Aggregation")
inv_a = Inventory()
inv_b = Inventory()
inv_a.add_product(laptop)
inv_a.add_product(ebook)
inv_a.remove_product("P001")
print("P001 in A after removal?", inv_a.find_product("P001"))
print("Laptop still works:", laptop.get_name(), "| stock", laptop.get_stock())
inv_b.add_product(laptop)
print("Same laptop object in B?", inv_b.find_product("P001") is laptop)
inv_a.remove_product("D001")
inv_b.add_product(ebook)

section("4. Composition")
order1 = Order("O001")
order1.add_order_line(laptop, 1)
order1.add_order_line(ebook, 2)
order1.display_information()
order2 = Order("O002")
order2.add_order_line(laptop, 3)
line1 = order1.get_order_lines()[0]
line2 = order2.get_order_lines()[0]
print("Same Product object in both orders?",
      line1.get_product() is line2.get_product())
print("Same OrderLine object in both orders?", line1 is line2)
order1.remove_order_line("D001")
print("After removing eBook line, order 1 total:", order1.calculate_total())

section("6/7. LSP and polymorphism")
show_product_details(laptop)
show_product_details(ebook)
for product in inv_b.get_products():
    product.display_information()
    print(product.get_fulfilment_info())
    product.update_stock(10)
    print("Stock after update:", product.get_stock())
