import psycopg2

from helper import PostgresqlOperations

connection_params = {
    'user': 'postgres',
    'password': 'wtpsydneymetro2023',
    'host': '34.151.111.183',
    'port': '5432',
    'database': 'shift-progress-data'
}

connection = psycopg2.connect(**connection_params)
cursor = connection.cursor()

postgres_op = PostgresqlOperations()

if connection:
    postgres_op.create_dummy_tables_in_cloud_sql()

