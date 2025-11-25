# Задание 2.1

# Автоматизация тест-кейсов 

## Требования

- Python 3.7 или выше
- pip (менеджер пакетов Python)
- Доступ к интернету (для подключения к API)

## Структура проекта

```
Task2/
├── api_client.py          # API клиент для работы с микросервисом
├── conftest.py             # Pytest конфигурация и фикстуры
├── test_create_ad.py      # Тесты для создания объявлений (TestCase 1-6)
├── test_get_ad_by_id.py   # Тесты для получения объявления по ID (TestCase 7-10)
├── test_get_ads_by_seller.py  # Тесты для получения объявлений по sellerID (TestCase 11-15)
├── test_get_statistics.py # Тесты для получения статистики (TestCase 16-18)
├── test_integration.py    # Интеграционные тесты (TestCase 19-20)
├── requirements.txt       # Зависимости проекта
```

## Установка

### Перейти в директорию проекта

```bash
cd Avito_QA/Task2
```

### Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск тестов

### Запуск всех тестов

```bash
pytest
```

### Запуск с подробным выводом

```bash
pytest -v
```

### Запуск конкретного тест-файла

```bash
pytest "имя_файла"
```

### Запуск конкретного теста

```bash
pytest "имя_файла"::"имя_класса"::"имя_функции"
```

### Запуск с HTML отчетом

```bash
pytest --html=report.html --self-contained-html
```

HTML отчет будет создан в файле `report.html` в текущей директории.
