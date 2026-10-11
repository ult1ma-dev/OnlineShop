"""Модели предметной области для товаров и категорий."""

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


class Category:
    """Категория, объединяющая товары магазина."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.__products = products

        Category.category_count += 1
        Category.product_count += len(products)

    def add_product(self, product: Product) -> None:
        """Добавляет товар в категорию."""

        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> str:
        """Возвращает товары категории в формате строки."""

        products = ""
        for product in self.__products:
            products += (
                f"{product.name}, {product.price} руб. "
                f"Остаток: {product.quantity} шт.\n"
            )
        return products
