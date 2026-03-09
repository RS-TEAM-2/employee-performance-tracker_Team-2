import sqlite3
from datetime import date
from db_connections import get_sql_connection


def add_project(project_name, start_date, end_date=None, status="Planning"):
    conn = get_sql_connection()
    try:
        conn.execute(
            """
            INSERT INTO Projects (project_name, start_date, end_date, status)
            VALUES (?, ?, ?, ?)
            """,
            (project_name, start_date, end_date, status)
        )
        conn.commit()
        print(f"Project '{project_name}' added successfully.")
        return True
    except Exception as e:
        raise Exception(f"Failed to add project: {e}")
    finally:
        conn.close()


def assign_employee_to_project(employee_id, project_id, role):
    conn = get_sql_connection()
    try:
        emp = conn.execute(
            "SELECT employee_id FROM Employees WHERE employee_id = ?",
            (employee_id,)
        ).fetchone()
        if emp is None:
            raise ValueError(f"No employee found with ID {employee_id}.")

        proj = conn.execute(
            "SELECT project_id FROM Projects WHERE project_id = ?",
            (project_id,)
        ).fetchone()
        if proj is None:
            raise ValueError(f"No project found with ID {project_id}.")

        conn.execute(
            """
            INSERT INTO EmployeeProjects (employee_id, project_id, role, assignment_date)
            VALUES (?, ?, ?, ?)
            """,
            (employee_id, project_id, role, str(date.today()))
        )
        conn.commit()
        print(f"Employee {employee_id} assigned to project {project_id} as '{role}'.")
        return True
    except ValueError:
        raise
    except Exception as e:
        raise Exception(f"Failed to assign: {e}")
    finally:
        conn.close()


def get_projects_for_employee(employee_id):
    conn = get_sql_connection()
    try:
        cursor = conn.execute(
            """
            SELECT p.project_id, p.project_name, p.start_date,
                   p.end_date, p.status, ep.role, ep.assignment_date
            FROM EmployeeProjects ep
            JOIN Projects p ON ep.project_id = p.project_id
            WHERE ep.employee_id = ?
            ORDER BY ep.assignment_date DESC
            """,
            (employee_id,)
        )
        return [dict(row) for row in cursor.fetchall()]
    finally:
        conn.close()