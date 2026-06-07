from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Mapping, Any


def _get_value(operation: Mapping[str, Any], key: str, default: Any = None) -> Any:
    return operation.get(key, default)


def calculate_income(operations: Iterable[Mapping[str, Any]]) -> float:
    total = 0.0
    for operation in operations:
        if _get_value(operation, "operation_type") == "income":
            total += float(_get_value(operation, "amount", 0) or 0)
    return round(total, 2)


def calculate_expenses(operations: Iterable[Mapping[str, Any]]) -> float:
    total = 0.0
    for operation in operations:
        if _get_value(operation, "operation_type") == "expense":
            total += float(_get_value(operation, "amount", 0) or 0)
    return round(total, 2)


def calculate_balance(income: float, expenses: float) -> float:
    return round(float(income) - float(expenses), 2)


def count_operations(operations: Iterable[Mapping[str, Any]]) -> int:
    return len(list(operations))


def group_expenses_by_category(operations: Iterable[Mapping[str, Any]]) -> dict[str, float]:
    grouped: dict[str, float] = defaultdict(float)
    for operation in operations:
        if _get_value(operation, "operation_type") == "expense":
            category = str(_get_value(operation, "category", "Прочее") or "Прочее")
            grouped[category] += float(_get_value(operation, "amount", 0) or 0)
    return {category: round(amount, 2) for category, amount in grouped.items()}


def get_top_expense_category(category_expenses: Mapping[str, float]) -> str | None:
    if not category_expenses:
        return None
    return max(category_expenses, key=category_expenses.get)


def prepare_dashboard_data(operations: Iterable[Mapping[str, Any]]) -> dict[str, Any]:
    operations_list = list(operations)
    income = calculate_income(operations_list)
    expenses = calculate_expenses(operations_list)
    balance = calculate_balance(income, expenses)
    category_expenses = group_expenses_by_category(operations_list)
    top_category = get_top_expense_category(category_expenses)

    return {
        "income": income,
        "expenses": expenses,
        "balance": balance,
        "operations_count": len(operations_list),
        "category_expenses": category_expenses,
        "top_category": top_category,
    }
