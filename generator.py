import random
import time
from datetime import datetime

MAX_DOWNTIME_BREAKDOWN = 300
MAX_DOWNTIME = 6
MAX_BREAKDOWN = 10
MAX_TBM_STATUS = 5
MAX_REP_STATUS = 4

DOWNTIME_TABLE = 'downtime'
BREAKDOWN_TABLE = 'breakdown'
TBM_STATUS_TABLE = 'shift_tbm_status'
REPORT_STATUS_TABLE = 'shift_report_status'
RELATIONSHIP_TABLE = 'downtime_breakdown_rl'
 
DOWNTIME_COLUMNS = [
    'downtime_id',
    'name',
]
BREAKDOWN_COLUMNS = [
    'breakdown_id',
    'name',
]
TBM_COLUMNS = [
    'tbm_status_id',
    'name',
]
STATUS_COLUMNS = [
    'report_status_id',
    'name',
]
RELATIONSHIP_COLUMNS = [
    'downtime_id',
    'breakdown_id',
    'id'
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


# downtime breakdown relationship- randomise both
# downtime, breakdown, tbm status, report status just static

def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    non_generated = True
    # downtime = []
    # breakdown = []  
    # tbm_status = []
    # report_status = [] # list of sql queries
    
    # -------------------------------------- DOWNTIME BREAKDOWN RELATIONSHIP TABLE --------------------------- #
    # relationships = []
    # for id in range(1, MAX_DOWNTIME_BREAKDOWN):
    #     downtime_id = random.randint(1, 6)
    #     breakdown_id = random.randint(1, len(BREAKDOWN_CAUSES))
    #     id = id

    #     values = f"{downtime_id}, {breakdown_id}, {id}"
    #     relationships.append(
    #         f'INSERT INTO {RELATIONSHIP_TABLE} ({", ".join(RELATIONSHIP_COLUMNS)}) VALUES ({values})'
    #     )

    # with open('./sql/downtime_breakdown_rl.sql', 'w') as file:
    #     for relationship in relationships:
    #         file.write(relationship)
    #         file.write(';\n')

    # ------------------------------------ ALL THE PARENT TABLES (THOSE WITH PRIMARY KEY) ----------------------- #
    if non_generated:
        downtimes = []
        breakdowns = []
        tbm_states = []
        rep_statuses = []

        for id in range(1, MAX_DOWNTIME):
            downtime_id = id
            name = DOWNTIME_TYPES[id - 1]
            values = f"{downtime_id}, '{name}'"
            downtimes.append(
                f'INSERT INTO {DOWNTIME_TABLE} ({", ".join(DOWNTIME_COLUMNS)}) VALUES ({values})'
            )

        # for id in range(1, MAX_BREAKDOWN):
        #     breakdown_id = id
        #     name = BREAKDOWN_CAUSES[id - 1]
        #     values = f"{breakdown_id}, '{name}'"
        #     breakdowns.append(
        #         f'INSERT INTO {BREAKDOWN_TABLE} ({", ".join(BREAKDOWN_COLUMNS)}) VALUES ({values})'
        #     )

        # for id in range(1, MAX_TBM_STATUS):
        #     tbm_status_id = id
        #     name = TBM_STATUSES[id - 1]
        #     values = f"{tbm_status_id}, '{name}'"
        #     tbm_states.append(f'INSERT INTO {TBM_STATUS_TABLE} ({", ".join(TBM_COLUMNS)}) VALUES ({values})'
        #     )

        # for id in range(1, MAX_REP_STATUS):
        #     report_status_id = id
        #     name = REPORT_STATUSES[id - 1]
        #     values = f"{report_status_id}, '{name}'"
        #     rep_statuses.append(f'INSERT INTO {REPORT_STATUS_TABLE} ({", ".join(STATUS_COLUMNS)}) VALUES ({values})'
        #     )

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



    

