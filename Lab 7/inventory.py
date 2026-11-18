class Inventory:
    def __init__(self):
        self.__products = []

    def add_product(self, product):
        if self.find_by_id(product.get_product_id()) is not None:
            return False
        self.__products.append(product)
        return True

    def find_by_id(self, product_id):
        for product in self.__products:
            if product.get_product_id().lower() == product_id.lower():
                return product
        return None

    def search_product(self, query):
        query = query.lower()
        matches = []
        for product in self.__products:
            if (query == product.get_product_id().lower()
                    or query in product.get_name().lower()):
                matches.append(product)
        return matches

    def display_all(self):
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

    def get_products(self):
        return self.__products.copy()
