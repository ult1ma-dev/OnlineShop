"""Utilities for creating store entities from external data."""

import json
from pathlib import Path
from typing import TypedDict

from src.classes import Category, Product


class ProductData(TypedDict):
    """Expected JSON representation of a product."""

    name: str
    description: str
    price: float
    quantity: int


class CategoryData(TypedDict):
    """Expected JSON representation of a category."""

    name: str
    description: str
    products: list[ProductData]


def load_categories_from_json(file_path: str | Path) -> list[Category]:
    """Read categories from a UTF-8 JSON file and create domain objects."""

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
