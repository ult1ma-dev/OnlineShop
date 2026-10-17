"""Проверка полного запуска демонстрации из домашнего задания."""

import subprocess
import sys
from pathlib import Path


def test_main_runs_assignment_example_without_errors() -> None:
    project_root = Path(__file__).resolve().parents[1]

    result = subprocess.run(
        [sys.executable, "-X", "utf8", str(project_root / "main.py")],
        cwd=project_root,
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=True,
        timeout=10,
    )

    lines = result.stdout.splitlines()
    assert result.stderr == ""
    assert lines[0] == (
        "Возникла ошибка ValueError прерывающая работу программы "
        "при попытке добавить продукт с нулевым количеством"
    )
    assert "Не возникла ошибка" not in result.stdout
    creation_lines = [line for line in lines if line.startswith("Product(")]
    assert creation_lines == [
        "Product('Samsung Galaxy S23 Ultra', "
        "'256GB, Серый цвет, 200MP камера', 180000.0, 5)",
        "Product('Iphone 15', '512GB, Gray space', 210000.0, 8)",
        "Product('Xiaomi Redmi Note 11', '1024GB, Синий', 31000.0, 14)",
        "Product('Чехол', 'Защитный чехол', 1000.0, 2)",
    ]
    assert lines[4:6] == ["140333.33333333334", "0"]
    assert lines[7:12] == [
        "Товар успешно добавлен",
        "Обработка добавления товара завершена",
        "Товар успешно добавлен",
        "Обработка добавления товара завершена",
        "Samsung Galaxy S23 Ultra, количество: 2 шт. "
        "Итоговая стоимость: 360000.0 руб.",
    ]
    assert lines[-4:] == [
        "Товар с нулевым количеством не может быть добавлен",
        "Обработка добавления товара завершена",
        "Товар с нулевым количеством не может быть добавлен",
        "Обработка добавления товара завершена",
    ]
