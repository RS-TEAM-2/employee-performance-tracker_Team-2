import pytest
from performance_reviewer import submit_performance_review
from employee_manager import add_employee
from project_manager import add_project, assign_employee_to_project


def test_cannot_review_unassigned_employee(sql_db, mongo_col):
    # reviewer (ID 2) is assigned, reviewee (ID 1) is not
    add_employee("Jane", "Doe", "jane@example.com", "2024-01-15", "Engineering")
    add_employee("Bob", "Smith", "bob@example.com", "2024-02-10", "HR")
    add_project("Website Redesign", "2024-01-01")
    assign_employee_to_project(2, 1, "Developer")

    with pytest.raises(ValueError) as excinfo:
        submit_performance_review(1, 2, 4.0, ["Skill"], ["Area"], "Good", ["Goal"])
    assert "assigned to at least one project" in str(excinfo.value)


def test_cannot_review_self(sql_db, mongo_col):
    add_employee("Alice", "Wong", "alice@example.com", "2024-01-15", "Engineering")
    add_project("Internal Tool", "2024-03-01")
    assign_employee_to_project(1, 1, "Developer")

    with pytest.raises(ValueError) as excinfo:
        submit_performance_review(1, 1, 4.0, ["Skill"], ["Area"], "Good", ["Goal"])
    assert str(excinfo.value) == "You cannot review yourself"
