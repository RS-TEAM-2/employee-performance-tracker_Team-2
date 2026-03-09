from connections.sqlite_connection import get_connection

conn = get_connection()
cursor = conn.cursor()

cursor.execute("SELECT * FROM Employees")

for row in cursor.fetchall():
    print(row)

conn.close()