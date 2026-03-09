from db_connections import init_sql_db
from employee_manager import add_employee, get_employee_by_id, list_all_employees
from project_manager import add_project, assign_employee_to_project, get_projects_for_employee
from performance_reviewer import submit_performance_review, get_performance_reviews_for_employee
from reports import generate_employee_project_report, generate_employee_performance_summary


def show_menu():
    print("\n" + "="*40)
    print("  Employee Performance Tracker")
    print("="*40)
    print("1.  Add Employee")
    print("2.  Add Project")
    print("3.  Assign Employee to Project")
    print("4.  Submit Performance Review")
    print("5.  View Employee Projects")
    print("6.  View Employee Performance")
    print("7.  Generate Full Project Report")
    print("8.  List All Employees")
    print("9.  Get Employee By ID")
    print("10. Exit")
    print("="*40)


def main():
    init_sql_db()

    while True:
        show_menu()
        choice = input("Enter choice (1-10): ").strip()

        if choice == "1":
            print("\n--- Add New Employee ---")
            fn = input("First Name       : ")
            ln = input("Last Name        : ")
            em = input("Email            : ")
            hd = input("Hire Date (YYYY-MM-DD): ")
            dp = input("Department       : ")
            try:
                add_employee(fn, ln, em, hd, dp)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "2":
            print("\n--- Add New Project ---")
            pn = input("Project Name     : ")
            sd = input("Start Date (YYYY-MM-DD): ")
            ed = input("End Date (leave blank if none): ").strip()
            st = input("Status (leave blank for Planning): ").strip()
            add_project(pn, sd, ed or None, st or "Planning")

        elif choice == "3":
            print("\n--- Assign Employee to Project ---")
            try:
                ei = int(input("Employee ID: "))
                pi = int(input("Project ID : "))
                ro = input("Role       : ")
                assign_employee_to_project(ei, pi, ro)
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "4":
            print("\n--- Submit Performance Review ---")
            try:
                ei  = int(input("Employee ID          : "))
                rn  = input("Reviewer Name        : ")
                rt  = float(input("Rating (1.0 - 5.0)   : "))
                st  = input("Strengths (comma separated)       : ").split(",")
                ai  = input("Areas to Improve (comma separated): ").split(",")
                cm  = input("Comments             : ")
                gl  = input("Goals (comma separated)           : ").split(",")
                submit_performance_review(
                    ei, rn, rt,
                    [s.strip() for s in st],
                    [a.strip() for a in ai],
                    cm,
                    [g.strip() for g in gl]
                )
            except Exception as e:
                print(f"Error: {e}")

        elif choice == "5":
            print("\n--- View Employee Projects ---")
            try:
                ei = int(input("Employee ID: "))
                projects = get_projects_for_employee(ei)
                if not projects:
                    print("No projects found for this employee.")
                else:
                    print(f"\n{'Project':<25} {'Role':<20} {'Assigned':<12} {'Status'}")
                    print("-"*70)
                    for p in projects:
                        print(f"{p['project_name']:<25} {p['role']:<20} {p['assignment_date']:<12} {p['status']}")
            except ValueError as e:
                print(f"Error: {e}")

        elif choice == "6":
            print("\n--- View Employee Performance ---")
            try:
                ei = int(input("Employee ID: "))
                generate_employee_performance_summary(ei)
            except ValueError:
                print("Please enter a valid employee ID.")

        elif choice == "7":
            print("\n--- Full Project Report ---")
            generate_employee_project_report()

        elif choice == "8":
            print("\n--- All Employees ---")
            employees = list_all_employees()
            if not employees:
                print("No employees found.")
            else:
                print(f"\n{'ID':<5} {'First Name':<15} {'Last Name':<15} {'Department':<20} {'Hire Date'}")
                print("-"*70)
                for e in employees:
                    print(f"{e['employee_id']:<5} {e['first_name']:<15} {e['last_name']:<15} {e['department']:<20} {e['hire_date']}")

        elif choice == "9":
            print("\n--- Get Employee By ID ---")
            try:
                ei = int(input("Employee ID: "))
                emp = get_employee_by_id(ei)
                if emp is None:
                    print("No employee found with that ID.")
                else:
                    print(f"\nID         : {emp['employee_id']}")
                    print(f"Name       : {emp['first_name']} {emp['last_name']}")
                    print(f"Email      : {emp['email']}")
                    print(f"Department : {emp['department']}")
                    print(f"Hire Date  : {emp['hire_date']}")
            except ValueError:
                print("Please enter a valid number.")

        elif choice == "10":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 10.")


if __name__ == "__main__":
    main()