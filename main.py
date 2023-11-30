import psycopg2
from pathlib import Path

connection_params = {
    'user': 'postgres',
    'password': 'wtpsydneymetro2023',
    'host': '34.151.111.183',
    'port': '5432',
    'database': 'shift-progress-data'
}

connection = psycopg2.connect(**connection_params)
cursor = connection.cursor()

if connection:
    print("Connection successful. Queries running......")

# One-time read of sql file
with open('createMock.sql', 'r') as file:
    queries = file.read()

commands = queries.split(';') 

for command in commands[:-1]:
    try:
        cursor.execute(f'{command}')
        connection.commit()

    except psycopg2.Error as e:
        print(f"Error: {e} for {command}")
        connection.rollback() 

print("Dummy postgres tables created.")

cursor.close()
connection.close()


