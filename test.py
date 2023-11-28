import psycopg2

from helper import PostgresqlOperations
from tabulate import tabulate

# Employ class functions to run postgresql queries
db = PostgresqlOperations()

conn = db.connection
curr = conn.cursor()

db.create_table()
db.populate_table()
db.update_table()

# db.clear_table()
# db.delete_table()

# Fetching all rows from the created table
curr.execute("SELECT * from coordinators;")
data = curr.fetchall()

headers = ["ID", "Name", "Topic"]
results = []

for row in data:
    results.append(row)

print(tabulate(results, headers=headers, tablefmt="grid")) # or psql fmt


db.close_postgresql_connection()
