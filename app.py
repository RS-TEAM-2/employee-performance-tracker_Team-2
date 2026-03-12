# importing necessary Libraries

import streamlit as st
from employee_manager import add_employee, list_all_employees, get_employee_by_id
from project_manager import add_project, assign_employee_to_project, get_projects_for_employee
from performance_reviewer import submit_performance_review, get_performance_reviews_for_employee
from reports import generate_employee_project_report, generate_employee_performance_summary
from db_connections import init_sql_db, get_sql_connection, get_mongo_collection
import pandas as pd
import re

init_sql_db()

st.set_page_config(page_title="Employee Performance Tracker", layout="wide")

# --- Simple Gmail-based authentication ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_email = ""
if 'hide_login_ui' not in st.session_state:
    st.session_state.hide_login_ui = False

def is_valid_gmail(email: str) -> bool:
    if not email or '@' not in email:
        return False
    local, _, domain = email.partition('@')
    return domain.lower() == 'gmail.com' and len(local) > 0


def is_valid_email(email: str) -> bool:
    if not email or '@' not in email:
        return False
    email = email.strip()
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return re.match(pattern, email) is not None

def show_login():
    # if another run set this flag, don't render the login UI
    if st.session_state.get('hide_login_ui'):
        return
    login_container = st.container()
    with login_container:
        st.title("Sign in")
        st.write("Sign in with your Gmail account to access the Employee Performance Tracker.")
        with st.form("login_form"):
            email = st.text_input("Gmail address")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign in")
            if submitted:
                if is_valid_gmail(email):
                    st.session_state.logged_in = True
                    st.session_state.user_email = email
                    st.session_state.hide_login_ui = True
                    # remove the login UI immediately in this run
                    login_container.empty()
                else:
                    st.error("Please enter a valid Gmail address (example@gmail.com).")

# If not logged-in, show login and stop further rendering
if not st.session_state.logged_in:
    show_login()
    if not st.session_state.logged_in:
        st.stop()

# Sidebar sign-out + info
with st.sidebar:
    st.write(f"Signed in: {st.session_state.user_email}")
    if st.button("Sign out"):
        st.session_state.logged_in = False
        st.session_state.user_email = ""
        st.session_state.hide_login_ui = False
        st.success("Signed out")

st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Employees", "Projects", "Performance Reviews", "Reports"])

# ─────────────────────────────────────────────
# PAGE 1 — EMPLOYEES
# ─────────────────────────────────────────────
if page == "Employees":
    st.title("Employees")

    tab1, tab2 = st.tabs(["View Employees", "Add Employee"])

    with tab1:
        st.subheader("All Employees")
        employees = list_all_employees()
        if employees:
            df = pd.DataFrame(employees)
            df.columns = ["ID", "First Name", "Last Name", "Email", "Hire Date", "Department"]
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total employees: {len(df)}")
        else:
            st.info("No employees found. Add some using the Add Employee tab.")

    with tab2:
        st.subheader("Add New Employee")
        with st.form("add_employee_form"):
            col1, col2 = st.columns(2)
            with col1:
                first_name = st.text_input("First Name")
                email      = st.text_input("Email")
                department = st.selectbox("Department", [
                    "Engineering", "Data Science", "Product", "HR",
                    "Marketing", "Finance", "Sales"
                ])
            with col2:
                last_name  = st.text_input("Last Name")
                hire_date  = st.date_input("Hire Date")

            submitted = st.form_submit_button("Add Employee")
            if submitted:
                # normalize inputs
                first_name = first_name.strip()
                last_name = last_name.strip()
                email = email.strip()

                if not first_name or not last_name or not email:
                    st.error("Please fill in all fields.")
                elif not is_valid_email(email):
                    st.error("Please enter a valid email address.")
                else:
                    try:
                        add_employee(first_name, last_name, email, str(hire_date), department)
                        st.success(f"Employee {first_name} {last_name} added successfully.")
                    except ValueError as e:
                        st.error(str(e))

# ─────────────────────────────────────────────
# PAGE 2 — PROJECTS
# ─────────────────────────────────────────────
elif page == "Projects":
    st.title("Projects")

    tab1, tab2, tab3 = st.tabs(["View Projects", "Add Project", "Assign Employee"])

    with tab1:
        st.subheader("All Projects")
        conn = get_sql_connection()
        try:
            rows = conn.execute("SELECT * FROM Projects ORDER BY start_date DESC").fetchall()
        finally:
            conn.close()

        if rows:
            df = pd.DataFrame([dict(r) for r in rows])
            df.columns = ["ID", "Project Name", "Start Date", "End Date", "Status"]
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total projects: {len(df)}")
        else:
            st.info("No projects found. Add one using the Add Project tab.")

    with tab2:
        st.subheader("Add New Project")
        with st.form("add_project_form"):
            col1, col2 = st.columns(2)
            with col1:
                project_name = st.text_input("Project Name")
                start_date   = st.date_input("Start Date")
            with col2:
                status   = st.selectbox("Status", ["Planning", "Active", "Completed", "On Hold"])
                end_date = st.date_input("End Date (optional)", value=None)

            submitted = st.form_submit_button("Add Project")
            if submitted:
                project_name = project_name.strip()
                if not project_name:
                    st.error("Please enter a project name.")
                elif end_date and start_date > end_date:
                    st.error("Start date cannot be after the end date.")
                else:
                    try:
                        add_project(project_name, str(start_date),
                                    str(end_date) if end_date else None, status)
                        st.success(f"Project '{project_name}' added successfully.")
                    except ValueError as ve:
                        st.error(str(ve))
                    except Exception as e:
                        st.error(str(e))

    with tab3:
        st.subheader("Assign Employee to Project")
        employees = list_all_employees()
        conn = get_sql_connection()
        try:
            projects = conn.execute("SELECT project_id, project_name FROM Projects").fetchall()
        finally:
            conn.close()

        if not employees:
            st.warning("No employees found. Please add employees first.")
        elif not projects:
            st.warning("No projects found. Please add a project first.")
        else:
            emp_options  = {f"{e['first_name']} {e['last_name']} (ID: {e['employee_id']})": e['employee_id'] for e in employees}
            proj_options = {f"{p['project_name']} (ID: {p['project_id']})": p['project_id'] for p in projects}

            with st.form("assign_form"):
                selected_emp  = st.selectbox("Select Employee", list(emp_options.keys()))
                selected_proj = st.selectbox("Select Project",  list(proj_options.keys()))
                role          = st.text_input("Role")

                submitted = st.form_submit_button("Assign")
                if submitted:
                    if not role:
                        st.error("Please enter a role.")
                    else:
                        try:
                            assign_employee_to_project(
                                emp_options[selected_emp],
                                proj_options[selected_proj],
                                role
                            )
                            st.success("Employee assigned successfully.")
                        except ValueError as e:
                            st.error(str(e))

            st.subheader("View Employee Assignments")
            selected_emp2 = st.selectbox("Select Employee to view projects",
                                          list(emp_options.keys()), key="view_emp")
            emp_id = emp_options[selected_emp2]
            projs  = get_projects_for_employee(emp_id)
            if projs:
                df = pd.DataFrame(projs)
                df = df[["project_name", "role", "assignment_date", "status"]]
                df.columns = ["Project", "Role", "Assigned Date", "Status"]
                st.dataframe(df, use_container_width=True)
            else:
                st.info("This employee has no project assignments yet.")

# ─────────────────────────────────────────────
# PAGE 3 — PERFORMANCE REVIEWS
# ─────────────────────────────────────────────
elif page == "Performance Reviews":
    st.title("Performance Reviews")

    tab1, tab2 = st.tabs(["View Reviews", "Submit Review"])

    with tab1:
        st.subheader("Employee Performance Reviews")
        employees = list_all_employees()
        if not employees:
            st.warning("No employees found.")
        else:
            emp_options = {f"{e['first_name']} {e['last_name']} (ID: {e['employee_id']})": e['employee_id'] for e in employees}
            selected    = st.selectbox("Select Employee", list(emp_options.keys()))
            emp_id      = emp_options[selected]
            reviews     = get_performance_reviews_for_employee(emp_id)

            if reviews:
                avg_rating = sum(r["overall_rating"] for r in reviews) / len(reviews)
                col1, col2 = st.columns(2)
                col1.metric("Total Reviews", len(reviews))
                col2.metric("Average Rating", f"{avg_rating:.1f} / 5.0")

                for i, r in enumerate(reviews, 1):
                    with st.expander(f"Review {i} — {r['review_date']} by {r['reviewer_name']}"):
                        st.write(f"**Rating:** {r['overall_rating']} / 5.0")
                        st.write(f"**Strengths:** {', '.join(r['strengths'])}")
                        st.write(f"**Areas to Improve:** {', '.join(r['areas_for_improvement'])}")
                        st.write(f"**Comments:** {r['comments']}")
                        st.write(f"**Goals:** {', '.join(r['goals_for_next_period'])}")
            else:
                st.info("No reviews found for this employee.")

    with tab2:
        st.subheader("Submit Performance Review")
        employees = list_all_employees()
        if not employees:
            st.warning("No employees found. Please add employees first.")
        else:
            emp_options = {f"{e['first_name']} {e['last_name']} (ID: {e['employee_id']})": e['employee_id'] for e in employees}

            with st.form("review_form"):
                selected_reviewee = st.selectbox("Select Employee", list(emp_options.keys()))
                # Reviewer should be chosen from existing employees
                reviewer_options = {f"{e['first_name']} {e['last_name']} (ID: {e['employee_id']})": e['employee_id'] for e in employees}
                selected_reviewer = st.selectbox("Reviewer", list(reviewer_options.keys()))
                rating        = st.slider("Overall Rating", 1.0, 5.0, 3.0, step=0.5)

                col1, col2 = st.columns(2)
                with col1:
                    strengths = st.text_area("Strengths (one per line)")
                    comments  = st.text_area("Comments")
                with col2:
                    improvements = st.text_area("Areas to Improve (one per line)")
                    goals        = st.text_area("Goals for Next Period (one per line)")

                submitted = st.form_submit_button("Submit Review")
                if submitted:
                    if not selected_reviewer or not strengths or not improvements or not goals:
                        st.error("Please fill in all fields.")
                    else:
                        try:
                            reviewer_id = reviewer_options[selected_reviewer]
                            # quick client-side check: ensure reviewer has at least one assignment
                            reviewer_projects = get_projects_for_employee(reviewer_id)
                            if not reviewer_projects:
                                st.error("Selected reviewer has no project assignments and cannot submit reviews.")
                            else:
                                submit_performance_review(
                                    emp_options[selected_reviewee],
                                    reviewer_id,
                                    rating,
                                    [s.strip() for s in strengths.splitlines() if s.strip()],
                                    [a.strip() for a in improvements.splitlines() if a.strip()],
                                    comments,
                                    [g.strip() for g in goals.splitlines() if g.strip()]
                                )
                                st.success("Review submitted successfully.")
                        except Exception as e:
                            st.error(str(e))

# ─────────────────────────────────────────────
# PAGE 4 — REPORTS
# ─────────────────────────────────────────────
elif page == "Reports":
    st.title("Reports")

    tab1, tab2 = st.tabs(["Project Assignment Report", "Employee Performance Summary"])

    with tab1:
        st.subheader("Full Project Assignment Report")
        conn = get_sql_connection()
        try:
            rows = conn.execute("""
                SELECT e.first_name || ' ' || e.last_name AS employee_name,
                       p.project_name, ep.role, ep.assignment_date, p.status
                FROM EmployeeProjects ep
                JOIN Employees e ON ep.employee_id = e.employee_id
                JOIN Projects p  ON ep.project_id  = p.project_id
                ORDER BY e.first_name
            """).fetchall()
        finally:
            conn.close()

        if rows:
            df = pd.DataFrame([dict(r) for r in rows])
            df.columns = ["Employee", "Project", "Role", "Assigned Date", "Status"]
            st.dataframe(df, use_container_width=True)
            st.caption(f"Total assignments: {len(df)}")
        else:
            st.info("No assignments found.")

    with tab2:
        st.subheader("Employee Performance Summary")
        employees = list_all_employees()
        if not employees:
            st.warning("No employees found.")
        else:
            emp_options = {f"{e['first_name']} {e['last_name']} (ID: {e['employee_id']})": e['employee_id'] for e in employees}
            selected    = st.selectbox("Select Employee", list(emp_options.keys()))
            emp_id      = emp_options[selected]
            emp         = get_employee_by_id(emp_id)
            reviews     = get_performance_reviews_for_employee(emp_id)

            st.markdown(f"**Name:** {emp['first_name']} {emp['last_name']}")
            st.markdown(f"**Department:** {emp['department']}")
            st.markdown(f"**Hire Date:** {emp['hire_date']}")
            st.divider()

            if reviews:
                avg = sum(r["overall_rating"] for r in reviews) / len(reviews)
                col1, col2 = st.columns(2)
                col1.metric("Total Reviews", len(reviews))
                col2.metric("Average Rating", f"{avg:.1f} / 5.0")

                latest = reviews[-1]
                st.markdown(f"**Latest Reviewer:** {latest['reviewer_name']}")
                st.markdown(f"**Strengths:** {', '.join(latest['strengths'])}")
                st.markdown(f"**Areas to Improve:** {', '.join(latest['areas_for_improvement'])}")
                st.markdown(f"**Comments:** {latest['comments']}")
                st.markdown(f"**Goals:** {', '.join(latest['goals_for_next_period'])}")
            else:
                st.info("No reviews found for this employee.")