import pytest
import sqlite3
import mongomock
from db_connections import create_sql_tables

@pytest.fixture
def mock_sql_db(monkeypatch):
    """Creates an in-memory SQLite database for testing."""
    conn = sqlite3.connect(":memory:")
    # Create the required tables in the temporary memory db [cite: 79, 80]
    create_sql_tables(conn) 
    
    # Patch the connection getter to use our in-memory db instead of company.db
    monkeypatch.setattr("db_connections.get_sql_connection", lambda: sqlite3.connect(":memory:"))
    return conn

@pytest.fixture
def mock_nosql_db(monkeypatch):
    """Mocks MongoDB using mongomock to avoid needing a live Atlas connection."""
    client = mongomock.MongoClient()
    db = client.performance_reviews_db
    collection = db.reviews
    
    # Patch the MongoDB connection getter [cite: 82]
    monkeypatch.setattr("db_connections.get_nosql_collection", lambda: collection)
    return collection