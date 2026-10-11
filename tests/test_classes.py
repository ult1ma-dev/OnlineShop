"""Тесты моделей товаров и категорий."""

import pytest

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


@pytest.mark.parametrize("creation_method", ["constructor", "new_product"])
def test_product_price_is_private(creation_method: str) -> None:
    if creation_method == "constructor":
        product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    else:
        product = Product.new_product(
            {
                "name": "Iphone 15",
                "description": "512GB, Gray space",
                "price": 210000.0,
                "quantity": 8,
            }
        )

    assert vars(product)["_Product__price"] == 210000.0
    assert "price" not in vars(product)
    assert "_price" not in vars(product)
    assert isinstance(Product.price, property)
    assert product.price == 210000.0
    with pytest.raises(AttributeError):
        getattr(product, "__price")


def test_category_initialization() -> None:
    products = [
        Product("Iphone 15", "512GB, Gray space", 210000.0, 8),
        Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14),
    ]

    category = Category("Смартфоны", "Мобильные устройства", products)

    assert category.name == "Смартфоны"
    assert category.description == "Мобильные устройства"
    assert category.products == (
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        "Xiaomi Redmi Note 11, 31000.0 руб. Остаток: 14 шт.\n"
    )
    assert not hasattr(category, "__products")


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


def test_new_product() -> None:
    product = Product.new_product(
        {
            "name": "Iphone 15",
            "description": "512GB, Gray space",
            "price": 210000.0,
            "quantity": 8,
        }
    )

    assert isinstance(product, Product)
    assert product.name == "Iphone 15"
    assert product.description == "512GB, Gray space"
    assert product.price == 210000.0
    assert product.quantity == 8


def test_price_setter_updates_positive_price() -> None:
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    product.price = 200000.0

    assert product.price == 200000.0
    assert vars(product)["_Product__price"] == 200000.0
    assert "price" not in vars(product)
    assert "_price" not in vars(product)


@pytest.mark.parametrize("new_price", [0, -100.0])
def test_price_setter_rejects_nonpositive_price(
    new_price: float, capsys: pytest.CaptureFixture[str]
) -> None:
    product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    original_attributes = vars(product).copy()

    product.price = new_price

    assert product.price == 210000.0
    assert vars(product) == original_attributes
    assert capsys.readouterr().out == "Цена не должна быть нулевая или отрицательная\n"


def test_products_property_has_no_setter() -> None:
    category = Category("Аксессуары", "Дополнительные товары", [])

    with pytest.raises(AttributeError):
        setattr(category, "products", "")


def test_empty_category_products_getter() -> None:
    category = Category("Аксессуары", "Дополнительные товары", [])

    assert category.products == ""


def test_add_product() -> None:
    first_product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    added_product = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category = Category("Техника", "Техника для дома", [first_product])

    category.add_product(added_product)

    assert category.products == (
        "Iphone 15, 210000.0 руб. Остаток: 8 шт.\n"
        '55" QLED 4K, 123000.0 руб. Остаток: 7 шт.\n'
    )
    assert Category.product_count == 2
