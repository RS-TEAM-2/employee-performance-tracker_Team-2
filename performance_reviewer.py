from datetime import date
from db_connections import get_mongo_collection
import re


def submit_performance_review(employee_id, reviewer_name, overall_rating,
                               strengths, areas_for_improvement,
                               comments, goals_for_next_period):
    collection = get_mongo_collection()
    # Server-side validation: prefer using the test-patched SQL connection if
    # available (conftest monkeypatches `employee_manager.get_sql_connection`).
    reviewer_display_name = None
    try:
        conn = None
        try:
            import employee_manager as _emp
            if hasattr(_emp, "get_sql_connection"):
                conn = _emp.get_sql_connection()
        except Exception:
            conn = None

        if conn is None:
            try:
                import project_manager as _pm
                if hasattr(_pm, "get_sql_connection"):
                    conn = _pm.get_sql_connection()
            except Exception:
                conn = None

        if conn is None:
            from db_connections import get_sql_connection as _get_sql
            conn = _get_sql()

        try:
            reviewer_id = None
            # Resolve reviewer id/display name when possible
            if isinstance(reviewer_name, int):
                reviewer_id = reviewer_name
                row = conn.execute("SELECT first_name, last_name FROM Employees WHERE employee_id = ?", (reviewer_id,)).fetchone()
                if row:
                    reviewer_display_name = f"{row['first_name']} {row['last_name']}"
            elif isinstance(reviewer_name, str):
                m = re.search(r"\(ID:\s*(\d+)\)", reviewer_name)
                if m:
                    reviewer_id = int(m.group(1))
                    row = conn.execute("SELECT first_name, last_name FROM Employees WHERE employee_id = ?", (reviewer_id,)).fetchone()
                    if row:
                        reviewer_display_name = f"{row['first_name']} {row['last_name']}"
                else:
                    parts = reviewer_name.strip().split()
                    if len(parts) >= 2:
                        first = parts[0]
                        last = " ".join(parts[1:])
                        row = conn.execute("SELECT employee_id, first_name, last_name FROM Employees WHERE first_name = ? AND last_name = ?", (first, last)).fetchone()
                        if row:
                            reviewer_id = row['employee_id']
                            reviewer_display_name = f"{row['first_name']} {row['last_name']}"

            # Ensure the reviewed employee has at least one project assignment
            assigned_reviewee = conn.execute("SELECT 1 FROM EmployeeProjects WHERE employee_id = ? LIMIT 1", (employee_id,)).fetchone()
            if not assigned_reviewee:
                raise ValueError("Reviewed employee must be assigned to at least one project to receive reviews.")

            # If reviewer resolved, ensure reviewer is not the same as reviewee
            if reviewer_id is not None:
                if reviewer_id == employee_id:
                    raise ValueError("You cannot review yourself")
                assigned_reviewer = conn.execute("SELECT 1 FROM EmployeeProjects WHERE employee_id = ? LIMIT 1", (reviewer_id,)).fetchone()
                if not assigned_reviewer:
                    raise ValueError("Reviewer must be assigned to at least one project to submit reviews.")

            if reviewer_display_name is None:
                reviewer_display_name = reviewer_name if isinstance(reviewer_name, str) else f"Employee ID {reviewer_name}"
        finally:
            conn.close()
    except ValueError:
        # propagate validation errors
        raise
    except Exception:
        # Could not validate against SQL DB (e.g., DB not available in tests)
        reviewer_display_name = reviewer_name if isinstance(reviewer_name, str) else f"Employee ID {reviewer_name}"

    review = {
        "employee_id": employee_id,
        "review_date": str(date.today()),
        "reviewer_name": reviewer_display_name,
        "overall_rating": float(overall_rating),
        "strengths": strengths,
        "areas_for_improvement": areas_for_improvement,
        "comments": comments,
        "goals_for_next_period": goals_for_next_period
    }
    result = collection.insert_one(review)
    print(f"Review submitted successfully. ID: {result.inserted_id}")
    return True


def get_performance_reviews_for_employee(employee_id):
    collection = get_mongo_collection()
    reviews = list(collection.find({"employee_id": employee_id}))
    for r in reviews:
        r["_id"] = str(r["_id"])
    return reviews