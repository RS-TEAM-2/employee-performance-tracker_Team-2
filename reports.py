from db_connections import sql_connection_context, get_mongo_collection



def generate_employee_project_report():
    with sql_connection_context() as conn:
        cursor = conn.execute("""
            SELECT e.first_name || ' ' || e.last_name AS employee_name,
                   p.project_name, ep.role, ep.assignment_date, p.status
            FROM EmployeeProjects ep
            JOIN Employees e ON ep.employee_id = e.employee_id
            JOIN Projects p  ON ep.project_id  = p.project_id
            ORDER BY e.first_name
        """)
        rows = cursor.fetchall()
        if not rows:
            print("No assignments found.")
            return
        print(f"\n{'-'*80}")
        print(f"{'Employee':<25} {'Project':<25} {'Role':<15} {'Assigned':<12} {'Status'}")
        print(f"{'-'*80}")
        for row in rows:
            print(f"{row['employee_name']:<25} {row['project_name']:<25} {row['role']:<15} {row['assignment_date']:<12} {row['status']}")


def generate_employee_performance_summary(employee_id):
    with sql_connection_context() as conn:
        emp = conn.execute(
            "SELECT * FROM Employees WHERE employee_id = ?",
            (employee_id,)
        ).fetchone()

    if emp is None:
        print(f"No employee found with ID {employee_id}.")
        return

    collection = get_mongo_collection()
    reviews = list(collection.find({"employee_id": employee_id}))

    print(f"\n{'='*50}")
    print(f"Employee  : {emp['first_name']} {emp['last_name']}")
    print(f"Department: {emp['department']}")
    print(f"Hire Date : {emp['hire_date']}")
    print(f"{'='*50}")

    if not reviews:
        print("No reviews found for this employee.")
        return

    avg = sum(r["overall_rating"] for r in reviews) / len(reviews)
    print(f"Total Reviews : {len(reviews)}")
    print(f"Average Rating: {avg:.1f} / 5.0")
    latest = reviews[-1]
    print(f"Reviewer      : {latest['reviewer_name']}")
    print(f"Strengths     : {', '.join(latest['strengths'])}")
    print(f"Improve       : {', '.join(latest['areas_for_improvement'])}")
    print(f"Comments      : {latest['comments']}")
    print(f"Goals         : {', '.join(latest['goals_for_next_period'])}")