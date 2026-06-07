from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any


DEFAULT_DB_PATH = "budgetflow.db"


def get_connection(db_path: str = DEFAULT_DB_PATH) -> sqlite3.Connection:
    connection = sqlite3.connect(db_path)
    connection.row_factory = sqlite3.Row
    return connection


def init_db(db_path: str = DEFAULT_DB_PATH) -> None:
    parent = Path(db_path).parent
    if str(parent) not in ("", "."):
        parent.mkdir(parents=True, exist_ok=True)

    with get_connection(db_path) as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS operations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operation_date TEXT NOT NULL,
                operation_type TEXT NOT NULL CHECK(operation_type IN ('income', 'expense')),
                category TEXT NOT NULL,
                amount REAL NOT NULL CHECK(amount > 0),
                comment TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def add_operation(
    operation_date: str,
    operation_type: str,
    category: str,
    amount: float,
    comment: str = "",
    db_path: str = DEFAULT_DB_PATH,
) -> int:
    if operation_type not in {"income", "expense"}:
        raise ValueError("operation_type must be 'income' or 'expense'")
    if not category:
        raise ValueError("category is required")
    if amount <= 0:
        raise ValueError("amount must be greater than zero")
    if not operation_date:
        raise ValueError("operation_date is required")

    init_db(db_path)

    with get_connection(db_path) as connection:
        cursor = connection.execute(
            """
            INSERT INTO operations (operation_date, operation_type, category, amount, comment)
            VALUES (?, ?, ?, ?, ?)
            """,
            (operation_date, operation_type, category, float(amount), comment),
        )
        connection.commit()
        return int(cursor.lastrowid)


def get_operations(db_path: str = DEFAULT_DB_PATH) -> list[dict[str, Any]]:
    init_db(db_path)

    with get_connection(db_path) as connection:
        rows = connection.execute(
            """
            SELECT id, operation_date, operation_type, category, amount, comment, created_at
            FROM operations
            ORDER BY operation_date DESC, id DESC
            """
        ).fetchall()

    return [dict(row) for row in rows]


def delete_operation(operation_id: int, db_path: str = DEFAULT_DB_PATH) -> None:
    init_db(db_path)

    with get_connection(db_path) as connection:
        connection.execute("DELETE FROM operations WHERE id = ?", (operation_id,))
        connection.commit()


def clear_operations(db_path: str = DEFAULT_DB_PATH) -> None:
    init_db(db_path)

    with get_connection(db_path) as connection:
        connection.execute("DELETE FROM operations")
        connection.commit()


def seed_demo_data(db_path: str = DEFAULT_DB_PATH) -> None:
    init_db(db_path)
    existing = get_operations(db_path)
    if existing:
        return

    demo_operations = [
        ("2026-06-01", "income", "Зарплата", 80000, "Зарплата за месяц"),
        ("2026-06-02", "expense", "Еда", 15000, "Продукты"),
        ("2026-06-03", "expense", "Транспорт", 5000, "Метро и такси"),
        ("2026-06-04", "expense", "Развлечения", 10000, "Кино и кафе"),
        ("2026-06-05", "expense", "Здоровье", 3000, "Аптека"),
    ]

    for operation in demo_operations:
        add_operation(*operation, db_path=db_path)
