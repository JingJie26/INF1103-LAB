from discount_strategy import DiscountStrategy, NoDiscount
from order_line import OrderLine
from product import Product


class Order:
    def __init__(self, order_id: str,
                 discount: DiscountStrategy | None = None):
        self.__order_id: str = order_id
        self.__order_lines: list[OrderLine] = []
        self.__discount: DiscountStrategy = (
            discount if discount is not None else NoDiscount()
        )

    def get_order_id(self) -> str:
        return self.__order_id

    def get_discount(self) -> DiscountStrategy:
        return self.__discount

    def set_discount(self, discount: DiscountStrategy) -> None:
        self.__discount = discount

    def add_order_line(self, product: Product, quantity: int) -> None:
        # OrderLine owns the quantity rule, so it validates itself.
        order_line = OrderLine(product, quantity)
        self.__order_lines.append(order_line)

    def remove_order_line(self, product_id: str) -> bool:
        for line in self.__order_lines:
            if line.get_product().get_product_id() == product_id:
                self.__order_lines.remove(line)
                return True
        return False

    def get_order_lines(self) -> list[OrderLine]:
        return self.__order_lines.copy()

    def calculate_subtotal(self) -> float:
        return sum(line.calculate_subtotal() for line in self.__order_lines)

    def calculate_total(self) -> float:
        total = self.calculate_subtotal()
        return self.__discount.apply(total)

    def display_information(self) -> None:
        print(f"Order {self.__order_id}")
        for line in self.__order_lines:
            line.display_information()
        print(f"Total: ${self.calculate_total():.2f}")
