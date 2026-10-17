"""Тесты заказа и общей базы заказа и категории."""

import pytest

from src import BaseEntity, Category, LawnGrass, Order, Product, Smartphone


@pytest.fixture
def product() -> Product:
    return Product("Товар", "Описание", 100.5, 3)


def test_order_initialization(product: Product) -> None:
    order = Order(product, 2)

    assert order.product is product
    assert order.name == "Товар"
    assert order.description == "Описание"
    assert order.quantity == 2
    assert order.total_cost == 201.0
    assert product.quantity == 3
    assert Category.category_count == 0
    assert Category.product_count == 0


@pytest.mark.parametrize(
    ("product_class", "extra_args"),
    [
        (Product, ()),
        (Smartphone, (95.5, "Model A", 128, "Белый")),
        (LawnGrass, ("Россия", "7 дней", "Зеленый")),
    ],
)
@pytest.mark.parametrize("quantity", [1, 3, 8])
def test_order_accepts_products_and_subclasses_without_changing_stock(
    product_class: type[Product],
    extra_args: tuple[object, ...],
    quantity: int,
) -> None:
    product = product_class("Товар", "Описание", 100.5, 3, *extra_args)
    original_attributes = vars(product).copy()

    order = Order(product, quantity)

    assert order.product is product
    assert order.quantity == quantity
    assert order.total_cost == pytest.approx(100.5 * quantity)
    assert vars(product) == original_attributes
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_order_accepts_other_product_descendants() -> None:
    class OtherProduct(Product):
        """Дополнительный вид товара для проверки наследников."""

    product = OtherProduct("Особый товар", "Описание", 25.0, 1)

    order = Order(product, 2)

    assert order.product is product
    assert order.total_cost == 50.0
    assert product.quantity == 1


def test_category_and_order_share_base_entity(product: Product) -> None:
    category = Category("Категория", "Описание категории", [product])
    order = Order(product, 2)

    assert isinstance(category, BaseEntity)
    assert isinstance(order, BaseEntity)
    assert category.name == "Категория"
    assert category.description == "Описание категории"
    assert order.name == product.name
    assert order.description == product.description
    assert Category.category_count == 1
    assert Category.product_count == 1


def test_order_preserves_purchase_cost_and_description(
    product: Product,
) -> None:
    order = Order(product, 2)

    product.price = 200.0
    product.name = "Новое название"
    product.description = "Новое описание"
    product.quantity = 10

    assert order.product is product
    assert order.total_cost == 201.0
    assert order.name == "Товар"
    assert order.description == "Описание"
    assert order.quantity == 2


def test_order_str(product: Product) -> None:
    order = Order(product, 2)

    assert (
        str(order) == "Товар, количество: 2 шт. Итоговая стоимость: 201.0 руб."
    )


@pytest.mark.parametrize(
    "invalid_product", [None, "товар", 42, {}, [], object(), Product]
)
def test_order_rejects_nonproducts(invalid_product: object) -> None:
    with pytest.raises(TypeError):
        Order(invalid_product, 1)

    assert Category.category_count == 0
    assert Category.product_count == 0


@pytest.mark.parametrize(
    "quantity", [None, "2", 2.0, True, False, {}, [], object()]
)
def test_order_rejects_noninteger_quantity(
    product: Product, quantity: object
) -> None:
    original_attributes = vars(product).copy()

    with pytest.raises(TypeError):
        Order(product, quantity)

    assert vars(product) == original_attributes
    assert Category.category_count == 0
    assert Category.product_count == 0


@pytest.mark.parametrize("quantity", [0, -1, -10])
def test_order_rejects_nonpositive_quantity(
    product: Product, quantity: int
) -> None:
    original_attributes = vars(product).copy()

    with pytest.raises(ValueError):
        Order(product, quantity)

    assert vars(product) == original_attributes
    assert Category.category_count == 0
    assert Category.product_count == 0
