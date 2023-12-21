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
    downtime_ids = helper.retrieve_cycle_foreign_keys_values()
    breakdown_ids = helper.retrieve_cycle_foreign_keys_values()
    tbm_status_ids = helper.retrieve_cycle_foreign_keys_values()
    grease_ids = helper.retrieve_foreign_key_grease_id()
    n = 0

    print(f"Current value of n: {n}, Length of report_uids: {len(report_uids)}")
    print(f"Current value of n: {n}, Length of report_uids: {len(grease_ids)}")


    # same number of reports as shift reports - 5596
    for x in range(1, 5597):
        # ------------------------------------- CYCLE TIME ----------------------------------------- #
        manufacture_defect = random.choice(BOOLEAN)
        remarks = random.choice(REMARKS)
        start_time = datetime.utcfromtimestamp(time.time())
        end_time = datetime.utcfromtimestamp(time.time() + 2 * 60) # always two hours later
        ring_number = x

        report_uid = report_uids[n]
        downtime_id = random.choice(downtime_ids)
        breakdown_id = random.choice(breakdown_ids)
        tbm_status_id = random.choice(tbm_status_ids)
        grease_id = random.choice(grease_ids)

        values = [
            f"'{report_uid}'::uuid",
            f'{downtime_id}',
            f'{breakdown_id}',
            f"'{manufacture_defect}'",
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

    with open('./sql/grease_report.sql', 'w') as file:
        for grease_report in grease_reports:
            file.write(grease_report)
            file.write(';\n')
