"""Тесты среднего ценника товаров категории."""

import pytest

from src import Category, LawnGrass, Product, Smartphone


def test_middle_price_uses_prices_without_stock_weights() -> None:
    category = Category(
        "Техника",
        "Описание",
        [
            Product("Телефон", "Описание", 100.0, 1),
            Product("Чехол", "Описание", 300.0, 100),
        ],
    )

    assert category.middle_price() == 200.0


def test_middle_price_of_empty_category_is_zero() -> None:
    category = Category("Пустая категория", "Описание", [])

    assert category.middle_price() == 0


def test_middle_price_of_one_product_is_its_price() -> None:
    category = Category(
        "Техника", "Описание", [Product("Товар", "Описание", 125.5, 3)]
    )

    assert category.middle_price() == 125.5


def test_middle_price_uses_local_product_count() -> None:
    first_category = Category(
        "Техника", "Описание", [Product("Товар", "Описание", 125.5, 3)]
    )
    Category(
        "Другая категория",
        "Описание",
        [
            Product("Другой товар", "Описание", 1000.0, 1),
            Product("Еще один товар", "Описание", 2000.0, 2),
        ],
    )

    assert Category.product_count == 3
    assert first_category.middle_price() == 125.5


def test_middle_price_updates_after_price_change_and_addition() -> None:
    first_product = Product("Телефон", "Описание", 100.0, 3)
    category = Category("Техника", "Описание", [first_product])

    first_product.price = 250.0

    assert category.middle_price() == 250.0

    category.add_product(Product("Чехол", "Описание", 101.0, 2))

    assert category.middle_price() == 175.5


def test_middle_price_accepts_product_subclasses_without_rounding() -> None:
    category = Category(
        "Разные товары",
        "Описание",
        [
            Product("Товар", "Описание", 1.0, 1),
            Smartphone("Телефон", "Описание", 1.0, 2, 95.5, "A", 128, "Белый"),
            LawnGrass(
                "Трава", "Описание", 2.0, 3, "Россия", "7 дней", "Зеленый"
            ),
        ],
    )

    assert category.middle_price() == pytest.approx(4.0 / 3)


def test_middle_price_keeps_products_and_counters_unchanged() -> None:
    product = Product("Товар", "Описание", 125.5, 3)
    category = Category("Техника", "Описание", [product])
    original_attributes = vars(product).copy()

    assert category.middle_price() == 125.5
    assert category.middle_price() == 125.5
    assert list(category) == [product]
    assert vars(product) == original_attributes
    assert Category.category_count == 1
    assert Category.product_count == 1
