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
    creation_lines = [line for line in lines if line.startswith("Product(")]
    assert creation_lines == [
        "Product('Samsung Galaxy S23 Ultra', "
        "'256GB, Серый цвет, 200MP камера', 180000.0, 5)",
        "Product('Iphone 15', '512GB, Gray space', 210000.0, 8)",
        "Product('Xiaomi Redmi Note 11', '1024GB, Синий', 31000.0, 14)",
        "Product('55\" QLED 4K', 'Фоновая подсветка', 123000.0, 7)",
    ]
    assert "True" in lines
    assert '55" QLED 4K, 123000.0 руб. Остаток: 7 шт.' in lines
    assert lines[-3:] == [
        "2",
        "4",
        "Samsung Galaxy S23 Ultra, количество: 2 шт. "
        "Итоговая стоимость: 360000.0 руб.",
    ]
