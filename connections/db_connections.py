from connections.sqlite_connection import get_connection


def initialize_database():

    conn = get_connection()
    cursor = conn.cursor()

    # Employees Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        hire_date DATE NOT NULL,
        department TEXT NOT NULL
    )
    """)

    # Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Projects (
        project_id INTEGER PRIMARY KEY AUTOINCREMENT,
        project_name TEXT NOT NULL,
        start_date DATE NOT NULL,
        end_date DATE,
        status TEXT NOT NULL
    )
    """)

    # EmployeeProjects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS EmployeeProjects (
        assignment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        project_id INTEGER,
        role TEXT,
        assignment_date DATE,
        FOREIGN KEY(employee_id) REFERENCES Employees(employee_id),
        FOREIGN KEY(project_id) REFERENCES Projects(project_id)
    )
    """)

    conn.commit()
    conn.close()