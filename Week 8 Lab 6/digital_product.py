from product import Product

class DigitalProduct(Product):

    def __init__(self, product_id, name, price, stock, download_size):
        super().__init__(product_id, name, price, stock)
        self.__download_size = download_size

    def get_download_size(self):
        return self.__download_size

    def display_information(self):
        super().display_information()
        print("Type: Digital")
        print(f"Download Size: {self.__download_size} MB")
        print(self.get_fulfilment_info())

    def get_fulfilment_info(self):
        return "Fulfilment: Delivered via digital download."

    def to_dict(self):
        data = super().to_dict()
        data["type"] = "digital"
        data["download_size"] = self.__download_size
        return data
