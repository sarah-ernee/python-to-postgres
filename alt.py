import random
import time
from datetime import datetime, timedelta

from helper import PostgresqlOperations
helper = PostgresqlOperations()

# Initialize variables for date and ring increment
current_date = datetime(2024, 1, 1)
date_increment = timedelta(days=1)
ring_counter = 0

# List to store generated SQL queries
cycles = []
report_uids = helper.retrieve_foreign_key_report_uid()
n = 0

# Loop for generating SQL commands
for x in range(1, 3001):
    for drive in ['OP-EB', 'OP-WB']:
        for tbm_status in ['Stoppage', 'Ring Build', 'Advance']:
            # Generate random manufacture_defect and remarks
            report_uid = report_uids[n]
            manufacture_defect = random.choice([True, False])
            report_status = random.choice([
                'draft',
                'submitted',
                'rejected',
                'approved'])
            remarks = random.choice([
                'Belt misalignment fault. Conveyor crew called to fix.',
                'Opened hatch to remove obtrusion from under.',
                '10 min prestart, 15 min walk, 8 min changing grease barrel prior to regrip.',
                'Thrust pumps dropped out.',
                'Revert to manual. Fitter/sparky monitoring.',
                'Ventilation bag repairs after the cable broke.',
                'Crew evacuated to the back of the machine.',
                'Waiting for parts arrival on site.',
            ])
            
            # Generate random start_time and end_time within 5 to 20 minutes range
            start_time = current_date + timedelta(minutes=random.randint(0, 1435))  # 1435 minutes = 23 hours 55 minutes
            end_time = start_time + timedelta(minutes=random.randint(5, 20))

            # Increment ring counter
            ring_counter += 1

            # Generate SQL command to insert row
            sql = f"INSERT INTO shift_cycle_time (report_uid, drive, manufacture_defect, remarks, start_time, end_time, ring, tbm_status, report_status) VALUES ('{report_uid}'::uuid, '{drive}', {manufacture_defect}, '{remarks}', '{start_time}', '{end_time}', {x}, '{tbm_status}', '{report_status}')"
            
            # Append the SQL command to the list
            cycles.append(sql)

            # Increment date every 10 rings
            if ring_counter % 10 == 0:
                current_date += date_increment
                if current_date.day == 28:
                    current_date = current_date.replace(day=1, month=current_date.month + 1)
                    if current_date.month == 12:
                        current_date = current_date.replace(day=1, month=1, year=current_date.year + 1)


# Write the generated SQL commands to a file
with open('./fml.sql', 'w') as file:
    for cycle in cycles:
        file.write(cycle)
        file.write(';\n')

print("SQL queries generated successfully!")
