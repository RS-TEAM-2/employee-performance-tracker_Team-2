import sqlite3
import re
from db_connections import get_sql_connection


def is_valid_email(email: str) -> bool:
    """Simple email format validation."""
    if not email:
        return False
    email = email.strip()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None


def _normalize_and_validate_name(name: str, field: str) -> str:
    if name is None:
        raise ValueError(f"{field} is required.")
    if not isinstance(name, str):
        raise ValueError(f"{field} must be a string.")
    value = " ".join(name.strip().split())
    if value == "":
        raise ValueError(f"{field} is required.")
    # Only allow letters and spaces
    if not re.match(r"^[A-Za-z ]+$", value):
        raise ValueError(f"{field} must contain only letters and spaces.")
    return value.title()


def add_employee(first_name, last_name, email, hire_date, department):
    # Basic validation and normalization
    # normalize/validate names
    first_name = _normalize_and_validate_name(first_name, "First name")
    last_name = _normalize_and_validate_name(last_name, "Last name")

    if email is None:
        raise ValueError("Email is required.")
    email = email.strip()
    if not is_valid_email(email):
        raise ValueError(f"Invalid email address: {email}")

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