from __future__ import annotations

from typing import Mapping


DISCLAIMER = "Рекомендация носит справочный характер и не является профессиональной финансовой консультацией."


def generate_recommendation(category_expenses: Mapping[str, float], balance: float) -> str:
    """
    Generate a simple budget recommendation from aggregated expense data.

    MVP note:
    This is a rule-based helper. It does not send financial data to external AI services.
    """
    if not category_expenses:
        return (
            "Недостаточно данных для рекомендации. "
            "Добавьте расходные операции, чтобы система могла проанализировать бюджет. "
            f"{DISCLAIMER}"
        )

    top_category = max(category_expenses, key=category_expenses.get)
    top_amount = float(category_expenses[top_category])
    category_tip = _category_tip(top_category)

    if balance < 0:
        return (
            "Ваши расходы превышают доходы. "
            f"Крупнейшая категория расходов — «{top_category}» ({top_amount:.0f} ₽). "
            "Рекомендуется пересмотреть необязательные траты и установить лимит на эту категорию. "
            f"{category_tip} {DISCLAIMER}"
        )

    return (
        f"Больше всего расходов приходится на категорию «{top_category}» ({top_amount:.0f} ₽). "
        "Рекомендуется отслеживать эту категорию и при необходимости установить лимит на следующий период. "
        f"{category_tip} {DISCLAIMER}"
    )


def _category_tip(category: str) -> str:
    normalized = category.strip().lower()
    if normalized == "еда":
        return "Для категории «Еда» можно заранее планировать покупки и фиксировать недельный лимит."
    if normalized == "развлечения":
        return "Для развлечений удобно задать отдельный лимит, чтобы не сокращать обязательные расходы."
    if normalized == "транспорт":
        return "Для транспорта можно проверить регулярные маршруты и сравнить стоимость альтернатив."
    if normalized == "жильё":
        return "Расходы на жильё обычно обязательные, поэтому лучше контролировать переменную часть платежей."
    if normalized == "здоровье":
        return "Расходы на здоровье лучше не сокращать резко, но их можно планировать заранее."
    if normalized == "образование":
        return "Расходы на образование могут быть инвестицией, но их тоже стоит учитывать в месячном плане."
    return "Эту категорию стоит отдельно отслеживать в следующем месяце."
