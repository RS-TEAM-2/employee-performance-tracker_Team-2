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

def seed_database(force=False):

    conn = get_connection()
    cursor = conn.cursor()

    if not force:
        # Check if data already exists
        cursor.execute("SELECT COUNT(*) FROM Employees")
        count = cursor.fetchone()[0]

        if count > 0:
            print("Database already seeded")
            conn.close()
            return
    else:
        # Force reseed: clear existing data in correct order
        print("Force reseed: clearing existing data...")
        cursor.execute("DELETE FROM EmployeeProjects")
        cursor.execute("DELETE FROM Projects")
        cursor.execute("DELETE FROM Employees")
        # Reset AUTOINCREMENT counters (sqlite_sequence) if present
        try:
            cursor.execute("DELETE FROM sqlite_sequence WHERE name IN ('Employees','Projects','EmployeeProjects')")
        except Exception:
            pass
        conn.commit()

    print("Seeding database with initial data...")
    employees = [
        ("Rahul","Sharma","rahul.sharma@company.com","2022-05-12","Engineering"),
        ("Priya","Mehta","priya.mehta@company.com","2023-01-15","Data Science"),
        ("Arjun","Kapoor","arjun.kapoor@company.com","2021-09-30","Product"),
        ("Sneha","Iyer","sneha.iyer@company.com","2022-11-10","HR"),
        ("Vikram","Patel","vikram.patel@company.com","2024-02-20","Engineering"),
        ("Neha","Gupta","neha.gupta@company.com","2023-06-18","Marketing"),
        ("Karan","Shah","karan.shah@company.com","2022-03-11","Finance"),
        ("Aisha","Khan","aisha.khan@company.com","2024-01-05","Data Science"),
        ("Rohit","Agarwal","rohit.agarwal@company.com","2021-12-22","Engineering"),
        ("Meera","Nair","meera.nair@company.com","2023-04-17","HR"),
        ("Aditya","Verma","aditya.verma@company.com","2022-07-09","Engineering"),
        ("Pooja","Singh","pooja.singh@company.com","2024-03-01","Marketing"),
        ("Nikhil","Joshi","nikhil.joshi@company.com","2023-08-14","Product"),
        ("Divya","Menon","divya.menon@company.com","2022-02-28","Finance"),
        ("Siddharth","Rao","siddharth.rao@company.com","2021-10-19","Engineering"),
        ("Ananya","Das","ananya.das@company.com","2024-05-10","Data Science"),
        ("Manish","Chopra","manish.chopra@company.com","2022-12-01","Sales"),
        ("Ritika","Bose","ritika.bose@company.com","2023-09-21","Marketing"),
        ("Harsh","Malhotra","harsh.malhotra@company.com","2021-06-15","Engineering"),
        ("Tanvi","Kulkarni","tanvi.kulkarni@company.com","2024-04-08","HR"),
        ("Aman","Tiwari","aman.tiwari@company.com","2023-03-10","Engineering"),
        ("Kavya","Reddy","kavya.reddy@company.com","2022-08-18","Product"),
        ("Varun","Chatterjee","varun.chatterjee@company.com","2021-11-05","Finance"),
        ("Ishita","Bansal","ishita.bansal@company.com","2024-02-01","Marketing"),
        ("Dev","Arora","dev.arora@company.com","2022-09-25","Engineering"),
        ("Shreya","Mukherjee","shreya.mukherjee@company.com","2023-07-12","HR"),
        ("Rajat","Khanna","rajat.khanna@company.com","2021-05-17","Sales"),
        ("Simran","Gill","simran.gill@company.com","2023-10-02","Data Science"),
        ("Naveen","Pillai","naveen.pillai@company.com","2022-01-30","Engineering"),
        ("Tanya","Saxena","tanya.saxena@company.com","2024-03-19","Marketing")
    ]

    projects = [
        ("AI Chatbot Development","2024-01-01","2024-06-30","In Progress"),
        ("Sales Data Analytics","2024-02-15","2024-08-15","Planning"),
        ("Employee HR Portal","2023-11-01","2024-03-01","Completed"),
        ("Fraud Detection System","2024-04-01",None,"In Progress"),
        ("Customer Recommendation Engine","2024-01-20","2024-07-20","In Progress"),
        ("Cloud Migration","2023-09-01","2024-02-28","Completed"),
        ("Marketing Campaign Tracker","2024-03-10",None,"Planning"),
        ("Inventory Optimization","2024-02-01","2024-09-01","In Progress"),
        ("Financial Risk Dashboard","2023-12-15","2024-05-30","In Progress"),
        ("Mobile Banking App","2024-04-05",None,"Planning"),
        ("Supply Chain Analytics","2024-01-15","2024-08-01","In Progress"),
        ("HR Analytics Platform","2024-02-10",None,"Planning"),
        ("Social Media Insights Tool","2023-10-01","2024-01-30","Completed"),
        ("AI Resume Screening","2024-03-01",None,"In Progress"),
        ("Customer Support Automation","2024-02-25","2024-09-10","In Progress"),
        ("IoT Device Monitoring","2024-01-10","2024-12-20","In Progress"),
        ("E-commerce Recommendation","2023-11-05","2024-06-10","In Progress"),
        ("Healthcare Data Pipeline","2024-04-15",None,"Planning"),
        ("Cybersecurity Monitoring","2024-02-05","2024-10-30","In Progress"),
        ("Retail Demand Forecasting","2024-03-20","2024-11-15","Planning"),
        ("Smart Traffic Management","2024-01-18","2024-12-01","In Progress"),
        ("Predictive Maintenance System","2024-02-11",None,"Planning"),
        ("Online Learning Platform","2023-12-05","2024-07-15","In Progress"),
        ("Food Delivery Optimization","2024-03-03",None,"Planning"),
        ("Bank Loan Risk Model","2024-01-28","2024-09-20","In Progress"),
        ("Energy Consumption Analytics","2024-02-17","2024-10-25","In Progress"),
        ("Travel Recommendation Engine","2024-03-22",None,"Planning"),
        ("Real Estate Price Prediction","2024-04-02",None,"Planning"),
        ("Healthcare Appointment System","2023-10-15","2024-05-15","In Progress"),
        ("Sports Performance Analytics","2024-02-14","2024-12-10","In Progress")
    ]

    employee_projects = [
        (1,1,'Backend Developer','2024-01-10'),
        (2,2,'Data Analyst','2024-02-20'),
        (3,1,'Product Manager','2024-01-05'),
        (5,4,'ML Engineer','2024-04-02'),
        (4,3,'HR Coordinator','2023-11-05'),
        (6,7,'Marketing Analyst','2024-03-15'),
        (7,9,'Finance Analyst','2024-01-12'),
        (8,5,'Data Scientist','2024-02-01'),
        (9,8,'Software Engineer','2024-02-10'),
        (10,3,'HR Specialist','2023-11-10'),
        (11,16,'Backend Engineer','2024-01-15'),
        (12,7,'Marketing Executive','2024-03-20'),
        (13,14,'Product Analyst','2024-03-05'),
        (14,9,'Financial Analyst','2024-01-18'),
        (15,19,'Security Engineer','2024-02-10'),
        (16,18,'Data Scientist','2024-04-20'),
        (17,20,'Sales Manager','2024-03-22'),
        (18,7,'Marketing Strategist','2024-03-25'),
        (19,11,'Software Developer','2024-01-20'),
        (20,12,'HR Analyst','2024-02-28'),
        (21,21,'Software Engineer','2024-01-30'),
        (22,23,'Product Manager','2024-02-15'),
        (23,25,'Finance Analyst','2024-02-20'),
        (24,24,'Marketing Analyst','2024-03-05'),
        (25,26,'Backend Developer','2024-02-25'),
        (26,12,'HR Specialist','2024-03-10'),
        (27,20,'Sales Executive','2024-03-18'),
        (28,5,'Data Scientist','2024-02-12'),
        (29,21,'Software Engineer','2024-01-25'),
        (30,24,'Marketing Coordinator','2024-03-22')
    ]

    cursor.executemany(
        """
        INSERT INTO Employees(first_name,last_name,email,hire_date,department)
        VALUES(?,?,?,?,?)
    """, employees)

    cursor.executemany(
        """
        INSERT INTO Projects(project_name,start_date,end_date,status)
        VALUES(?,?,?,?)
    """, projects)

    cursor.executemany(
        """
        INSERT INTO EmployeeProjects(employee_id,project_id,role,assignment_date)
        VALUES(?,?,?,?)
    """, employee_projects)

    conn.commit()
    conn.close()

    print("Seed data inserted")