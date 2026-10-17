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
    assert "2580000.0" in lines
    assert "16750.0" in lines
    assert "Возникла ошибка TypeError при попытке сложения" in lines
    assert lines[-2:] == [
        "5",
        "Возникла ошибка TypeError при добавлении не продукта",
    ]
    assert "Не возникла ошибка" not in result.stdout
