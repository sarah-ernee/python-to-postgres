import random
import time
from datetime import datetime, timezone

from helper import PostgresqlOperations
helper = PostgresqlOperations()

TUNNEL_DRIVES = ['OP-EB', 'OP-WB']
CYCLE_TABLE = 'shift_cycle_time'
# GREASE_REPORT_TABLE = 'grease_report'

# remove GENERATED ALWAYS AS IDENTITY since we don't need to insert those
# no need to remove FKs since we are retrieving them with helper functions
CYCLE_COLUMNS = [
    'report_uid',
    'tunnel_drive',
    'downtime_id',
    'breakdown_id',
    'manufacture_defect',
    'remarks',
    'start_time',
    'end_time',
    'ring',
    'tbm_status',
    'report_status'
]
# GREASE_REPORT_COLUMNS = [
#     'report_uid',
#     'ring_number',
#     'grease_id'
# ]

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

TBM_STATUSES = [
    'Stoppage',
    'Ring Build',
    'Advance',
]

REPORT_STATUSES = [
    'draft',
    'submitted',
    'rejected',
    'approved'
]
 

def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    cycles = []
    # grease_reports = []

    # Foreign key retrieval
    report_uids = helper.retrieve_foreign_key_report_uid()
    # downtime_ids = helper.retrieve_cycle_foreign_keys_values()
    # breakdown_ids = helper.retrieve_cycle_foreign_keys_values()
    # tbm_status_ids = helper.retrieve_cycle_foreign_keys_values()
    # grease_ids = helper.retrieve_foreign_key_grease_id()
    n = 0

    # same number of reports as shift reports - 5596
    for x in range(1, 5597):
        for tbm_status in TBM_STATUSES:
            # ------------------------------------- CYCLE TIME ----------------------------------------- #
            manufacture_defect = random.choice(BOOLEAN)
            remarks = random.choice(REMARKS)
            start_time = datetime.fromtimestamp(time.time())
            end_time = datetime.fromtimestamp(time.time() + 2 * 60) # always two hours later
            ring = x
            tunnel_drive = random.choice(TUNNEL_DRIVES)
            report_status = random.choice(REPORT_STATUSES)

            report_uid = report_uids[n]
            downtime_id = random.randint(1, 6)
            breakdown_id = random.randint(1, 10)
            # tbm_status_id = random.randint(1, 5)
            # grease_id = random.randint(1, 2)

            values = [
                f"'{report_uid}'::uuid",
                f"'{tunnel_drive}'",
                f'{downtime_id}',
                f'{breakdown_id}',
                f'{manufacture_defect}',
                f"'{remarks}'",
                f"'{start_time}'",
                f"'{end_time}'",
                f'{ring}',
                f"'{tbm_status}'",
                f"'{report_status}'",
            ] 
            
            cycles.append(
                f'INSERT INTO {CYCLE_TABLE} ({", ".join(CYCLE_COLUMNS)}) VALUES ({", ".join(values)})'
            )
        
            # --------------------------------- GREASE REPORT TABLE ------------------------------------- #
            # report_values = [
            #     f"'{report_uid}'::uuid",
            #     f'{ring_number}',
            #     f'{grease_id}',
            # ]
            # grease_reports.append(
            #     f'INSERT INTO {GREASE_REPORT_TABLE} ({", ".join(GREASE_REPORT_COLUMNS)}) VALUES ({", ".join(report_values)})'
            # )

        n = n + 1
        print(f"Running generator loop for the {n} time")

                
        with open('./sql-sg/cycle_time.sql', 'w') as file:
            for cycle in cycles:
                file.write(cycle)
                file.write(';\n')

        # with open('./sql-sg/grease_report.sql', 'w') as file:
        #     for grease_report in grease_reports:
        #         file.write(grease_report)
        #         file.write(';\n')



'''
CREATE TABLE shift_cycle_time (
   id int generated always as identity,  
   report_uid uuid NOT NULL,
   tunnel_drive text NOT NULL,	  
   downtime_id int,	  
   breakdown_id int,	  
   manufacture_defect bool,	  
   remarks text,	  
   start_time timestamp without time zone NOT NULL,	  
   end_time timestamp without time zone NOT NULL,	  
   ring int NOT NULL,
   tbm_status text NOT NULL,	  
   report_status text NOT NULL,

   PRIMARY KEY (id),

   CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES shift_report(report_uid) ON DELETE CASCADE,
   CONSTRAINT downtime_id FOREIGN KEY (downtime_id) REFERENCES shift_downtime(downtime_id) ON DELETE CASCADE,
   CONSTRAINT breakdown_id FOREIGN KEY (breakdown_id) REFERENCES shift_breakdown(breakdown_id) ON DELETE CASCADE
);

C:/Users/Sarah/Desktop/python-to-postgres/sql-sg/cycle_time.sql
'''


# '''
# CREATE TABLE grease_report (
#    report_uid UUID,
#    ring_number INT NOT NULL,
#    grease_id INT,
#    id INT GENERATED ALWAYS AS IDENTITY, 
   
#    PRIMARY KEY (id),
#    CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports(report_uid) ON DELETE CASCADE,
#    CONSTRAINT grease_id FOREIGN KEY (grease_id) REFERENCES grease(grease_id) ON DELETE CASCADE
#  );
 
# C:/Users/sarahng/python-to-postgres/sql-sg/grease_report.sql
# '''