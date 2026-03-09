from connections.db_connections import initialize_database, seed_database


def main():
    initialize_database()
    seed_database(force=True)
    print("Database is ready")


if __name__ == "__main__":
    main()