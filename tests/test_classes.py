"""Tests for product and category models."""

from src.classes import Category, Product


def test_product_initialization() -> None:
    product = Product(
        "Samsung Galaxy C23 Ultra",
        "256GB, Серый цвет, 200MP камера",
        180000.50,
        5,
    )

    assert product.name == "Samsung Galaxy C23 Ultra"
    assert product.description == "256GB, Серый цвет, 200MP камера"
    assert product.price == 180000.50
    assert product.quantity == 5


def test_category_initialization() -> None:
    products = [
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]

    category = Category("Смартфоны", "Мобильные устройства", products)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные устройства"
    assert category.products is products
    assert category.products[0].name == "Iphone 15"


def test_category_and_product_counters() -> None:
    smartphones = [
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]
    televisions = [Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)]

    first_category = Category("Смартфоны", "Мобильные устройства", smartphones)
    Category("Телевизоры", "Техника для дома", televisions)
    Category("Аксессуары", "Дополнительные товары", [])

    assert Category.category_count == 3
    assert first_category.category_count == 3
    assert Category.product_count == 3
    assert first_category.product_count == 3
