from pathlib import Path

from db import add_operation, delete_operation, get_operations, init_db


def test_add_and_get_operation(tmp_path: Path):
    db_path = str(tmp_path / "test_budgetflow.db")
    init_db(db_path)
    operation_id = add_operation(
        operation_date="2026-06-01",
        operation_type="income",
        category="Зарплата",
        amount=80000,
        comment="Тест",
        db_path=db_path,
    )
    operations = get_operations(db_path)
    assert operation_id > 0
    assert len(operations) == 1
    assert operations[0]["category"] == "Зарплата"
    assert operations[0]["amount"] == 80000


def test_delete_operation(tmp_path: Path):
    db_path = str(tmp_path / "test_budgetflow.db")
    init_db(db_path)
    operation_id = add_operation(
        operation_date="2026-06-01",
        operation_type="expense",
        category="Еда",
        amount=1500,
        comment="Тест",
        db_path=db_path,
    )
    delete_operation(operation_id, db_path)
    assert get_operations(db_path) == []


def test_add_operation_validation(tmp_path: Path):
    db_path = str(tmp_path / "test_budgetflow.db")
    init_db(db_path)
    try:
        add_operation(
            operation_date="2026-06-01",
            operation_type="expense",
            category="Еда",
            amount=0,
            comment="Ошибка",
            db_path=db_path,
        )
    except ValueError as error:
        assert "amount" in str(error)
    else:
        raise AssertionError("Expected ValueError")
