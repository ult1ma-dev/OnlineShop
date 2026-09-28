"""Общие фикстуры pytest."""

from collections.abc import Generator

import pytest

from src.classes import Category


@pytest.fixture(autouse=True)
def reset_category_counters() -> Generator[None, None, None]:
    """Обнуляет счетчики классов для изоляции тестов."""

    Category.category_count = 0
    Category.product_count = 0
    yield
    Category.category_count = 0
    Category.product_count = 0
