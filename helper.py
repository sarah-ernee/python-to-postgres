import psycopg2
import uuid

class PostgresqlOperations:
    def __init__(self) -> None:
        '''
        Initiates connection to Cloud SQL instance with defined connection parameters.
        '''

        connection_params = {
            'user': 'sarah',
            'password': 'wtpsydneymetro2023',
            'host': '34.151.111.183',
            'port': '5432',
            'database': 'shift_progress_data'
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

    def retrieve_cycle_foreign_keys_values(self) -> list:
        '''
        Queries data values for foreign keys in cycle time and returns it as lists.

        Retrieves report_uid, downtime_id, breakdown_id and tbm_status_id from respective parent tables.
        '''
        # extend results?
        report_uids = []
        downtime_ids = []
        breakdown_ids = []
        tbm_status_ids = []

        fk_queries = [
            'SELECT report_uid FROM shift_report;', report_uids,
            'SELECT downtime_id FROM downtime;', downtime_ids,
            'SELECT report_uid FROM breakdown;', breakdown_ids,
            'SELECT report_uid FROM shift_tbm_status;', tbm_status_ids
        ]
        
        for query, results in fk_queries:
            self.sql_cursor.execute(query)
            result = [row[0] for row in self.sql_cursor.fetchall()]
            results.append(result)

        return report_uids, downtime_ids, breakdown_ids, tbm_status_ids

    @staticmethod
    def generate_report_uid() -> str:
        '''
        Generates report_uid string to be used for shift_report and shift_report_version query generator.
        '''
        report_uid = str(uuid.uuid4())
        return report_uid
    

