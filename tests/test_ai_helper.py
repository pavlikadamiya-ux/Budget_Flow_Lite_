from ai_helper import generate_recommendation


def test_generate_recommendation_with_expenses():
    category_expenses = {"Еда": 20000, "Транспорт": 5000}
    balance = 50000
    result = generate_recommendation(category_expenses, balance)
    assert "Еда" in result
    assert "справочный" in result.lower()


def test_generate_recommendation_without_data():
    result = generate_recommendation({}, 0)
    assert "недостаточно" in result.lower() or "добавьте" in result.lower()


def test_generate_recommendation_negative_balance():
    result = generate_recommendation({"Развлечения": 15000}, -5000)
    assert "превышают доходы" in result.lower()
    assert "Развлечения" in result
