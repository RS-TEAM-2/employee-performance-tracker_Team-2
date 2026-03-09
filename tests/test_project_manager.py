import pytest
from employee_manager import add_employee
from project_manager import add_project, assign_employee_to_project, get_projects_for_employee


def test_add_project_success(sql_db):
    result = add_project("Website Redesign", "2024-01-01")
    assert result == True


def test_add_project_with_all_fields(sql_db):
    result = add_project("Mobile App", "2024-02-01", "2024-12-31", "Active")
    assert result == True


def test_add_project_no_end_date(sql_db):
    result = add_project("Internal Tool", "2024-03-01")
    assert result == True


def test_assign_employee_success(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    add_project("Website Redesign", "2024-01-01")
    result = assign_employee_to_project(1, 1, "Developer")
    assert result == True


def test_assign_invalid_employee(sql_db):
    add_project("Website Redesign", "2024-01-01")
    with pytest.raises(ValueError) as exc_info:
        assign_employee_to_project(999, 1, "Developer")
    assert "No employee found" in str(exc_info.value)


def test_assign_invalid_project(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    with pytest.raises(ValueError) as exc_info:
        assign_employee_to_project(1, 999, "Developer")
    assert "No project found" in str(exc_info.value)


def test_get_projects_for_employee(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    add_project("Website Redesign", "2024-01-01")
    assign_employee_to_project(1, 1, "Developer")
    projects = get_projects_for_employee(1)
    assert len(projects) == 1
    assert projects[0]["project_name"] == "Website Redesign"
    assert projects[0]["role"] == "Developer"


def test_get_projects_empty(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    projects = get_projects_for_employee(1)
    assert projects == []


def test_employee_sees_only_own_projects(sql_db):
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    add_employee("Bob", "Smith", "bob@example.com", "2024-02-10", "HR")
    add_project("Website Redesign", "2024-01-01")
    assign_employee_to_project(1, 1, "Developer")
    assert len(get_projects_for_employee(1)) == 1
    assert len(get_projects_for_employee(2)) == 0