# Deployment Guide

## 1. Требования

- Python 3.10+
- pip
- браузер
- интернет для установки зависимостей

## 2. Установка

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 3. Запуск

```bash
streamlit run app.py
```

Открыть:

```text
http://localhost:8501
```

## 4. Тесты

```bash
pytest
```

## 5. Возможные ошибки

Если Streamlit не найден:

```bash
pip install streamlit
```

Если зависимости не установились:

```bash
pip install -r requirements.txt
```

Если порт занят:

```bash
streamlit run app.py --server.port 8502
```
