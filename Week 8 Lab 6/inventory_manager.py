import json
import os
import math

from inventory import Inventory
from physical_product import PhysicalProduct
from digital_product import DigitalProduct

FILENAME = "inventory.json"

def load_inventory():
    inventory = Inventory()

    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r", encoding="utf-8") as file:
                saved_products = json.load(file)

            for item in saved_products:
                product_type = item.get("type", "physical")

                if product_type == "physical":
                    product = PhysicalProduct(
                        item["id"],
                        item["name"],
                        float(item["price"]),
                        int(item["stock"]),
                        float(item.get("weight", 0.0))
                    )

                elif product_type == "digital":
                    product = DigitalProduct(
                        item["id"],
                        item["name"],
                        float(item["price"]),
                        int(item["stock"]),
                        float(item["download_size"])
                    )

                else:
                    raise ValueError("Unknown product type")

                inventory.add_product(product)

            print("Inventory loaded successfully.")

        except (OSError, json.JSONDecodeError,
                ValueError, TypeError, KeyError):
            print("Error loading inventory.")
            inventory = Inventory()

    else:
        print("No inventory file found.")
        inventory.add_product(
            PhysicalProduct("P001", "Laptop", 1200, 15, 2.0)
        )
        inventory.add_product(
            DigitalProduct("D001", "eBook", 15, 50, 12.5)
        )

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


def add_product(inventory):
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

    if inventory.find_by_id(product_id) is not None:
        print("Product ID already exists!")
        return

    name = input("Product Name: ").strip()

    if not name:
        print("Product name cannot be empty.")
        return

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))

        if not math.isfinite(price) or price < 0 or stock < 0:
            print("Price and stock must be valid non-negative values.")
            return

        if product_type == "1": 
            weight = float(input("Weight (kg): "))

            if not math.isfinite(weight) or weight < 0:
                print("Weight must be a valid non-negative number.")
                return

            product = PhysicalProduct(
                product_id, name, price, stock, weight
            )

        else:
            download_size = float(input("Download Size (MB): "))

            if not math.isfinite(download_size) or download_size < 0:
                print("Download size must be a valid non-negative number.")
                return

            product = DigitalProduct(
                product_id, name, price, stock, download_size
            )

    except ValueError:
        print("Invalid input! Please enter valid numbers.")
        return

    if inventory.add_product(product):
        print("Product added successfully!")
    else:
        print("Product ID already exists!")

def update_stock(inventory):
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()
    product = inventory.find_by_id(product_id)

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

    inventory = load_inventory()

    while True:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")

        choice = input("Enter option: ").strip()
        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product(inventory)
        elif choice == "3":
            update_stock(inventory)
        elif choice == "4":
            search_product(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            save_inventory(inventory, is_exit=True)
            print("\nThank you for using Inventory Management System!")
            break
        else:
            print("Invalid option! Please enter a number between 1 and 6.")


if __name__ == "__main__":
    main()