import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier


def load_products(path: str, inventory: Inventory, supplier: Supplier) -> None:
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        loaded = 0
        with file:
            reader = csv.reader(file)
            next(reader, None)  # skip the header row
            for row_number, row in enumerate(reader, start=2):
                try:
                    if len(row) != 5:
                        raise ValueError("expected 5 columns")
                    product_type, product_id, name, price, stock = row
                    product = ProductFactory.create(
                        product_type, product_id, name,
                        float(price), int(stock), supplier
                    )
                    if not inventory.add_product(product):
                        raise ValueError(
                            f"duplicate product ID: {product_id}")
                except ValueError as error:
                    print(f"Skipped row {row_number} {row}: {error}")
                    continue
                loaded += 1
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")
