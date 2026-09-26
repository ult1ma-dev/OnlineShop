"""Domain models for products and categories."""

from typing import ClassVar


class Product:
    """A product available in the store."""

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """A category that groups store products."""

    category_count: ClassVar[int] = 0
    product_count: ClassVar[int] = 0

    def __init__(self, name: str, description: str, products: list[Product]) -> None:
        self.name = name
        self.description = description
        self.products = products

        Category.category_count += 1
        Category.product_count += len(products)
