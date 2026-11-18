from product import Product


class Inventory:
    def __init__(self) -> None:
        self.__products: list[Product] = []

    def add_product(self, product: Product) -> bool:
        if self.find_product(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def remove_product(self, product_id: str) -> bool:
        product = self.find_product(product_id)
        if product is None:
            return False
        self.__products.remove(product)
        return True

    def find_product(self, product_id: str) -> Product | None:
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, query: str) -> list[Product]:
        query = query.lower()
        matches: list[Product] = []
        for product in self.__products:
            if (query == product.get_product_id().lower()
                    or query in product.get_name().lower()):
                matches.append(product)
        return matches

    def display_all(self) -> None:
        print("\nCurrent Inventory")
        print("-" * 48)
        if not self.__products:
            print("No products available in inventory.")
        else:
            for product in self.__products:
                product.display_information()
                print("-" * 48)
        if not self.__products:
            print("-" * 48)

    def get_products(self) -> list[Product]:
        return self.__products.copy()
