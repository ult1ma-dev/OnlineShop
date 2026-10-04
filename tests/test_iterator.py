"""Тесты перебора товаров категории."""

from collections.abc import Callable, Iterator

import pytest

from src import Category, CategoryIterator, Product


@pytest.fixture
def category_with_products() -> tuple[Category, list[Product]]:
    products = [
        Product("Телефон", "Описание", 100.0, 10),
        Product("Чехол", "Описание", 200.0, 2),
    ]
    return Category("Техника", "Описание", products), products


@pytest.mark.parametrize(
    "iterator_factory", [iter, CategoryIterator], ids=["category", "helper"]
)
def test_iteration_returns_original_products_in_order(
    iterator_factory: Callable[[Category], Iterator[Product]],
    category_with_products: tuple[Category, list[Product]],
) -> None:
    category, products = category_with_products
    visited = []

    for product in iterator_factory(category):
        visited.append(product)

    assert len(visited) == 2
    assert visited[0] is products[0]
    assert visited[1] is products[1]


def test_category_can_be_iterated_repeatedly(
    category_with_products: tuple[Category, list[Product]],
) -> None:
    category, products = category_with_products

    assert [product for product in category] == products
    assert [product for product in category] == products


def test_category_iterator_resumes_without_resetting(
    category_with_products: tuple[Category, list[Product]],
) -> None:
    category, products = category_with_products
    iterator = CategoryIterator(category)

    assert iter(iterator) is iterator
    assert next(iterator) is products[0]
    assert list(iter(iterator)) == [products[1]]
    with pytest.raises(StopIteration):
        next(iterator)
    with pytest.raises(StopIteration):
        next(iterator)


@pytest.mark.parametrize(
    "iterator_factory", [iter, CategoryIterator], ids=["category", "helper"]
)
def test_empty_category_iterator(
    iterator_factory: Callable[[Category], Iterator[Product]],
) -> None:
    iterator = iterator_factory(Category("Аксессуары", "Описание", []))

    assert list(iterator) == []
    with pytest.raises(StopIteration):
        next(iterator)


@pytest.mark.parametrize(
    "iterator_factory", [iter, CategoryIterator], ids=["category", "helper"]
)
def test_category_iterators_are_independent(
    iterator_factory: Callable[[Category], Iterator[Product]],
    category_with_products: tuple[Category, list[Product]],
) -> None:
    category, products = category_with_products
    first_iterator = iterator_factory(category)
    second_iterator = iterator_factory(category)

    assert next(first_iterator) is products[0]
    assert next(second_iterator) is products[0]
    assert next(first_iterator) is products[1]
    assert next(second_iterator) is products[1]
    with pytest.raises(StopIteration):
        next(first_iterator)
    with pytest.raises(StopIteration):
        next(second_iterator)


def test_category_iterator_includes_products_added_before_iteration(
    category_with_products: tuple[Category, list[Product]],
) -> None:
    category, products = category_with_products
    added_product = Product("Наушники", "Описание", 50.0, 1)
    expected_products = [*products, added_product]

    category.add_product(added_product)

    assert list(CategoryIterator(category)) == expected_products
