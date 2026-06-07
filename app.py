from __future__ import annotations

from datetime import date

import pandas as pd
import streamlit as st

from ai_helper import DISCLAIMER, generate_recommendation
from analytics import prepare_dashboard_data
from db import add_operation, clear_operations, delete_operation, get_operations, init_db, seed_demo_data
from export import export_to_csv, export_to_xlsx


DB_PATH = "budgetflow.db"

INCOME_CATEGORIES = ["Зарплата", "Подработка", "Подарки", "Прочее"]
EXPENSE_CATEGORIES = ["Еда", "Транспорт", "Жильё", "Развлечения", "Здоровье", "Образование", "Прочее"]


def filter_operations(
    operations: list[dict],
    start_date: date,
    end_date: date,
    operation_type_filter: str,
    category_filter: str,
) -> list[dict]:
    filtered = []

    for operation in operations:
        op_date = date.fromisoformat(operation["operation_date"])
        if not (start_date <= op_date <= end_date):
            continue

        if operation_type_filter != "Все":
            expected_type = "income" if operation_type_filter == "Доход" else "expense"
            if operation["operation_type"] != expected_type:
                continue

        if category_filter != "Все" and operation["category"] != category_filter:
            continue

        filtered.append(operation)

    return filtered


def render_operation_form() -> None:
    st.subheader("Добавить операцию")

    operation_type_label = st.selectbox("Тип операции", ["Расход", "Доход"])
    operation_type = "expense" if operation_type_label == "Расход" else "income"
    categories = EXPENSE_CATEGORIES if operation_type == "expense" else INCOME_CATEGORIES

    with st.form("operation_form", clear_on_submit=True):
        operation_date = st.date_input("Дата", value=date.today())
        category = st.selectbox("Категория", categories)
        amount = st.number_input("Сумма", min_value=0.0, step=100.0)
        comment = st.text_input("Комментарий")
        submitted = st.form_submit_button("Добавить")

    if submitted:
        try:
            add_operation(
                operation_date=operation_date.isoformat(),
                operation_type=operation_type,
                category=category,
                amount=amount,
                comment=comment,
                db_path=DB_PATH,
            )
            st.success("Операция добавлена")
            st.rerun()
        except ValueError as error:
            st.error(str(error))


def render_filters(operations: list[dict]) -> list[dict]:
    st.subheader("Фильтры")

    if operations:
        dates = [date.fromisoformat(op["operation_date"]) for op in operations]
        min_date = min(dates)
        max_date = max(dates)
    else:
        min_date = date.today()
        max_date = date.today()

    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input("Начальная дата", value=min_date)
    with col2:
        end_date = st.date_input("Конечная дата", value=max_date)

    operation_type_filter = st.selectbox("Тип", ["Все", "Доход", "Расход"])
    all_categories = sorted(set(INCOME_CATEGORIES + EXPENSE_CATEGORIES + [op["category"] for op in operations]))
    category_filter = st.selectbox("Категория", ["Все"] + all_categories)

    if start_date > end_date:
        st.warning("Начальная дата больше конечной. Фильтр по датам не применён.")
        start_date, end_date = min_date, max_date

    return filter_operations(operations, start_date, end_date, operation_type_filter, category_filter)


def render_dashboard(operations: list[dict]) -> dict:
    st.subheader("Дашборд")
    dashboard = prepare_dashboard_data(operations)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Доходы", f"{dashboard['income']:.0f} ₽")
    col2.metric("Расходы", f"{dashboard['expenses']:.0f} ₽")
    col3.metric("Баланс", f"{dashboard['balance']:.0f} ₽")
    col4.metric("Операций", dashboard["operations_count"])

    if dashboard["top_category"]:
        st.info(f"Крупнейшая категория расходов: {dashboard['top_category']}")
    else:
        st.info("Расходных операций пока нет.")

    return dashboard


def render_operations_table(operations: list[dict]) -> None:
    st.subheader("Операции")

    if not operations:
        st.write("Операций пока нет.")
        return

    df = pd.DataFrame(operations)
    visible_df = df.rename(
        columns={
            "id": "ID",
            "operation_date": "Дата",
            "operation_type": "Тип",
            "category": "Категория",
            "amount": "Сумма",
            "comment": "Комментарий",
            "created_at": "Создано",
        }
    )
    visible_df["Тип"] = visible_df["Тип"].replace({"income": "Доход", "expense": "Расход"})
    st.dataframe(visible_df, use_container_width=True)

    operation_ids = [op["id"] for op in operations]
    operation_to_delete = st.selectbox("ID операции для удаления", operation_ids)
    if st.button("Удалить выбранную операцию"):
        delete_operation(operation_to_delete, DB_PATH)
        st.success("Операция удалена")
        st.rerun()


def render_chart(dashboard: dict) -> None:
    st.subheader("Расходы по категориям")

    category_expenses = dashboard["category_expenses"]
    if not category_expenses:
        st.write("Нет расходов для построения графика.")
        return

    chart_df = pd.DataFrame(
        [{"Категория": category, "Сумма": amount} for category, amount in category_expenses.items()]
    ).set_index("Категория")

    st.bar_chart(chart_df)


def render_ai_recommendation(dashboard: dict) -> None:
    st.subheader("AI-рекомендация")
    recommendation = generate_recommendation(
        category_expenses=dashboard["category_expenses"],
        balance=dashboard["balance"],
    )
    st.write(recommendation)
    st.caption(DISCLAIMER)


def render_export(operations: list[dict]) -> None:
    st.subheader("Экспорт отчёта")

    if not operations:
        st.write("Нет данных для экспорта.")
        return

    csv_bytes = export_to_csv(operations)
    xlsx_bytes = export_to_xlsx(operations)

    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            label="Скачать CSV",
            data=csv_bytes,
            file_name="budgetflow_report.csv",
            mime="text/csv",
        )
    with col2:
        st.download_button(
            label="Скачать XLSX",
            data=xlsx_bytes,
            file_name="budgetflow_report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )


def main() -> None:
    st.set_page_config(page_title="BudgetFlow Lite", page_icon="💰", layout="wide")
    init_db(DB_PATH)

    st.title("BudgetFlow Lite")
    st.write("Веб-приложение для учёта личных финансов с AI-помощником.")

    with st.sidebar:
        st.header("Демо")
        if st.button("Заполнить demo-data"):
            seed_demo_data(DB_PATH)
            st.success("Демо-данные добавлены")
            st.rerun()

        if st.button("Очистить операции"):
            clear_operations(DB_PATH)
            st.warning("Операции очищены")
            st.rerun()

    render_operation_form()
    all_operations = get_operations(DB_PATH)
    filtered_operations = render_filters(all_operations)
    dashboard = render_dashboard(filtered_operations)
    render_operations_table(filtered_operations)
    render_chart(dashboard)
    render_ai_recommendation(dashboard)
    render_export(filtered_operations)


if __name__ == "__main__":
    main()
