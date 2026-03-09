import pytest
from employee_manager import add_employee, get_employee_by_id, list_all_employees


def test_add_employee_success(sql_db):
    result = add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    assert result == True


def test_add_employee_duplicate_email(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    with pytest.raises(ValueError) as exc_info:
        add_employee("John", "Smith", "jane@example.com", "2024-03-01", "HR")
    assert "already exists" in str(exc_info.value)


def test_get_employee_by_id_found(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    emp = get_employee_by_id(1)
    assert emp is not None
    assert emp["first_name"] == "Jane"
    assert emp["email"] == "jane@example.com"


def test_get_employee_by_id_not_found(sql_db):
    result = get_employee_by_id(999)
    assert result is None


def test_list_all_employees(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    add_employee("Bob", "Smith", "bob@example.com", "2024-02-10", "HR")
    employees = list_all_employees()
    assert len(employees) == 2


def test_list_all_employees_empty(sql_db):
    employees = list_all_employees()
    assert employees == []