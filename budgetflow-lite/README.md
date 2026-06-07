# BudgetFlow Lite

BudgetFlow Lite — учебное веб-приложение для учёта личных финансов, анализа расходов и формирования базовой AI-рекомендации по бюджету.

## Функции MVP

- добавление доходов и расходов;
- категории операций;
- таблица операций;
- удаление операций;
- фильтры по периоду, типу и категории;
- расчёт доходов, расходов и баланса;
- график расходов по категориям;
- экспорт CSV/XLSX;
- AI-рекомендация по расходам;
- автотесты pytest;
- локальный запуск через Streamlit.

## Стек

- Python 3.10+
- Streamlit
- SQLite
- Pandas
- OpenPyXL
- pytest
- GitHub Actions

## Быстрый запуск

```bash
git clone https://github.com/<username>/budgetflow-lite.git
cd budgetflow-lite
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Для macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

После запуска приложение доступно по адресу:

```text
http://localhost:8501
```

## Тесты

```bash
pytest
```

Ожидаемый результат:

```text
11 passed
```

## Структура

```text
budgetflow-lite/
├── app.py
├── db.py
├── analytics.py
├── export.py
├── ai_helper.py
├── requirements.txt
├── README.md
├── Deployment_Guide.md
├── Release_Notes_v0.1.0.md
├── tests/
│   ├── test_analytics.py
│   ├── test_ai_helper.py
│   └── test_db.py
└── .github/
    └── workflows/
        └── ci.yml
```

## Ограничения MVP

- локальный запуск;
- без авторизации;
- без банковских интеграций;
- без хранения платёжных данных;
- AI-рекомендация справочная и не является финансовой консультацией.
