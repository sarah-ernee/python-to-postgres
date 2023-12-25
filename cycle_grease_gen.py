import psycopg2
import random
import time
from datetime import datetime

from helper import PostgresqlOperations
helper = PostgresqlOperations()

CYCLE_TABLE = 'cycle_time'
GREASE_REPORT_TABLE = 'grease_report'

# remove GENERATED ALWAYS AS IDENTITY since we don't need to insert those
# no need to remove FKs since we are retrieving them with helper functions
CYCLE_COLUMNS = [
    'report_uid',
    'downtime_id',
    'breakdown_id',
    'manufacture_defect',
    'remarks',
    'start_time',
    'end_time',
    'ring_number',
    'tbm_status_id'
]
GREASE_REPORT_COLUMNS = [
    'report_uid',
    'ring_number',
    'grease_id'
]

REMARKS = [
    'Belt misalignment fault. Conveyor crew called to fix.',
    'Opened hatch to remove obtrusion from under.',
    '10 min prestart, 15 min walk, 8 min changing grease barrel prior to regrip.',
    'Thrust pumps dropped out.',
    'Revert to manual. Fitter/sparky monitoring.',
    'Ventilation bag repairs after the cable broke.',
    'Crew evacuated to the back of the machine.',
    'Waiting for parts arrival on site.',
]
BOOLEAN = [True, False]
 

def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    cycles = []
    grease_reports = []

    # Foreign key retrieval
    report_uids = helper.retrieve_foreign_key_report_uid()
    # downtime_ids = helper.retrieve_cycle_foreign_keys_values()
    # breakdown_ids = helper.retrieve_cycle_foreign_keys_values()
    # tbm_status_ids = helper.retrieve_cycle_foreign_keys_values()
    # grease_ids = helper.retrieve_foreign_key_grease_id()
    n = 0

    # same number of reports as shift reports - 5596
    for x in range(1, 5597):
        # ------------------------------------- CYCLE TIME ----------------------------------------- #
        manufacture_defect = random.choice(BOOLEAN)
        remarks = random.choice(REMARKS)
        start_time = datetime.utcfromtimestamp(time.time())
        end_time = datetime.utcfromtimestamp(time.time() + 2 * 60) # always two hours later
        ring_number = x

        report_uid = report_uids[n]
        downtime_id = random.randint(1, 6)
        breakdown_id = random.randint(1, 10)
        tbm_status_id = random.randint(1, 5)
        grease_id = random.randint(1, 2)

        values = [
            f"'{report_uid}'::uuid",
            f'{downtime_id}',
            f'{breakdown_id}',
            f'{manufacture_defect}',
            f"'{remarks}'",
            f"'{start_time}'",
            f"'{end_time}'",
            f'{ring_number}',
            f'{tbm_status_id}',
        ] 
        
        n = n + 1
        print(f"Running generator loop for the {n} time")

        cycles.append(
            f'INSERT INTO {CYCLE_TABLE} ({", ".join(CYCLE_COLUMNS)}) VALUES ({", ".join(values)})'
        )
    
        # --------------------------------- GREASE REPORT TABLE ------------------------------------- #
        report_values = [
            f"'{report_uid}'::uuid",
            f'{ring_number}',
            f'{grease_id}',
        ]
        grease_reports.append(
            f'INSERT INTO {GREASE_REPORT_TABLE} ({", ".join(GREASE_REPORT_COLUMNS)}) VALUES ({", ".join(report_values)})'
        )

            
    with open('./sql/cycle_time.sql', 'w') as file:
        for cycle in cycles:
            file.write(cycle)
            file.write(';\n')

    # with open('./sql/grease_report.sql', 'w') as file:
    #     for grease_report in grease_reports:
    #         file.write(grease_report)
    #         file.write(';\n')



'''
CREATE TABLE cycle_time (
   report_uid UUID,
   downtime_id INT,
   breakdown_id INT,
   manufacture_defect BOOLEAN,
   remarks TEXT NOT NULL,
   start_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
   end_time TIMESTAMP WITHOUT TIME ZONE NOT NULL,
   ring_number INT NOT NULL,
   tbm_status_id INT,
   id INT GENERATED ALWAYS AS IDENTITY,
   PRIMARY KEY (id),

   CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES shift_report(report_uid) ON DELETE CASCADE,
   CONSTRAINT downtime_id FOREIGN KEY (downtime_id) REFERENCES downtime(downtime_id) ON DELETE CASCADE,
   CONSTRAINT breakdown_id FOREIGN KEY (breakdown_id) REFERENCES breakdown(breakdown_id) ON DELETE CASCADE,
   CONSTRAINT tbm_status_id FOREIGN KEY (tbm_status_id) REFERENCES shift_tbm_status(tbm_status_id) ON DELETE CASCADE
);

C:/Users/sarahng/python-to-postgres/sql/cycle_time.sql
'''


'''
CREATE TABLE grease_report (
   report_uid UUID,
   ring_number INT NOT NULL,
   grease_id INT,
   id INT GENERATED ALWAYS AS IDENTITY, 
   
   PRIMARY KEY (id),
   CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports(report_uid) ON DELETE CASCADE,
   CONSTRAINT grease_id FOREIGN KEY (grease_id) REFERENCES grease(grease_id) ON DELETE CASCADE
 );
 
C:/Users/sarahng/python-to-postgres/sql/grease_report.sql
'''