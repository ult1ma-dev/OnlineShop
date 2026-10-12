"""Модели предметной области для товаров, категорий и заказов."""

from abc import ABC, abstractmethod
from collections.abc import Iterator
from types import NotImplementedType
from typing import ClassVar, Self, TypedDict


class ProductData(TypedDict):
    """Данные, необходимые для создания товара."""

    name: str
    description: str
    price: float
    quantity: int


class BaseProduct(ABC):
    """Общий интерфейс создания товара и работы с его ценой и остатком."""

    name: str
    description: str
    quantity: int

    @abstractmethod
    def __init__(self) -> None:
        """Продолжает цепочку инициализации родительских классов."""

        super().__init__()

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое описание товара."""

        ...

    @abstractmethod
    def __add__(self, other: object) -> float | NotImplementedType:
        """Возвращает общую стоимость остатков совместимых товаров."""

        ...

    @classmethod
    @abstractmethod
    def new_product(cls, product: ProductData) -> Self:
        """Создает товар на основе данных словаря."""

        ...

    @property
    @abstractmethod
    def price(self) -> float:
        """Возвращает цену товара."""

        ...

    @price.setter
    @abstractmethod
    def price(self, new_price: float) -> None:
        """Изменяет цену товара."""

        ...


class PrintMixin:
    """Печатает представление объекта после инициализации его полей."""

    _repr_fields: ClassVar[tuple[str, ...]] = ()

    def __init__(self) -> None:
        super().__init__()
        print(repr(self))

    def __repr__(self) -> str:
        """Возвращает имя класса и текущие значения параметров конструктора."""

        arguments = ", ".join(repr(getattr(self, field)) for field in self._repr_fields)
        return f"{type(self).__name__}({arguments})"


class Product(PrintMixin, BaseProduct):
    """Товар, доступный в магазине."""

    _repr_fields: ClassVar[tuple[str, ...]] = (
        "name",
        "description",
        "price",
        "quantity",
    )

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity
        super().__init__()

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

    _repr_fields: ClassVar[tuple[str, ...]] = Product._repr_fields + (
        "efficiency",
        "model",
        "memory",
        "color",
    )

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
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color
        super().__init__(name, description, price, quantity)


class LawnGrass(Product):
    """Газонная трава с указанием происхождения и срока прорастания."""

    _repr_fields: ClassVar[tuple[str, ...]] = Product._repr_fields + (
        "country",
        "germination_period",
        "color",
    )

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
        self.country = country
        self.germination_period = germination_period
        self.color = color
        super().__init__(name, description, price, quantity)


class BaseEntity(ABC):
    """Общие название, описание и строковое представление сущностей магазина."""

    def __init__(self, name: str, description: str) -> None:
        self.name = name
        self.description = description
        super().__init__()

    @abstractmethod
    def __str__(self) -> str:
        """Возвращает строковое описание сущности."""

        ...


class Category(BaseEntity):
    """Категория, объединяющая товары магазина."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(
        self, name: str, description: str, products: list[Product]
    ) -> None:
        super().__init__(name, description)
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


class Order(BaseEntity):
    """Покупка одного товара с количеством и стоимостью на момент создания."""

    def __init__(self, product: Product, quantity: int) -> None:
        if not isinstance(product, Product):
            raise TypeError("В заказе должен быть один товар или его наследник")
        if type(quantity) is not int:
            raise TypeError("Количество в заказе должно быть целым числом")
        if quantity <= 0:
            raise ValueError("Количество в заказе должно быть положительным")

        super().__init__(product.name, product.description)
        self.product = product
        self.quantity = quantity
        self.total_cost = product.price * quantity

    def __str__(self) -> str:
        """Возвращает название товара, купленное количество и стоимость."""

        return (
            f"{self.name}, количество: {self.quantity} шт. "
            f"Итоговая стоимость: {self.total_cost} руб."
        )


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
