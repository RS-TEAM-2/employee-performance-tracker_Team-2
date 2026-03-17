import sqlite3
from datetime import date, datetime
from db_connections import sql_connection_context


def _parse_date(value):
    """Parse a date value which may be a date object or an ISO date string.
    Returns a `date` or None. Raises ValueError for invalid formats/types.
    """
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        value = value.strip()
        try:
            return date.fromisoformat(value)
        except ValueError:
            try:
                return datetime.strptime(value, "%Y-%m-%d").date()
            except Exception:
                raise ValueError(f"Invalid date format: {value}. Expected YYYY-MM-DD or date object.")
    raise ValueError("Invalid date type for date fields.")


def add_project(project_name, start_date, end_date=None, status="Planning"):
    # validate/parse dates first
    start_dt = _parse_date(start_date)
    end_dt = _parse_date(end_date)

    if start_dt is None:
        raise ValueError("start_date is required and must be a valid date.")

    # Validate project name: must start with a letter and not be only numbers
    if project_name is None or not isinstance(project_name, str) or not project_name.strip():
        raise ValueError("Project name is required.")
    project_name = " ".join(project_name.strip().split())
    if not project_name[0].isalpha():
        raise ValueError("Project name must start with a letter.")
    if project_name.isdigit():
        raise ValueError("Project name cannot consist of only numbers.")

    if end_dt is not None and start_dt > end_dt:
        raise ValueError("Start date cannot be after end date.")

    with sql_connection_context() as conn:
        try:
            conn.execute(
                """
                INSERT INTO Projects (project_name, start_date, end_date, status)
                VALUES (?, ?, ?, ?)
                """,
                (project_name, start_dt.isoformat(), end_dt.isoformat() if end_dt else None, status)
            )
            conn.commit()
            print(f"Project '{project_name}' added successfully.")
            return True
        except Exception as e:
            raise Exception(f"Failed to add project: {e}")


def assign_employee_to_project(employee_id, project_id, role):
    with sql_connection_context() as conn:
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

            # Validate role: must start with a letter and not be only numbers
            if role is None or not isinstance(role, str) or not role.strip():
                raise ValueError("Role is required.")
            role = " ".join(role.strip().split())
            if not role[0].isalpha():
                raise ValueError("Role must start with a letter.")
            if role.isdigit():
                raise ValueError("Role cannot consist of only numbers.")

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


def get_projects_for_employee(employee_id):
    with sql_connection_context() as conn:
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