import pytest
import sqlite3
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class NoCloseConnection:
    """
    Wraps a sqlite3 connection and makes close() do nothing.
    This prevents test modules from closing the shared connection.
    """
    def __init__(self, conn):
        self._conn = conn

    def execute(self, *args, **kwargs):
        return self._conn.execute(*args, **kwargs)

    def executescript(self, *args, **kwargs):
        return self._conn.executescript(*args, **kwargs)

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def cursor(self):
        return self._conn.cursor()

    def close(self):
        pass  # do nothing — prevents modules from closing shared connection

    def __getattr__(self, name):
        return getattr(self._conn, name)


@pytest.fixture
def sql_db(monkeypatch):
    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row

    conn.executescript("""
        CREATE TABLE Employees (
            employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name  TEXT NOT NULL,
            last_name   TEXT NOT NULL,
            email       TEXT NOT NULL UNIQUE,
            hire_date   TEXT NOT NULL,
            department  TEXT NOT NULL
        );
        CREATE TABLE Projects (
            project_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            project_name TEXT NOT NULL,
            start_date   TEXT NOT NULL,
            end_date     TEXT,
            status       TEXT DEFAULT 'Planning'
        );
        CREATE TABLE EmployeeProjects (
            assignment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id     INTEGER NOT NULL,
            project_id      INTEGER NOT NULL,
            role            TEXT NOT NULL,
            assignment_date TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
            FOREIGN KEY (project_id)  REFERENCES Projects(project_id)
        );
    """)
    conn.commit()

    wrapped = NoCloseConnection(conn)

    import employee_manager
    import project_manager
    import reports

    monkeypatch.setattr(employee_manager, "get_sql_connection", lambda: wrapped)
    monkeypatch.setattr(project_manager,  "get_sql_connection", lambda: wrapped)
    monkeypatch.setattr(reports,          "get_sql_connection", lambda: wrapped)

    yield wrapped

    conn.close()


@pytest.fixture
def mongo_col(monkeypatch):
    import mongomock
    import performance_reviewer
    import reports

    mock_client = mongomock.MongoClient()
    mock_col = mock_client["test_db"]["reviews"]

    monkeypatch.setattr(performance_reviewer, "get_mongo_collection", lambda: mock_col)
    monkeypatch.setattr(reports, "get_mongo_collection", lambda: mock_col)

    return mock_col