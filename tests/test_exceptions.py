"""Тесты обработки нулевого остатка и результатов добавления товара."""

import pytest

from src import (
    Category,
    LawnGrass,
    Order,
    Product,
    Smartphone,
    ZeroQuantityError,
)

ZERO_QUANTITY_MESSAGE = "Товар с нулевым количеством не может быть добавлен"
SUCCESS_MESSAGE = "Товар успешно добавлен"
FINISHED_MESSAGE = "Обработка добавления товара завершена"


@pytest.mark.parametrize(
    ("product_class", "extra_args"),
    [
        (Product, ()),
        (Smartphone, (95.5, "A", 128, "Белый")),
        (LawnGrass, ("Россия", "7 дней", "Зеленый")),
    ],
)
def test_product_rejects_zero_quantity_before_creation_print(
    product_class: type[Product],
    extra_args: tuple[object, ...],
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(ValueError) as error:
        product_class("Товар", "Описание", 100.0, 0, *extra_args)

    assert type(error.value) is ValueError
    assert str(error.value) == ZERO_QUANTITY_MESSAGE
    captured = capsys.readouterr()
    assert captured.out == ""
    assert captured.err == ""
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_product_factory_rejects_zero_quantity(
    capsys: pytest.CaptureFixture[str],
) -> None:
    with pytest.raises(ValueError) as error:
        Product.new_product(
            {
                "name": "Товар",
                "description": "Описание",
                "price": 100.0,
                "quantity": 0,
            }
        )

    assert type(error.value) is ValueError
    assert str(error.value) == ZERO_QUANTITY_MESSAGE
    assert capsys.readouterr().out == ""


def test_zero_quantity_error_is_value_error_with_default_message() -> None:
    error = ZeroQuantityError()

    assert isinstance(error, ValueError)
    assert str(error) == ZERO_QUANTITY_MESSAGE


@pytest.mark.parametrize("destination", ["category", "order"])
def test_successful_addition_prints_success_then_completion(
    destination: str, capsys: pytest.CaptureFixture[str]
) -> None:
    product = Product("Товар", "Описание", 100.0, 3)
    category = Category("Категория", "Описание", [])
    original_attributes = vars(product).copy()
    capsys.readouterr()

    if destination == "category":
        category.add_product(product)
    else:
        Order(product, 2)

    assert capsys.readouterr().out == (
        f"{SUCCESS_MESSAGE}\n{FINISHED_MESSAGE}\n"
    )
    assert vars(product) == original_attributes
    assert list(category) == ([product] if destination == "category" else [])
    assert Category.category_count == 1
    assert Category.product_count == (1 if destination == "category" else 0)


@pytest.mark.parametrize("destination", ["category", "order"])
def test_zero_stock_addition_prints_error_and_reraises_without_changes(
    destination: str, capsys: pytest.CaptureFixture[str]
) -> None:
    product = Product("Товар", "Описание", 100.0, 3)
    product.quantity = 0
    existing_product = Product("Добавленный товар", "Описание", 50.0, 1)
    category = Category("Категория", "Описание", [existing_product])
    original_attributes = vars(product).copy()
    capsys.readouterr()

    with pytest.raises(ZeroQuantityError) as error:
        if destination == "category":
            category.add_product(product)
        else:
            Order(product, 2)

    assert str(error.value) == ZERO_QUANTITY_MESSAGE
    assert capsys.readouterr().out == (
        f"{ZERO_QUANTITY_MESSAGE}\n{FINISHED_MESSAGE}\n"
    )
    assert vars(product) == original_attributes
    assert list(category) == [existing_product]
    assert Category.category_count == 1
    assert Category.product_count == 1


@pytest.mark.parametrize("destination", ["category", "order"])
def test_invalid_product_still_raises_type_error_and_prints_completion(
    destination: str, capsys: pytest.CaptureFixture[str]
) -> None:
    category = Category("Категория", "Описание", [])

    with pytest.raises(TypeError):
        if destination == "category":
            category.add_product(object())
        else:
            Order(object(), 2)

    assert capsys.readouterr().out == f"{FINISHED_MESSAGE}\n"
    assert list(category) == []
    assert Category.category_count == 1
    assert Category.product_count == 0


@pytest.mark.parametrize(
    ("quantity", "expected_error"), [(0, ValueError), (True, TypeError)]
)
def test_invalid_order_quantity_precedes_zero_stock_check(
    quantity: object,
    expected_error: type[Exception],
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = Product("Товар", "Описание", 100.0, 3)
    product.quantity = 0
    original_attributes = vars(product).copy()
    capsys.readouterr()

    with pytest.raises(expected_error) as error:
        Order(product, quantity)

    assert type(error.value) is expected_error
    assert capsys.readouterr().out == f"{FINISHED_MESSAGE}\n"
    assert vars(product) == original_attributes
    assert Category.category_count == 0
    assert Category.product_count == 0
