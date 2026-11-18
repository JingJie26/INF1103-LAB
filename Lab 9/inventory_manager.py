import json
import math

from input_helpers import get_positive_float
from inventory import Inventory
from product_factory import ProductFactory
from product_loader import load_products
from supplier import Supplier

FILENAME = "inventory.json"
PRODUCTS_CSV = "products.csv"
PRODUCT_TYPES = {"1": "physical", "2": "digital"}


def create_suppliers() -> dict[str, Supplier]:
    return {
        "S001": Supplier("S001", "TechSource Pte Ltd", "sales@techsource.com"),
        "S002": Supplier("S002", "DigiWorks", "hello@digiworks.com"),
    }


def load_inventory(suppliers: dict[str, Supplier]) -> Inventory:
    inventory = Inventory()

    try:
        file = open(FILENAME, "r", encoding="utf-8")
    except FileNotFoundError:
        print("No inventory file found.")
        inventory.add_product(ProductFactory.create(
            "physical", "P001", "Laptop", 1200, 15, suppliers["S001"],
            weight=2.0))
        inventory.add_product(ProductFactory.create(
            "digital", "D001", "eBook", 15, 50, suppliers["S002"],
            download_size=12.5))
        return inventory

    try:
        with file:
            saved_products = json.load(file)
    except json.JSONDecodeError:
        print("Inventory file is not valid JSON. Starting with an empty "
              "inventory.")
        return inventory

    for item in saved_products:
        # One bad record is reported and skipped; the rest still load.
        try:
            supplier = suppliers[item.get("supplier_id", "S001")]
            product = ProductFactory.create(
                item.get("type", "physical"),
                item["id"],
                item["name"],
                float(item["price"]),
                int(item["stock"]),
                supplier,
                weight=float(item.get("weight", 0.0)),
                download_size=float(item.get("download_size", 0.0)),
            )
            inventory.add_product(product)
        except ValueError as error:
            print(f"Skipped saved product: {error}")
        except KeyError as error:
            print(f"Skipped saved product: missing or unknown {error}")

    print("Inventory loaded successfully.")
    return inventory


def save_inventory(inventory, is_exit=False):
    if is_exit:
        print("\nSaving inventory before exit...")
    else:
        print("\nSaving inventory...")

    data = [product.to_dict() for product in inventory.get_products()]
    try:
        with open(FILENAME, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)
        print(f"Inventory saved successfully to {FILENAME}.")
    except OSError:
        print("\nFailed to save inventory to file.")


def add_product(inventory, suppliers):
    print("\nAdd New Product")
    print("1. Physical Product")
    print("2. Digital Product")

    product_type = input("Select Product Type (1 or 2): ").strip()

    if product_type not in ("1", "2"):
        print("Invalid product type!")
        return

    product_id = input("Product ID: ").strip()

    if not product_id:
        print("Product ID cannot be empty.")
        return

    if inventory.find_product(product_id) is not None:
        print("Product ID already exists!")
        return

    name = input("Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    supplier_id = input(f"Supplier ID ({', '.join(suppliers)}): ").strip().upper()
    supplier = suppliers.get(supplier_id)

    if supplier is None:
        print("Supplier not found.")
        return

    price = get_positive_float("Price: ")

    try:
        stock = int(input("Stock Quantity: "))
        weight = 0.0
        download_size = 0.0

        if product_type == "1":
            weight = float(input("Weight (kg): "))

            if not math.isfinite(weight) or weight < 0:
                print("Weight must be a valid non-negative number.")
                return

        else:
            download_size = float(input("Download Size (MB): "))

            if not math.isfinite(download_size) or download_size < 0:
                print("Download size must be a valid non-negative number.")
                return

    except ValueError:
        print("Invalid input! Please enter valid numbers.")
        return

    try:
        product = ProductFactory.create(
            PRODUCT_TYPES[product_type], product_id, name, price, stock,
            supplier, weight=weight, download_size=download_size
        )
    except ValueError as error:
        print(f"Product not added: {error}")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product ID already exists!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_product(product_id)

    if product is None:
        print("Product not found.")
        return

    print("\nProduct Found:")
    print(f"Name: {product.get_name()}")
    print(f"Current Stock: {product.get_stock()}")

    try:
        new_stock = int(input("New Stock Quantity: "))
        product.update_stock(new_stock)
    except ValueError:
        print("Invalid input! Stock quantity must be a non-negative integer.")
        return
    print("Stock updated successfully!")


def search_product(inventory):
    print("\nSearch Product")
    query = input("Enter Product ID or Name: ").strip()
    matches = inventory.search_product(query)

    if not matches:
        print("Product not found.")
        return

    for product in matches:
        print("Product Found")
        print("-" * 48)
        product.display_information()
        print("-" * 48)


def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    suppliers = create_suppliers()
    inventory = load_inventory(suppliers)

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Load Products from CSV")
        print("6. Save Inventory")
        print("7. Exit")
        print("----------------------------")

        choice = input("Enter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory, suppliers)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            load_products(PRODUCTS_CSV, inventory, suppliers["S001"])
        elif choice == "6":
            save_inventory(inventory)
        elif choice == "7":
            save_inventory(inventory, is_exit=True)
            print("\nThank you for using Inventory Management System!")
            break
        else:
            print("Invalid option! Please enter a number between 1 and 7.")


if __name__ == "__main__":
    main()
