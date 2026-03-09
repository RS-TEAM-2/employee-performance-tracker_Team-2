import pytest
import sqlite3
import os
from db_connections import get_sql_connection, init_sql_db


def test_get_sql_connection_returns_connection():
    conn = get_sql_connection()
    assert conn is not None
    conn.close()


def test_sql_connection_row_factory():
    conn = get_sql_connection()
    assert conn.row_factory == sqlite3.Row
    conn.close()


def test_init_sql_db_creates_employees_table():
    init_sql_db()
    conn = get_sql_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Employees'"
    )
    result = cursor.fetchone()
    assert result is not None
    assert result["name"] == "Employees"
    conn.close()


def test_init_sql_db_creates_projects_table():
    init_sql_db()
    conn = get_sql_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='Projects'"
    )
    result = cursor.fetchone()
    assert result is not None
    assert result["name"] == "Projects"
    conn.close()


def test_init_sql_db_creates_employeeprojects_table():
    init_sql_db()
    conn = get_sql_connection()
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='EmployeeProjects'"
    )
    result = cursor.fetchone()
    assert result is not None
    assert result["name"] == "EmployeeProjects"
    conn.close()


def test_company_db_file_exists():
    init_sql_db()
    assert os.path.exists("company.db")


def test_get_mongo_collection_raises_without_uri(monkeypatch):
    monkeypatch.delenv("MONGO_URI", raising=False)
    from db_connections import get_mongo_collection
    with pytest.raises(ValueError) as exc_info:
        get_mongo_collection()
    assert "MONGO_URI not found" in str(exc_info.value)