"""Модели предметной области для товаров и категорий."""

from collections.abc import Iterator
from types import NotImplementedType
from typing import ClassVar, Self, TypedDict


class ProductData(TypedDict):
    """Данные, необходимые для создания товара."""

    name: str
    description: str
    price: float
    quantity: int


class Product:
    """Товар, доступный в магазине."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    def __str__(self) -> str:
        """Возвращает название, цену и остаток товара."""

        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: object) -> float | NotImplementedType:
        """Возвращает стоимость остатков двух товаров одинакового класса."""

        if not isinstance(other, Product):
            return NotImplemented
        if type(self) is not type(other):
            raise TypeError(
                "Можно складывать только товары одинакового класса"
            )
        return self.price * self.quantity + other.price * other.quantity

    @classmethod
    def new_product(cls, product: ProductData) -> Self:
        """Создает товар на основе данных словаря."""

        return cls(
            name=product["name"],
            description=product["description"],
            price=product["price"],
            quantity=product["quantity"],
        )

    @property
    def price(self) -> float:
        """Возвращает цену товара."""

        return self.__price

    @price.setter
    def price(self, new_price: float) -> None:
        """Устанавливает положительную цену товара."""

        if new_price <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            self.__price = new_price


class Smartphone(Product):
    """Смартфон с характеристиками производительности и памяти."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: float,
        model: str,
        memory: int,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color


class LawnGrass(Product):
    """Газонная трава с указанием происхождения и срока прорастания."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color


class Category:
    """Категория, объединяющая товары магазина."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(
        self, name: str, description: str, products: list[Product]
    ) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def __str__(self) -> str:
        """Возвращает название категории и суммарный остаток товаров."""

        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> Iterator[Product]:
        """Возвращает итератор товаров категории."""

        return iter(self.__products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар или его наследника, отклоняя посторонние объекты."""

        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только товары")
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает товары категории в формате строки."""

        return "".join(f"{product}\n" for product in self.__products)


class CategoryIterator(Iterator[Product]):
    """Перебирает товары переданной категории в порядке добавления."""

    def __init__(self, category: Category) -> None:
        self._products = iter(category)

    def __iter__(self) -> Self:
        """Возвращает текущий итератор без сброса позиции."""

        return self

    def __next__(self) -> Product:
        """Возвращает очередной товар или завершает перебор."""

        return next(self._products)
