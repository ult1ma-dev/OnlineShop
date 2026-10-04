"""Тесты строковых представлений и сложения товаров."""

import pytest

from src.classes import Category, Product


@pytest.mark.parametrize(
    ("price", "quantity", "expected"),
    [
        (80, 15, "Телефон, 80 руб. Остаток: 15 шт."),
        (80.5, 15, "Телефон, 80.5 руб. Остаток: 15 шт."),
        (80.0, 0, "Телефон, 80.0 руб. Остаток: 0 шт."),
    ],
)
def test_product_str(price: float, quantity: int, expected: str) -> None:
    product = Product("Телефон", "Описание", price, quantity)

    assert str(product) == expected


def test_product_str_uses_current_price_and_quantity() -> None:
    product = Product("Телефон", "Описание", 80.0, 15)

    product.price = 120.5
    product.quantity = 3

    assert str(product) == "Телефон, 120.5 руб. Остаток: 3 шт."


def test_category_str_sums_stock_quantities() -> None:
    category = Category(
        "Смартфоны",
        "Описание",
        [
            Product("Samsung", "Описание", 180000.0, 5),
            Product("Iphone", "Описание", 210000.0, 8),
            Product("Xiaomi", "Описание", 31000.0, 14),
        ],
    )

    assert str(category) == "Смартфоны, количество продуктов: 27 шт."
    assert Category.product_count == 3


def test_empty_category_str() -> None:
    category = Category("Аксессуары", "Описание", [])

    assert str(category) == "Аксессуары, количество продуктов: 0 шт."


def test_category_str_updates_after_stock_change_and_addition() -> None:
    product = Product("Телефон", "Описание", 100.0, 10)
    category = Category("Техника", "Описание", [product])

    assert str(category) == "Техника, количество продуктов: 10 шт."
    product.quantity = 4
    assert str(category) == "Техника, количество продуктов: 4 шт."
    category.add_product(Product("Чехол", "Описание", 200.0, 2))
    assert str(category) == "Техника, количество продуктов: 6 шт."
    assert Category.product_count == 2


def test_category_products_uses_product_str() -> None:
    class CustomProduct(Product):
        def __str__(self) -> str:
            return "Особый товар"

    category = Category(
        "Техника", "Описание", [CustomProduct("Телефон", "Описание", 100.0, 10)]
    )

    assert category.products == "Особый товар\n"


@pytest.mark.parametrize(
    ("first_price", "first_quantity", "second_price", "second_quantity", "expected"),
    [
        (100.0, 10, 200.0, 2, 1400.0),
        (125.5, 3, 25.25, 2, 427.0),
        (0.1, 3, 0.2, 2, 0.7),
        (100.0, 0, 200.0, 2, 400.0),
        (100.0, 0, 200.0, 0, 0.0),
    ],
)
def test_product_add(
    first_price: float,
    first_quantity: int,
    second_price: float,
    second_quantity: int,
    expected: float,
) -> None:
    first_product = Product("Телефон", "Описание", first_price, first_quantity)
    second_product = Product("Чехол", "Описание", second_price, second_quantity)
    first_attributes = vars(first_product).copy()
    second_attributes = vars(second_product).copy()

    assert first_product + second_product == pytest.approx(expected)
    assert second_product + first_product == pytest.approx(expected)
    assert vars(first_product) == first_attributes
    assert vars(second_product) == second_attributes


def test_product_add_uses_current_price_and_quantity() -> None:
    first_product = Product("Телефон", "Описание", 100.0, 10)
    second_product = Product("Чехол", "Описание", 200.0, 2)

    first_product.price = 150.0
    second_product.quantity = 3

    assert first_product + second_product == 2100.0


@pytest.mark.parametrize("other", [100, "товар", None])
def test_product_add_rejects_unsupported_operand(other: object) -> None:
    product = Product("Телефон", "Описание", 100.0, 10)

    assert product.__add__(other) is NotImplemented
    with pytest.raises(TypeError):
        product + other
