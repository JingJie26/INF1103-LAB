from abc import ABC, abstractmethod


class DiscountStrategy(ABC):
    @abstractmethod
    def apply(self, total: float) -> float:
        pass


class NoDiscount(DiscountStrategy):
    def apply(self, total: float) -> float:
        return total


class PercentageDiscount(DiscountStrategy):
    def __init__(self, percentage: float):
        if percentage < 0 or percentage > 100:
            raise ValueError("Percentage must be between 0 and 100.")
        self.__percentage: float = percentage

    def get_percentage(self) -> float:
        return self.__percentage

    def apply(self, total: float) -> float:
        return total * (100 - self.__percentage) / 100


class BulkDiscount(DiscountStrategy):
    def __init__(self, threshold: float, amount: float):
        if threshold < 0 or amount < 0:
            raise ValueError("Threshold and amount cannot be negative.")
        if amount > threshold:
            raise ValueError("Amount cannot be more than the threshold.")
        self.__threshold: float = threshold
        self.__amount: float = amount

    def apply(self, total: float) -> float:
        if total >= self.__threshold:
            return total - self.__amount
        return total


# Section 2.4: a fourth strategy, added without touching Order.
class StudentDiscount(DiscountStrategy):
    STUDENT_RATE: float = 5

    def apply(self, total: float) -> float:
        return total * (100 - self.STUDENT_RATE) / 100
