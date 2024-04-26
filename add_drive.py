import psycopg2
import random
import time
from datetime import datetime

from helper import PostgresqlOperations
helper = PostgresqlOperations()

TUNNEL_DRIVES = ['OP-EB', 'OP-WB']
REPORT_TABLE = 'shift_report'
SHIFT = ['DS', 'NS']

# remove GENERATED ALWAYS AS IDENTITY since we don't need to insert those
# no need to remove FKs since we are retrieving them with helper functions
REPORT_COLUMNS = [
    'report_uid',
    'date',
    'shift',
    'end_ring',
    'end_chainage',
    'reported_by',
]


def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    reports = []

    # Foreign key retrieval
    report_uids = helper.retrieve_foreign_key_report_uid()
    n = 0

    # same number of reports as shift reports - 5596
    for x in range(1, 5597):
        print(x)
        # ------------------------------------- CYCLE TIME ----------------------------------------- #
        # start_time = datetime.utcfromtimestamp(time.time())
        # end_time = datetime.utcfromtimestamp(
        #     time.time() + 2 * 60)  # always two hours later
        # ring_number = x
        # date = datetime.utcfromtimestamp(time.time())
        # end_ring = random.randint(100, 2_800)

        drive = random.choice(TUNNEL_DRIVES)
        report_uid = report_uids[n]

        # values = [
        #     f"'{report_uid}'::uuid",
        #     f"'{date}'",
        #     f"'{shift}'",
        #     f'{end_ring}',
        #     f'{end_chainage}',
        #     f"'{reported_by}'",
        # ]

        n = n + 1
        print(f"Running generator loop for the {n} time")

        reports.append(
            f"UPDATE {REPORT_TABLE} SET drive = '{drive}' WHERE report_uid = '{report_uid}'")

    with open('./sql/add_drive.sql', 'w') as file:
        for report in reports:
            file.write(report)
            file.write(';\n')


'''
ALTER TABLE shift_report DROP COLUMN IF EXISTS drive;
ALTER TABLE shift_report ADD COLUMN drive TEXT;

C:/Users/Sarah/Desktop/python-to-postgres/sql/add_drive.sql
'''
