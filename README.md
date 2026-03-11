# Employee Performance Tracking System

A full-stack Python application for managing employee records, project assignments, and performance reviews using a hybrid SQLite + MongoDB Atlas database architecture.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.14 |
| SQL Database | SQLite (local file) |
| NoSQL Database | MongoDB Atlas (cloud) |
| Web UI | Streamlit |
| Testing | pytest + pytest-cov |
| Version Control | Git + GitHub |

---

## Project Structure

```
employee-tracker/
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_db_connections.py
│   ├── test_employee_manager.py
│   ├── test_project_manager.py
│   └── test_performance_reviewer.py
├── db_connections.py        # SQLite + MongoDB connection setup
├── employee_manager.py      # Employee CRUD operations
├── project_manager.py       # Project and assignment operations
├── performance_reviewer.py  # MongoDB performance review operations
├── reports.py               # Cross-database reports
├── main.py                  # Terminal menu interface
├── app.py                   # Streamlit web interface
├── seed_data.py             # Database seeding script
├── requirements.txt
├── .env                     # Not committed — see setup below
└── .gitignore
```

---

## Prerequisites

- Python 3.8 or higher
- A MongoDB Atlas account (free M0 cluster)
- Git

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/employee-tracker.git
cd employee-tracker
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate — Windows
venv\Scripts\activate

# Activate — Mac/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MongoDB Atlas

Create a `.env` file in the root folder:

```
MONGO_URI=mongodb+srv://<username>:<password>@<cluster>.mongodb.net/?retryWrites=true&w=majority
```

Replace `<username>`, `<password>`, and `<cluster>` with your Atlas credentials.

> **Note:** The `.env` file is listed in `.gitignore` and is never committed to GitHub. Each developer must create their own local copy with the shared credentials.

### 5. Seed the Databases

```bash
python seed_data.py
```

This creates all SQLite tables, inserts 30 employees, 5 projects, 10 assignments, and 10 MongoDB performance reviews.

---

## Running the Application

### Web Interface (Streamlit)

```bash
streamlit run app.py
```

Opens automatically in your browser at `http://localhost:8501`

### Terminal Interface

```bash
python main.py
```

---

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage report
pytest tests/ -v --cov=. --cov-report term-missing
```

**Test Results:** 28 tests passing | Core module coverage 88–100%

---

## Features

- **Employees** — Add and view all employees
- **Projects** — Create projects and assign employees with roles
- **Performance Reviews** — Submit and view reviews stored in MongoDB
- **Reports** — Full project assignment report and employee performance summary

---

## Data Storage

| Data | Storage | Location |
|---|---|---|
| Employees, Projects, Assignments | SQLite | `company.db` (local) |
| Performance Reviews | MongoDB | Atlas cloud |
| Secrets | `.env` | Local only, never committed |

---

## MongoDB Atlas Setup (New Team Member)

1. Go to [mongodb.com/atlas](https://mongodb.com/atlas) and log in
2. Navigate to your cluster → **Connect** → **Drivers**
3. Copy the connection string
4. Create `.env` in the project root with `MONGO_URI=<your connection string>`
5. Run `python seed_data.py`

---

## Team Workflow

```bash
# Daily sync
git checkout main
git pull origin main
git checkout feature/your-branch
git merge main

# Push your work
git add .
git commit -m "your message"
git push origin feature/your-branch
```

## Notes
- SQLite is file-based; the project uses Python's built-in `sqlite3` module. The database is the file `company.db` — there is no separate SQLite server to configure.
- There are two DB helper modules in the repo: `db_connections.py` at the repo root (used by `seed_data.py` and `main.py`) and `connections/db_connections.py` (used by other parts). Both create tables and provide seeding logic; use the one that matches how you run scripts in your environment.
- Never push directly to `main`. Always work on a feature branch and submit a pull request.