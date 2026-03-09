import sqlite3
from db_connections import get_sql_connection


def add_employee(first_name, last_name, email, hire_date, department):
    conn = get_sql_connection()
    try:
        conn.execute(
            """
            INSERT INTO Employees (first_name, last_name, email, hire_date, department)
            VALUES (?, ?, ?, ?, ?)
            """,
            (first_name, last_name, email, hire_date, department)
        )
        conn.commit()
        print(f"Employee {first_name} {last_name} added successfully.")
        return True
    except sqlite3.IntegrityError:
        raise ValueError(f"Email '{email}' already exists.")
    finally:
        conn.close()


def get_employee_by_id(employee_id):
    conn = get_sql_connection()
    try:
        cursor = conn.execute(
            "SELECT * FROM Employees WHERE employee_id = ?",
            (employee_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def list_all_employees():
    conn = get_sql_connection()
    try:
        cursor = conn.execute("SELECT * FROM Employees")
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()