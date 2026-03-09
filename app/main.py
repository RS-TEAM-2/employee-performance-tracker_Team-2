from connections.db_connections import initialize_database


def main():
    initialize_database()
    print("Database initialized successfully")


if __name__ == "__main__":
    main()