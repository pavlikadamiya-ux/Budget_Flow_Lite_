from analytics import (
    calculate_balance,
    calculate_expenses,
    calculate_income,
    get_top_expense_category,
    group_expenses_by_category,
    prepare_dashboard_data,
)


def test_calculate_income():
    operations = [
        {"operation_type": "income", "amount": 80000},
        {"operation_type": "expense", "amount": 15000},
    ]
    assert calculate_income(operations) == 80000


def test_calculate_expenses():
    operations = [
        {"operation_type": "income", "amount": 80000},
        {"operation_type": "expense", "amount": 15000},
        {"operation_type": "expense", "amount": 5000},
    ]
    assert calculate_expenses(operations) == 20000


def test_calculate_balance():
    assert calculate_balance(80000, 30000) == 50000


def test_group_expenses_by_category():
    operations = [
        {"operation_type": "expense", "category": "Еда", "amount": 15000},
        {"operation_type": "expense", "category": "Еда", "amount": 5000},
        {"operation_type": "expense", "category": "Транспорт", "amount": 3000},
        {"operation_type": "income", "category": "Зарплата", "amount": 80000},
    ]
    result = group_expenses_by_category(operations)
    assert result["Еда"] == 20000
    assert result["Транспорт"] == 3000
    assert "Зарплата" not in result


def test_get_top_expense_category():
    category_data = {"Еда": 20000, "Транспорт": 3000, "Развлечения": 10000}
    assert get_top_expense_category(category_data) == "Еда"


def test_prepare_dashboard_data():
    operations = [
        {"operation_type": "income", "category": "Зарплата", "amount": 80000},
        {"operation_type": "expense", "category": "Еда", "amount": 15000},
        {"operation_type": "expense", "category": "Транспорт", "amount": 5000},
    ]
    result = prepare_dashboard_data(operations)
    assert result["income"] == 80000
    assert result["expenses"] == 20000
    assert result["balance"] == 60000
    assert result["operations_count"] == 3
    assert result["top_category"] == "Еда"
