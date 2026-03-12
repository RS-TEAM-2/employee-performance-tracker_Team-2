import sqlite3
import os
from pymongo import MongoClient
from dotenv import load_dotenv
import certifi

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

    # Build MongoClient kwargs to ensure proper TLS CA is used for Atlas
    kwargs = {"serverSelectionTimeoutMS": 20000}

    # For SRV URIs and Atlas connections, ensure TLS and provide certifi CA bundle
    try:
        if uri.startswith("mongodb+srv://") or os.getenv("MONGO_TLS", "true").lower() == "true":
            kwargs["tls"] = True
            kwargs["tlsCAFile"] = certifi.where()
    except Exception:
        # certifi may not be available; leave kwargs as-is and let MongoClient error surface
        pass

    # Allow bypassing certificate verification for debugging (NOT recommended)
    if os.getenv("MONGO_ALLOW_INVALID_CERTS", "false").lower() in ("1", "true", "yes"):
        kwargs["tlsAllowInvalidCertificates"] = True

    try:
        client = MongoClient(uri, **kwargs)
        # Verify the connection early to fail fast with a clear error
        client.admin.command("ping")
    except Exception as e:
        # Connection failed; attempt to fallback to mongomock and warn instead of
        # crashing the entire app. This keeps local dev functional when Atlas is
        # unreachable or TLS fails.
        try:
            import warnings
            warnings.warn(f"MongoDB connection failed: {e}. Falling back to in-memory mongomock.")
        except Exception:
            pass
        try:
            import mongomock
            client = mongomock.MongoClient()
            db = client["dev_performance_reviews_db"]
            return db["reviews"]
        except Exception:
            msg = (
                f"Failed to connect to MongoDB at {uri!r}: {e}\n"
                "Possible causes: network/DNS issues, incorrect MONGO_URI, or TLS/SSL handshake problems.\n"
                "Suggestions: \n"
                " - Ensure your environment variable MONGO_URI is set and correct.\n"
                " - If you are using MongoDB Atlas, make sure your Python/OpenSSL supports TLS 1.2+.\n"
                " - Update the 'certifi' package (`pip install -U certifi`) so the driver can verify Atlas certificates.\n"
                " - For temporary debugging only, set MONGO_ALLOW_INVALID_CERTS=true to bypass certificate verification (not recommended).\n"
            )
            raise ConnectionError(msg) from e

    db = client["performance_reviews_db"]
    return db["reviews"]