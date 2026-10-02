import json
import os

FILENAME = "inventory.json"

# DATA PERSISTENCE FUNCTIONS

def load_inventory():
    """Loads inventory from inventory.json if it exists, otherwise returns an empty list."""
    if os.path.exists(FILENAME):
        try:
            with open(FILENAME, "r") as file:
                inventory = json.load(file)
                print(f"\n{FILENAME} found.\nInventory loaded successfully.\n")
                return inventory
        except (json.JSONDecodeError, IOError):
            print(f"\nError loading {FILENAME}. Starting with an empty inventory.\n")
            return []
    else:
        print(f"\n{FILENAME} not found. Starting with an empty inventory.\n")
        return []


def save_inventory(inventory, is_exit=False):
    """Saves the current inventory list to inventory.json."""
    if is_exit:
        print("\nSaving inventory before exit...")
    else:
        print("\nSaving inventory...")
        
    try:
        with open(FILENAME, "w") as file:
            json.dump(inventory, file, indent=4)
        
        if is_exit:
            print("Inventory saved successfully.")
        else:
            print(f"Inventory saved successfully to {FILENAME}.")
    except IOError:
        print("\nFailed to save inventory to file.")

# INVENTORY MANIPULATION FUNCTIONS

def display_all(inventory):
    """Displays all products formatted in a list."""
    print("\nCurrent Inventory")
    print("-" * 48)
    if not inventory:
        print("No products available in inventory.")
    else:
        for item in inventory:
            print(
                f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['stock']}"
            )
    print("-" * 48)


def add_product(inventory):
    """Prompts user for product details and appends a new dictionary to the list."""
    print("\nAdd New Product")
    product_id = input("Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == product_id.lower():
            print(f"Error: Product ID '{product_id}' already exists!")
            return

    name = input("Product Name: ").strip()

    try:
        price = float(input("Price: "))
        stock = int(input("Stock Quantity: "))
    except ValueError:
        print("Invalid input! Price must be a number and stock must be an integer.")
        return

    product = {
        "id": product_id,
        "name": name,
        "price": price,
        "stock": stock
    }

    inventory.append(product)
    print("Product added successfully!")


def update_stock(inventory):
    """Updates the stock quantity for an existing product matching sample output 2."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ").strip()

    for item in inventory:
        if item["id"].lower() == product_id.lower():
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['stock']}")
            
            try:
                new_stock = int(input("New Stock Quantity: "))
                item["stock"] = new_stock
                print("Stock updated successfully!")
                return
            except ValueError:
                print("Invalid input! Stock quantity must be an integer.")
                return

    print("Product not found.")


def search_product(inventory):
    """Searches for a product by ID or Name matching sample output 2."""
    print("\nSearch Product")
    query = input("Enter Product ID or Name: ").strip().lower()

    found = False
    for item in inventory:
        if query == item["id"].lower() or query in item["name"].lower():
            print("Product Found")
            print("-" * 48)
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['stock']}")
            print("-" * 48)
            found = True

    if not found:
        print("Product not found.")

# MENU SYSTEM

def main():
    print("========================================")
    print("INVENTORY MANAGEMENT SYSTEM")
    print("========================================")

    inventory = load_inventory()

    if not inventory:
        inventory = [
            {"id": "P001", "name": "Laptop", "price": 1200.00, "stock": 15},
            {"id": "P002", "name": "Mouse", "price": 25.50, "stock": 40},
            {"id": "P003", "name": "Keyboard", "price": 45.00, "stock": 25},
        ]
        save_inventory(inventory)

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
            display_all(inventory)
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