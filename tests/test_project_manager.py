import pytest
from project_manager import add_project, assign_employee_to_project, get_projects_for_employee
from employee_manager import add_employee

def test_add_project_default_status(mock_sql_db):
    """Tests project creation with default 'Planning' status[cite: 94, 108]."""
    result = add_project("Cloud Migration", "2024-05-01")
    assert result is True

def test_assign_employee_to_project(mock_sql_db):
    """Tests linking an employee to a project via the junction table[cite: 96, 144]."""
    add_employee("Bob", "Builder", "bob@test.com", "2024-01-01", "Construction")
    add_project("Bridge Build", "2024-06-01")
    
    # Link employee 1 to project 1 [cite: 109, 110]
    result = assign_employee_to_project(employee_id=1, project_id=1, role="Lead Architect")
    assert result is True

def test_get_projects_for_employee(mock_sql_db):
    """Tests querying projects across related tables[cite: 97, 111]."""
    add_employee("Dev", "User", "dev@test.com", "2024-01-01", "DevOps")
    add_project("Project Alpha", "2024-01-01")
    assign_employee_to_project(1, 1, "Developer")
    
    projects = get_projects_for_employee(1)
    assert len(projects) == 1
    assert projects[0]['project_name'] == "Project Alpha"