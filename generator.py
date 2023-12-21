import random
import time
from datetime import datetime

MAX_DOWNTIME_BREAKDOWN = 300

# maximums +1 since range inexclusive of end
MAX_DOWNTIME = 7
MAX_BREAKDOWN = 11
MAX_TBM_STATUS = 6
MAX_REP_STATUS = 5
MAX_GREASE = 3

DOWNTIME_TABLE = 'downtime'
BREAKDOWN_TABLE = 'breakdown'
TBM_STATUS_TABLE = 'shift_tbm_status'
REPORT_STATUS_TABLE = 'shift_report_status'
RELATIONSHIP_TABLE = 'downtime_breakdown_rl'
GREASE_TABLE = 'grease'

# remove FK and GENERATED ALWAYS AS IDENTITY since we don't need to insert those
DOWNTIME_COLUMNS = [
    'name',
]
BREAKDOWN_COLUMNS = [
    'name',
]
TBM_COLUMNS = [
    'name',
]
STATUS_COLUMNS = [
    'name',
]
RELATIONSHIP_COLUMNS = [
    'downtime_id',
    'breakdown_id',
]
GREASE_COLUMNS = [
    'name'
]

DOWNTIME_TYPES = [
    'Mechanical Downtime',
    'Electrical Downtime',
    'Operational Downtime',
    'Supplier Downtime',
    'HK Downtime',
    'H+E Downtime'
]
BREAKDOWN_CAUSES = [
    'Power Supply',
    'PLC/PCs',
    'Water Cooling Circuits',
    'Lubrication Grease, Gearbox Oil',
    'Sacrificial Grease (Tailskin, Shield Articulation, Main Drive, etc)',
    'Hydraulic Systems (Main, Auxiliary)',
    'Gripper functions (Main, Stabilizer)',
    'Roll Correction',
    'Thrust Cylinder (Main and Auxiliary)',
    'Cutting Wheel'
]
TBM_STATUSES = [
    'Stoppage',
    'Ring Build',
    'Advance RB',
    'Advance',
    'Regrip'
]
REPORT_STATUSES = [
    'draft',
    'submitted',
    'rejected',
    'approved'
]
GREASE_NAMES = [
    'Tail Skin',
    'EP2'
]



def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    non_generated = True
    
    # -------------------------------------- DOWNTIME BREAKDOWN RELATIONSHIP TABLE --------------------------- #
    relationships = []
    for id in range(1, MAX_DOWNTIME_BREAKDOWN):
        downtime_id = random.randint(1, 6)
        breakdown_id = random.randint(1, len(BREAKDOWN_CAUSES))

        values = f"{downtime_id}, {breakdown_id}"
        relationships.append(
            f'INSERT INTO {RELATIONSHIP_TABLE} ({", ".join(RELATIONSHIP_COLUMNS)}) VALUES ({values})'
        )

    with open('./sql/downtime_breakdown_rl.sql', 'w') as file:
        for relationship in relationships:
            file.write(relationship)
            file.write(';\n')

    # ------------------------------------ ALL THE PARENT TABLES (THOSE WITH PRIMARY KEY) ----------------------- #
    if non_generated:
        downtimes = []
        breakdowns = []
        tbm_states = []
        rep_statuses = []

        for id in range(1, MAX_DOWNTIME):
            name = DOWNTIME_TYPES[id - 1]
            values = f"'{name}'"
            downtimes.append(
                f'INSERT INTO {DOWNTIME_TABLE} ({", ".join(DOWNTIME_COLUMNS)}) VALUES ({values})'
            )

        for id in range(1, MAX_BREAKDOWN):
            name = BREAKDOWN_CAUSES[id - 1]
            values = f"'{name}'"
            breakdowns.append(
                f'INSERT INTO {BREAKDOWN_TABLE} ({", ".join(BREAKDOWN_COLUMNS)}) VALUES ({values})'
            )

        for id in range(1, MAX_TBM_STATUS):
            name = TBM_STATUSES[id - 1]
            values = f"'{name}'"
            tbm_states.append(f'INSERT INTO {TBM_STATUS_TABLE} ({", ".join(TBM_COLUMNS)}) VALUES ({values})'
            )

        for id in range(1, MAX_REP_STATUS):
            name = REPORT_STATUSES[id - 1]
            values = f"'{name}'"
            rep_statuses.append(f'INSERT INTO {REPORT_STATUS_TABLE} ({", ".join(STATUS_COLUMNS)}) VALUES ({values})'
            )

        with open('./sql/parent_tables.sql', 'w') as file:
            for downtime in downtimes:
                file.write(downtime)
                file.write(';\n')

            for breakdown in breakdowns:
                file.write(breakdown)
                file.write(';\n')

            for tbm_status in tbm_states:
                file.write(tbm_status)
                file.write(';\n')
            
            for report_status in rep_statuses:
                file.write(report_status)
                file.write(';\n')

    # ---------------------------------------------- GREASE & GREASE REPORT TABLE ------------------------------------------- #
    greases = []
    for id in range(1, MAX_GREASE):
        name = GREASE_NAMES[id - 1]

        values = f"'{name}'"
        greases.append(
            f'INSERT INTO {GREASE_TABLE} ({", ".join(GREASE_COLUMNS)}) VALUES ({values})'
        )

    with open('./sql/grease-report.sql', 'w') as file:
        for grease in greases:
            file.write(grease)
            file.write(';\n')




'''
CREATE TABLE IF NOT EXISTS downtime (
   downtime_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
   name TEXT NOT NULL,
   PRIMARY KEY (downtime_id)
);
CREATE TABLE IF NOT EXISTS breakdown (
   breakdown_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
   name TEXT NOT NULL,
   PRIMARY KEY (breakdown_id)
);
CREATE TABLE IF NOT EXISTS shift_tbm_status (
   tbm_status_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
   name TEXT NOT NULL,
   PRIMARY KEY (tbm_status_id)
);
CREATE TABLE IF NOT EXISTS shift_report_status (
   report_status_id INT GENERATED ALWAYS AS IDENTITY NOT NULL,
   name TEXT NOT NULL,
   PRIMARY KEY (report_status_id)
);
CREATE TABLE IF NOT EXISTS grease (
   grease_id INT GENERATED ALWAYS AS IDENTITY,
   name TEXT NOT NULL,
   PRIMARY KEY (grease_id)
);
'''



'''
CREATE TABLE downtime_breakdown_rl (
   downtime_id INT,
   breakdown_id INT,
   id INT GENERATED ALWAYS AS IDENTITY,
   PRIMARY KEY (id),

   CONSTRAINT downtime_id FOREIGN KEY (downtime_id) REFERENCES downtime(downtime_id) ON DELETE CASCADE,
   CONSTRAINT breakdown_id FOREIGN KEY (breakdown_id) REFERENCES breakdown(breakdown_id) ON DELETE CASCADE 
);
'''

