import psycopg2

class PostgresqlOperations:
    def __init__(self) -> None:
        '''
        Initiates connection to Cloud SQL instance with defined connection parameters.
        '''
        connection_params = {
            'user': 'postgres',
            'password': 'wtpsydneymetro2023',
            'host': '34.151.111.183',
            'port': '5432',
            'database': 'shift-progress-data'
        }
        self.sql_conn = psycopg2.connect(**connection_params)
        self.sql_cursor = self.sql_conn.cursor()


    def create_dummy_tables_in_cloud_sql(self) -> None:
        '''
        Create dummy data tables with connected instance and only needs to be run once.

        Reads from SQL file containing necessary Postgres queries.
        '''
        with open('createMock.sql', 'r') as file:
            queries = file.read()

            commands = queries.split(';') 

            for command in commands[:-1]:
                try:
                    self.sql_cursor.execute(f'{command}')
                    self.sql_conn.commit()

                except psycopg2.Error as e:
                    print(f"Error: {e} for {command}")
                    self.sql_conn.rollback() 

            self.sql_cursor.close()
            self.sql_conn.close()
