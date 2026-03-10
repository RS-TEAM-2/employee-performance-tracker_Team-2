# Employee Performance Tracker

This project provides a small employee/project/performance tracker using SQLite for primary storage and optionally MongoDB for storing reviews.

## Quick overview
- **What:** seedable SQLite DB with `Employees`, `Projects`, and `EmployeeProjects` tables.
- **Where:** SQLite DB file `company.db` in the project root (see `sqlite_connection.py` or `db_connections.py`).
- **Mongo:** Mongo logic is optional — check `db_connections.py` and `seed_data.py` for Mongo usage.

## Prerequisites
- Python 3.8+ installed
- (Optional) MongoDB running and `MONGO_URI` set in a `.env` file if you want Mongo seeding

## Setup (local)
1. Create and activate a virtual environment:
```bash
python -m venv .venv
# PowerShell
.venv\Scripts\Activate.ps1
# CMD
.venv\Scripts\activate.bat
# macOS / Linux
source .venv/bin/activate
```
2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Initialize and seed the database
- To create tables and insert the sample data run the seeder script:
```bash
python seed_data.py
```
- The seeder creates the SQLite tables, inserts employees/projects/assignments, and (optionally) inserts review documents into MongoDB if `MONGO_URI` is set.

## Run the application
- To run the console/CLI app:
```bash
python main.py
```
- To run the Streamlit UI:
```bash
streamlit run app.py
```

## Verify seeded data
- Check tables and rows in SQLite:
```bash
python -m connections.check_tables   # show tables
python -m connections.check_data     # prints Employees rows
```

## Notes
- SQLite is file-based; the project uses Python's built-in `sqlite3` module. The database is the file `company.db` — there is no separate SQLite server to configure.
- There are two DB helper modules in the repo: `db_connections.py` at the repo root (used by `seed_data.py` and `main.py`) and `connections/db_connections.py` (used by other parts). Both create tables and provide seeding logic; use the one that matches how you run scripts in your environment.

## Tests
- Run the test suite with:
```bash
pytest
```

## Git: pull & get data (collaborator)
1. Pull and rebase the latest branch:
```bash
git pull origin main --rebase
```
2. Create/activate your virtualenv and install deps (see Setup above).
3. Run the seeder to populate `company.db`:
```bash
python seed_data.py
```
4. Verify with the check scripts above.

If you prefer a non-destructive seeder or want MongoDB seeding behavior changed, update `seed_data.py` or the DB helper modules accordingly.
