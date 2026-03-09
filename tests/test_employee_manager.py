import pytest
from employee_manager import add_employee, get_employee_by_id, list_all_employees

def test_add_employee_success(mock_sql_db):
    """Tests successful employee creation[cite: 140]."""
    result = add_employee("Jane", "Doe", "jane.doe@enterprise.com", "2024-01-01", "Engineering")
    assert result is True

def test_add_employee_duplicate_email(mock_sql_db):
    """Tests handling of duplicate emails[cite: 89, 141, 142]."""
    add_employee("Jane", "Doe", "jane@test.com", "2024-01-01", "HR")
    # Attempting to add the same email should fail or raise an error depending on implementation
    result = add_employee("John", "Smith", "jane@test.com", "2024-02-01", "Finance")
    assert result is False

def test_get_employee_by_id(mock_sql_db):
    """Tests retrieval of a single record[cite: 90, 143]."""
    add_employee("Alice", "Wonder", "alice@test.com", "2024-01-01", "IT")
    employee = get_employee_by_id(1)
    assert employee['first_name'] == "Alice"