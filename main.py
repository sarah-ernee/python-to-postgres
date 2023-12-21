import psycopg2

from helper import PostgresqlOperations


postgres_op = PostgresqlOperations()

if postgres_op.sql_conn:
    postgres_op.create_dummy_tables_in_cloud_sql()


