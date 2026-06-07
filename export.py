from __future__ import annotations

import io
from typing import Mapping, Any

import pandas as pd


def operations_to_dataframe(operations: list[Mapping[str, Any]]) -> pd.DataFrame:
    df = pd.DataFrame(list(operations))
    if df.empty:
        return pd.DataFrame(columns=["ID", "Дата", "Тип", "Категория", "Сумма", "Комментарий", "Создано"])

    rename_map = {
        "id": "ID",
        "operation_date": "Дата",
        "operation_type": "Тип",
        "category": "Категория",
        "amount": "Сумма",
        "comment": "Комментарий",
        "created_at": "Создано",
    }
    df = df.rename(columns=rename_map)
    preferred_columns = ["ID", "Дата", "Тип", "Категория", "Сумма", "Комментарий", "Создано"]
    existing_columns = [column for column in preferred_columns if column in df.columns]
    df = df[existing_columns]
    if "Тип" in df.columns:
        df["Тип"] = df["Тип"].replace({"income": "Доход", "expense": "Расход"})
    return df


def export_to_csv(operations: list[Mapping[str, Any]]) -> bytes:
    df = operations_to_dataframe(operations)
    return df.to_csv(index=False).encode("utf-8-sig")


def export_to_xlsx(operations: list[Mapping[str, Any]]) -> bytes:
    df = operations_to_dataframe(operations)
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Operations")
    output.seek(0)
    return output.read()
