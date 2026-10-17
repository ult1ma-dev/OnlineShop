"""Тесты абстрактного интерфейса товара и миксина печати."""

from inspect import isabstract

import pytest

from src import (
    BaseEntity,
    BaseProduct,
    LawnGrass,
    PrintMixin,
    Product,
    Smartphone,
)


class IncompleteProduct(BaseProduct):
    """Наследник, который не реализует обязательные операции товара."""


class NamedProduct(Product):
    """Дополнительный наследник для проверки фактического имени класса."""


@pytest.mark.parametrize("abstract_class", [BaseProduct, IncompleteProduct])
def test_abstract_product_cannot_be_created(
    abstract_class: type[BaseProduct],
) -> None:
    with pytest.raises(TypeError, match="abstract"):
        abstract_class()


def test_base_product_declares_common_operations() -> None:
    assert {
        "__init__",
        "__str__",
        "__add__",
        "new_product",
        "price",
    } <= BaseProduct.__abstractmethods__


@pytest.mark.parametrize("product_class", [Product, Smartphone, LawnGrass])
def test_product_classes_are_concrete(product_class: type[Product]) -> None:
    assert issubclass(product_class, BaseProduct)
    assert issubclass(product_class, PrintMixin)
    assert not isabstract(product_class)


@pytest.mark.parametrize("product_class", [Smartphone, LawnGrass])
def test_specialized_products_inherit_only_product(
    product_class: type[Product],
) -> None:
    assert product_class.__bases__ == (Product,)


@pytest.mark.parametrize(
    ("product_class", "extra_args", "expected"),
    [
        (Product, (), "Product('Товар', 'Описание', 100.0, 3)"),
        (
            Smartphone,
            (95.5, "Model A", 128, "Белый"),
            "Smartphone('Товар', 'Описание', 100.0, 3, "
            "95.5, 'Model A', 128, 'Белый')",
        ),
        (
            LawnGrass,
            ("Россия", "7 дней", "Зеленый"),
            "LawnGrass('Товар', 'Описание', 100.0, 3, "
            "'Россия', '7 дней', 'Зеленый')",
        ),
        (NamedProduct, (), "NamedProduct('Товар', 'Описание', 100.0, 3)"),
    ],
)
def test_creation_prints_full_representation_once(
    product_class: type[Product],
    extra_args: tuple[object, ...],
    expected: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = product_class("Товар", "Описание", 100.0, 3, *extra_args)

    captured = capsys.readouterr()
    assert captured.out == expected + "\n"
    assert captured.err == ""
    assert repr(product) == expected
    assert str(product) == "Товар, 100.0 руб. Остаток: 3 шт."
    assert capsys.readouterr().out == ""


@pytest.mark.parametrize(
    "creation_method", ["positional", "keyword", "factory"]
)
def test_creation_prints_same_arguments_for_all_creation_methods(
    creation_method: str, capsys: pytest.CaptureFixture[str]
) -> None:
    if creation_method == "positional":
        product = Product("Продукт1", "Описание продукта", 1200, 10)
    elif creation_method == "keyword":
        product = Product(
            quantity=10,
            price=1200,
            description="Описание продукта",
            name="Продукт1",
        )
    else:
        product = Product.new_product(
            {
                "quantity": 10,
                "price": 1200,
                "description": "Описание продукта",
                "name": "Продукт1",
            }
        )

    expected = "Product('Продукт1', 'Описание продукта', 1200, 10)"
    assert capsys.readouterr().out == expected + "\n"
    assert repr(product) == expected


def test_repr_uses_current_values_without_printing(
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = Product("Товар", "Описание", 100.0, 3)
    assert (
        capsys.readouterr().out == "Product('Товар', 'Описание', 100.0, 3)\n"
    )

    product.name = "Новый товар"
    product.description = "Новое описание"
    product.price = 125.5
    product.quantity = 2

    assert (
        repr(product) == "Product('Новый товар', 'Новое описание', 125.5, 2)"
    )
    assert capsys.readouterr().out == ""


def test_repr_escapes_quotes_and_newlines(
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = Product("Товар\nновый", "Описание 'вариант'", 100.0, 3)
    expected = "Product('Товар\\nновый', \"Описание 'вариант'\", 100.0, 3)"

    assert repr(product) == expected
    assert capsys.readouterr().out.splitlines() == [expected]


def test_base_entity_cannot_be_created() -> None:
    with pytest.raises(TypeError, match="abstract"):
        BaseEntity("Сущность", "Описание")
