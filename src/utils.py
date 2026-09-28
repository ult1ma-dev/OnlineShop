"""Функции для создания объектов магазина из внешних данных."""

import json
from pathlib import Path
from typing import TypedDict

from src.classes import Category, Product


class ProductData(TypedDict):
    """Ожидаемое представление товара в JSON."""

    name: str
    description: str
    price: float
    quantity: int


class CategoryData(TypedDict):
    """Ожидаемое представление категории в JSON."""

    name: str
    description: str
    products: list[ProductData]


def load_categories_from_json(file_path: str | Path) -> list[Category]:
    """Загружает категории из JSON-файла в кодировке UTF-8."""

    with Path(file_path).open(encoding="utf-8") as file:
        categories_data: list[CategoryData] = json.load(file)

    categories = []
    for category_data in categories_data:
        products = [
            Product(
                name=product_data["name"],
                description=product_data["description"],
                price=product_data["price"],
                quantity=product_data["quantity"],
            )
            for product_data in category_data["products"]
        ]
        categories.append(
            Category(
                name=category_data["name"],
                description=category_data["description"],
                products=products,
            )
        )

    return categories


read_json = load_categories_from_json
