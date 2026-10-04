# SkyPro Store Homework

Учебное ядро интернет-магазина на Python. Проект подготовлен по GitFlow и
использует Poetry для управления виртуальным окружением и зависимостями.

## Реализованная функциональность

- класс `Product` с названием, описанием, ценой и количеством на складе;
- класс `Category` со списком товаров;
- строковые представления товаров и категорий через `__str__`;
- сложение товаров для расчёта стоимости их остатков на складе;
- класс `CategoryIterator` для перебора товаров категории;
- автоматический подсчёт созданных категорий и товаров;
- загрузка категорий и вложенных товаров из JSON-файла;
- тесты инициализации моделей, классовых счётчиков и JSON-загрузчика;
- автоматическая проверка покрытия с минимальным порогом 75%.

## Установка

```bash
poetry install
```

## Использование

```python
from src.utils import load_categories_from_json

categories = load_categories_from_json("data/products.json")
```

Цена товара хранится в приватном атрибуте `Product.__price`. Python преобразует
его имя в `_Product__price`. Читать и изменять цену следует через свойство `price`:

```python
from src.classes import Product

product = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
print(product.price)
product.price = 200000.0
```

Сеттер принимает положительную цену. При попытке установить нулевую или
отрицательную цену он выводит сообщение и сохраняет прежнее значение.
Приватное хранение цены проверяется тестами для конструктора и `new_product()`.

Строка товара содержит название, цену и остаток. Строка категории показывает
сумму остатков всех её товаров, а не количество наименований. Сложение двух
товаров возвращает общую стоимость их остатков и сохраняет исходные объекты:

```python
from src.classes import Category, CategoryIterator, Product

first_product = Product("Телефон", "Описание", 100.0, 10)
second_product = Product("Чехол", "Описание", 200.0, 2)
category = Category("Техника", "Товары для дома", [first_product, second_product])

print(first_product)  # Телефон, 100.0 руб. Остаток: 10 шт.
print(category)  # Техника, количество продуктов: 12 шт.
print(first_product + second_product)  # 1400.0

for product in CategoryIterator(category):
    print(product)
```

Категорию можно перебирать и напрямую: `for product in category`.
Каждый новый `CategoryIterator(category)` начинает перебор с первого товара.
После завершения перебора `next()` вызывает `StopIteration`.

## Сдача задания 14_3

Реализация задания находится в ветке
[`Feature/14_3`](https://github.com/ult1ma-dev/OnlineShop/tree/Feature/14_3).
Для проверки преподавателю нужно передать ссылку на эту ветку.

В `main.py` включены примеры из
[файла задания](https://drive.google.com/file/d/16nHmgNK9QJs0iR7fopgOWPvCsa8tgBQm/view)
и демонстрация итератора. Запуск:

```bash
poetry run python main.py
```

## Проверка качества

```bash
poetry run pytest
poetry run black --check .
poetry run isort --check-only .
poetry run flake8 .
poetry run mypy
```

После запуска тестов XML-отчёт сохраняется в `coverage.xml`. Текущая настройка
останавливает проверку, если покрытие функционального кода опускается ниже 75%.
