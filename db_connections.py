import sqlite3
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "company.db")


def get_sql_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


def init_sql_db():
    conn = get_sql_connection()
    try:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS Employees (
                employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name  TEXT NOT NULL,
                last_name   TEXT NOT NULL,
                email       TEXT NOT NULL UNIQUE,
                hire_date   TEXT NOT NULL,
                department  TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS Projects (
                project_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                project_name TEXT NOT NULL,
                start_date   TEXT NOT NULL,
                end_date     TEXT,
                status       TEXT DEFAULT 'Planning'
            );

            CREATE TABLE IF NOT EXISTS EmployeeProjects (
                assignment_id   INTEGER PRIMARY KEY AUTOINCREMENT,
                employee_id     INTEGER NOT NULL,
                project_id      INTEGER NOT NULL,
                role            TEXT NOT NULL,
                assignment_date TEXT NOT NULL,
                FOREIGN KEY (employee_id) REFERENCES Employees(employee_id),
                FOREIGN KEY (project_id)  REFERENCES Projects(project_id)
            );
        """)
        conn.commit()
        print("SQLite tables ready.")
    finally:
        conn.close()


def get_mongo_collection():
    uri = os.getenv("MONGO_URI")
    if not uri:
        raise ValueError("MONGO_URI not found. Check your .env file.")
    client = MongoClient(uri)
    db = client["performance_reviews_db"]
    return db["reviews"]