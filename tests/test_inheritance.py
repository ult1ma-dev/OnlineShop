"""Тесты наследования товаров и ограничений операций."""

from itertools import permutations

import pytest

from src import Category, LawnGrass, Product, Smartphone

PRODUCT_KINDS = ("product", "smartphone", "lawn_grass", "custom")


class CustomProduct(Product):
    """Дополнительный наследник для проверки общих ограничений."""


@pytest.fixture
def product_pairs() -> dict[str, tuple[Product, Product]]:
    """Предоставляет пары товаров с разными ценами и остатками."""

    return {
        "product": (
            Product("Товар", "Описание", 100.0, 3),
            Product("Другой товар", "Описание", 25.0, 2),
        ),
        "smartphone": (
            Smartphone(
                "Телефон", "Описание", 100.0, 3, 95.5, "A", 128, "Белый"
            ),
            Smartphone(
                "Другой телефон", "Описание", 25.0, 2, 98.2, "B", 256, "Черный"
            ),
        ),
        "lawn_grass": (
            LawnGrass(
                "Трава", "Описание", 100.0, 3, "Россия", "7 дней", "Зеленый"
            ),
            LawnGrass(
                "Другая трава", "Описание", 25.0, 2, "США", "5 дней", "Темный"
            ),
        ),
        "custom": (
            CustomProduct("Особый товар", "Описание", 100.0, 3),
            CustomProduct("Другой особый товар", "Описание", 25.0, 2),
        ),
    }


def test_smartphone_initialization(
    product_pairs: dict[str, tuple[Product, Product]],
) -> None:
    smartphone = product_pairs["smartphone"][0]

    assert isinstance(smartphone, Smartphone)
    assert isinstance(smartphone, Product)
    assert smartphone.name == "Телефон"
    assert smartphone.description == "Описание"
    assert smartphone.price == 100.0
    assert smartphone.quantity == 3
    assert smartphone.efficiency == 95.5
    assert smartphone.model == "A"
    assert smartphone.memory == 128
    assert smartphone.color == "Белый"


def test_lawn_grass_initialization(
    product_pairs: dict[str, tuple[Product, Product]],
) -> None:
    grass = product_pairs["lawn_grass"][0]

    assert isinstance(grass, LawnGrass)
    assert isinstance(grass, Product)
    assert grass.name == "Трава"
    assert grass.description == "Описание"
    assert grass.price == 100.0
    assert grass.quantity == 3
    assert grass.country == "Россия"
    assert grass.germination_period == "7 дней"
    assert grass.color == "Зеленый"


@pytest.mark.parametrize(
    ("kind", "expected"),
    [
        ("smartphone", "Телефон, 125.5 руб. Остаток: 2 шт."),
        ("lawn_grass", "Трава, 125.5 руб. Остаток: 2 шт."),
    ],
)
def test_subclasses_inherit_price_and_str(
    kind: str,
    expected: str,
    product_pairs: dict[str, tuple[Product, Product]],
) -> None:
    product = product_pairs[kind][0]

    product.price = 125.5
    product.quantity = 2

    assert product.price == 125.5
    assert str(product) == expected


@pytest.mark.parametrize("kind", ["smartphone", "lawn_grass"])
@pytest.mark.parametrize("new_price", [0, -100.0])
def test_subclasses_reject_nonpositive_price(
    kind: str,
    new_price: float,
    product_pairs: dict[str, tuple[Product, Product]],
    capsys: pytest.CaptureFixture[str],
) -> None:
    product = product_pairs[kind][0]
    original_attributes = vars(product).copy()

    product.price = new_price

    assert vars(product) == original_attributes
    assert (
        capsys.readouterr().out
        == "Цена не должна быть нулевая или отрицательная\n"
    )


@pytest.mark.parametrize("kind", PRODUCT_KINDS)
def test_same_class_addition(
    kind: str, product_pairs: dict[str, tuple[Product, Product]]
) -> None:
    first, second = product_pairs[kind]
    first_attributes = vars(first).copy()
    second_attributes = vars(second).copy()

    assert first + second == pytest.approx(350.0)
    assert second + first == pytest.approx(350.0)
    assert vars(first) == first_attributes
    assert vars(second) == second_attributes

    first.price = 120.5
    first.quantity = 2

    assert first + second == pytest.approx(291.0)


@pytest.mark.parametrize(
    ("first_kind", "second_kind"), list(permutations(PRODUCT_KINDS, 2))
)
def test_addition_rejects_different_classes(
    first_kind: str,
    second_kind: str,
    product_pairs: dict[str, tuple[Product, Product]],
) -> None:
    first = product_pairs[first_kind][0]
    second = product_pairs[second_kind][0]
    first_attributes = vars(first).copy()
    second_attributes = vars(second).copy()

    with pytest.raises(TypeError):
        first.__add__(second)
    with pytest.raises(TypeError):
        first + second

    assert vars(first) == first_attributes
    assert vars(second) == second_attributes


@pytest.mark.parametrize("kind", PRODUCT_KINDS)
def test_category_accepts_products_and_subclasses(
    kind: str, product_pairs: dict[str, tuple[Product, Product]]
) -> None:
    initial_product = Product("Чехол", "Описание", 10.0, 1)
    category = Category("Смартфоны", "Описание", [initial_product])
    added_product = product_pairs[kind][0]

    category.add_product(added_product)

    assert list(category) == [initial_product, added_product]
    assert Category.product_count == 2
    assert Category.category_count == 1


@pytest.mark.parametrize(
    "invalid_product", [100, "товар", None, {}, [], object(), Product]
)
def test_category_rejects_nonproducts_without_changes(
    invalid_product: object,
) -> None:
    product = Product("Телефон", "Описание", 100.0, 3)
    category = Category("Смартфоны", "Описание", [product])
    original_products = category.products

    with pytest.raises(TypeError):
        category.add_product(invalid_product)

    assert list(category) == [product]
    assert category.products == original_products
    assert Category.product_count == 1
    assert Category.category_count == 1
