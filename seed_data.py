import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from db_connections import init_sql_db, get_sql_connection, get_mongo_collection

print("Setting up databases...")

# Step 1 - Create all SQLite tables
init_sql_db()

# Step 2 - Insert all 30 employees
conn = get_sql_connection()
try:
    conn.execute("""
        INSERT OR IGNORE INTO Employees
        (first_name, last_name, email, hire_date, department) VALUES
        ('Rahul','Sharma','rahul.sharma@company.com','2022-05-12','Engineering'),
        ('Priya','Mehta','priya.mehta@company.com','2023-01-15','Data Science'),
        ('Arjun','Kapoor','arjun.kapoor@company.com','2021-09-30','Product'),
        ('Sneha','Iyer','sneha.iyer@company.com','2022-11-10','HR'),
        ('Vikram','Patel','vikram.patel@company.com','2024-02-20','Engineering'),
        ('Neha','Gupta','neha.gupta@company.com','2023-06-18','Marketing'),
        ('Karan','Shah','karan.shah@company.com','2022-03-11','Finance'),
        ('Aisha','Khan','aisha.khan@company.com','2024-01-05','Data Science'),
        ('Rohit','Agarwal','rohit.agarwal@company.com','2021-12-22','Engineering'),
        ('Meera','Nair','meera.nair@company.com','2023-04-17','HR'),
        ('Aditya','Verma','aditya.verma@company.com','2022-07-09','Engineering'),
        ('Pooja','Singh','pooja.singh@company.com','2024-03-01','Marketing'),
        ('Nikhil','Joshi','nikhil.joshi@company.com','2023-08-14','Product'),
        ('Divya','Menon','divya.menon@company.com','2022-02-28','Finance'),
        ('Siddharth','Rao','siddharth.rao@company.com','2021-10-19','Engineering'),
        ('Ananya','Das','ananya.das@company.com','2024-05-10','Data Science'),
        ('Manish','Chopra','manish.chopra@company.com','2022-12-01','Sales'),
        ('Ritika','Bose','ritika.bose@company.com','2023-09-21','Marketing'),
        ('Harsh','Malhotra','harsh.malhotra@company.com','2021-06-15','Engineering'),
        ('Tanvi','Kulkarni','tanvi.kulkarni@company.com','2024-04-08','HR'),
        ('Aman','Tiwari','aman.tiwari@company.com','2023-03-10','Engineering'),
        ('Kavya','Reddy','kavya.reddy@company.com','2022-08-18','Product'),
        ('Varun','Chatterjee','varun.chatterjee@company.com','2021-11-05','Finance'),
        ('Ishita','Bansal','ishita.bansal@company.com','2024-02-01','Marketing'),
        ('Dev','Arora','dev.arora@company.com','2022-09-25','Engineering'),
        ('Shreya','Mukherjee','shreya.mukherjee@company.com','2023-07-12','HR'),
        ('Rajat','Khanna','rajat.khanna@company.com','2021-05-17','Sales'),
        ('Simran','Gill','simran.gill@company.com','2023-10-02','Data Science'),
        ('Naveen','Pillai','naveen.pillai@company.com','2022-01-30','Engineering'),
        ('Ishaan','Jain','ishaan.jain@gmail.com','2024-03-19','Marketing')
    """)
    conn.commit()
    print("30 employees inserted into SQLite.")
finally:
    conn.close()

# Step 3 - Insert 5 projects
conn = get_sql_connection()
try:
    conn.execute("""
        INSERT OR IGNORE INTO Projects
        (project_name, start_date, end_date, status) VALUES
        ('Website Redesign','2024-01-01','2024-06-30','Active'),
        ('Mobile App Development','2024-02-01',NULL,'Active'),
        ('Data Analytics Platform','2024-03-01','2024-12-31','Planning'),
        ('HR Management System','2024-01-15','2024-09-30','Active'),
        ('Sales Dashboard','2024-04-01',NULL,'Planning')
    """)
    conn.commit()
    print("5 projects inserted into SQLite.")
finally:
    conn.close()

# Step 4 - Insert 10 assignments
conn = get_sql_connection()
try:
    conn.execute("""
        INSERT OR IGNORE INTO EmployeeProjects
        (employee_id, project_id, role, assignment_date) VALUES
        (1, 1, 'Backend Developer','2024-01-10'),
        (2, 3, 'Data Analyst','2024-03-05'),
        (3, 2, 'Product Manager','2024-02-10'),
        (4, 4, 'HR Lead','2024-01-20'),
        (5, 1, 'Frontend Developer','2024-01-12'),
        (6, 5, 'Marketing Analyst','2024-04-05'),
        (7, 5, 'Finance Analyst','2024-04-10'),
        (8, 3, 'ML Engineer','2024-03-08'),
        (9, 2, 'Tech Lead','2024-02-05'),
        (10, 4, 'HR Coordinator','2024-01-25')
    """)
    conn.commit()
    print("10 assignments inserted into SQLite.")
finally:
    conn.close()

# Step 5 - Insert reviews into MongoDB
col = get_mongo_collection()
existing = col.count_documents({})
if existing == 0:
    reviews = [
        {
            'employee_id': 1,
            'review_date': '2024-06-01',
            'reviewer_name': 'Anita Desai',
            'overall_rating': 4.5,
            'strengths': ['Problem solving', 'Team work', 'Code quality'],
            'areas_for_improvement': ['Documentation', 'Meeting deadlines'],
            'comments': 'Rahul has shown great technical skills this quarter.',
            'goals_for_next_period': ['Lead a project', 'Complete AWS certification']
        },
        {
            'employee_id': 2,
            'review_date': '2024-06-05',
            'reviewer_name': 'Suresh Menon',
            'overall_rating': 4.0,
            'strengths': ['Data analysis', 'Python skills', 'Attention to detail'],
            'areas_for_improvement': ['Presentation skills', 'Stakeholder communication'],
            'comments': 'Priya delivers clean and well-documented analysis.',
            'goals_for_next_period': ['Present findings to leadership', 'Learn ML frameworks']
        },
        {
            'employee_id': 3,
            'review_date': '2024-06-10',
            'reviewer_name': 'Anita Desai',
            'overall_rating': 3.5,
            'strengths': ['Product thinking', 'User empathy'],
            'areas_for_improvement': ['Technical knowledge', 'Prioritization'],
            'comments': 'Arjun has good product instincts but needs stronger execution.',
            'goals_for_next_period': ['Complete product management course', 'Improve sprint delivery']
        },
        {
            'employee_id': 4,
            'review_date': '2024-06-12',
            'reviewer_name': 'Ramesh Iyer',
            'overall_rating': 4.2,
            'strengths': ['Communication', 'Policy knowledge', 'Employee relations'],
            'areas_for_improvement': ['Data driven decisions', 'Process automation'],
            'comments': 'Sneha is a reliable HR professional.',
            'goals_for_next_period': ['Implement HRMS module', 'Reduce onboarding time by 20%']
        },
        {
            'employee_id': 5,
            'review_date': '2024-06-15',
            'reviewer_name': 'Anita Desai',
            'overall_rating': 4.8,
            'strengths': ['Backend development', 'Fast learner', 'Problem solving'],
            'areas_for_improvement': ['Frontend skills', 'Client communication'],
            'comments': 'Vikram is one of our strongest engineers.',
            'goals_for_next_period': ['Mentor junior developers', 'Lead backend architecture']
        },
        {
            'employee_id': 6,
            'review_date': '2024-06-18',
            'reviewer_name': 'Suresh Menon',
            'overall_rating': 3.8,
            'strengths': ['Creativity', 'Campaign management'],
            'areas_for_improvement': ['Data analysis', 'Budget management'],
            'comments': 'Neha brings creative energy to the marketing team.',
            'goals_for_next_period': ['Learn Google Analytics', 'Run independent campaign']
        },
        {
            'employee_id': 7,
            'review_date': '2024-06-20',
            'reviewer_name': 'Ramesh Iyer',
            'overall_rating': 4.1,
            'strengths': ['Financial analysis', 'Accuracy', 'Reporting'],
            'areas_for_improvement': ['Communication', 'Automation tools'],
            'comments': 'Karan is thorough and reliable in financial work.',
            'goals_for_next_period': ['Learn Power BI', 'Automate monthly reports']
        },
        {
            'employee_id': 8,
            'review_date': '2024-06-22',
            'reviewer_name': 'Suresh Menon',
            'overall_rating': 4.3,
            'strengths': ['Machine learning', 'Research', 'Python'],
            'areas_for_improvement': ['Deployment skills', 'Documentation'],
            'comments': 'Aisha shows strong research and ML capabilities.',
            'goals_for_next_period': ['Deploy first ML model', 'Write technical blog']
        },
        {
            'employee_id': 9,
            'review_date': '2024-06-25',
            'reviewer_name': 'Anita Desai',
            'overall_rating': 4.6,
            'strengths': ['System design', 'Debugging', 'Mentoring'],
            'areas_for_improvement': ['Frontend knowledge', 'Agile practices'],
            'comments': 'Rohit is a senior engineer who consistently delivers.',
            'goals_for_next_period': ['Complete system design course', 'Lead architecture review']
        },
        {
            'employee_id': 10,
            'review_date': '2024-06-28',
            'reviewer_name': 'Ramesh Iyer',
            'overall_rating': 4.0,
            'strengths': ['Recruitment', 'Onboarding', 'Employee engagement'],
            'areas_for_improvement': ['HR analytics', 'Policy documentation'],
            'comments': 'Meera handles recruitment and onboarding effectively.',
            'goals_for_next_period': ['Implement HR analytics dashboard', 'Update policy documents']
        }
    ]
    result = col.insert_many(reviews)
    print(f"10 reviews inserted into MongoDB.")
else:
    print(f"MongoDB already has {existing} reviews. Skipping insert.")

print("\nAll done. Your databases are ready.")
print("Run 'python main.py' to start the app.")