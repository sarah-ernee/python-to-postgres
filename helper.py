import psycopg2
from psycopg2.extras import execute_values

class PostgresqlOperations:
    def __init__(self):
        self.connection = psycopg2.connect(
            database="postgres",
            user="postgres",
            host="localhost",
            password="dsn",
            port=5432
        )
        self.cursor = self.connection.cursor()

    def create_table(self):
        create_query = "CREATE TABLE coordinators(id integer, name text, topic text);"
        self.cursor.execute(create_query)
        self.connection.commit()

    def populate_table(self):
        insert_query = """
            INSERT INTO coordinators(id, name, topic) VALUES
                (134, 'Julia', 'Marketing'),
                (786, 'Amanda', 'Tech'),
                (295, 'Cerny', 'Manufacturing'),
                (667, 'Bob', 'Production'),  
                (915, 'Smith', 'Engineering');
        """
        self.cursor.execute(insert_query)
        self.connection.commit()

    def update_table(self):
        update_query = "UPDATE coordinators SET topic = 'Economy' WHERE name = 'Julia'"
        self.cursor.execute(update_query)
        self.connection.commit()

    def clear_table(self):
        clear_query = "DELETE FROM coordinators;"
        self.cursor.execute(clear_query)
        self.connection.commit()

    def delete_table(self):
        delete_query = "DROP TABLE IF EXISTS coordinators;"
        self.cursor.execute(delete_query)
        self.connection.commit()

    def close_postgresql_connection(self):
        self.cursor.close()
        self.connection.close()