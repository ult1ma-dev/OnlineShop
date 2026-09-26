"""Tests for JSON loading utilities."""

import json
from pathlib import Path

import pytest

from src.classes import Category, Product
from src.utils import load_categories_from_json, read_json


def test_load_categories_from_json() -> None:
    categories = load_categories_from_json(Path("data/products.json"))

    assert len(categories) == 2
    assert all(isinstance(category, Category) for category in categories)
    assert categories[0].name == "Смартфоны"
    assert len(categories[0].products) == 3
    assert isinstance(categories[0].products[0], Product)
    assert categories[0].products[0].price == 180000.0
    assert Category.category_count == 2
    assert Category.product_count == 4


def test_read_json_alias_handles_empty_list(tmp_path: Path) -> None:
    file_path = tmp_path / "empty.json"
    file_path.write_text("[]", encoding="utf-8")

    assert read_json(file_path) == []
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_categories_from_json_raises_for_invalid_json(tmp_path: Path) -> None:
    file_path = tmp_path / "invalid.json"
    file_path.write_text("not json", encoding="utf-8")

    with pytest.raises(json.JSONDecodeError):
        load_categories_from_json(file_path)


def test_load_categories_from_json_raises_for_missing_file(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        load_categories_from_json(tmp_path / "missing.json")
