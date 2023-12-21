import random
import time
from datetime import datetime
import json

from helper import PostgresqlOperations
helper = PostgresqlOperations()

TUNNEL_DRIVES = ['OP-EB', 'OP-WB']
SHIFT = ['DS', 'NS']
RINGS = 1400

REPORT_TABLE = 'shift_report'
VERSION_TABLE = 'shift_report_version'

# remove FKs and GENERATED ALWAYS AS IDENTITY since we don't need to insert those
REPORT_COLUMNS = [
    'report_uid',
    'date',
    'shift',
    'end_ring',
    'end_chainage',
    'reported_by',
]
VERSION_COLUMNS = [
    'report_uid',
    'data',
    'updated_at',
]

EMAILS = [
    'hanfai@gamuda.com.my',
    'marcus@gamuda.com.my',
    'sarah@gamuda.com.my',
    'kaiwen@gamuda.com.my',
    'kenny@gamuda.com.my',
    'zhynn@gamuda.com.my',
    'sam@gamuda.com.my',
    'chu@gamuda.com.my',
    'dana@gamuda.com.my',
]

LOCATIONS = [
    'Rosehill Site',
    'Palm Grove Site',
    'Sorascea Site',
    'Thalmes Site'
]

STRUCTURES = [
    'Sinkholes Detected',
    'Muddy Foundation',
    'Ground Fissures',
    'Heavy Underground Piping Networks'
]
 

def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    versions = []
    reports = []

    # 2800 rings per drive for both shifts - 5600 reports
    for ring_number in range(1, RINGS, 1):
        for tunnel_drive in TUNNEL_DRIVES:
            for shift in SHIFT:  
                report_uid = helper.generate_report_uid()
                date = datetime.utcfromtimestamp(time.time()) 
                end_ring = random.randint(100, 2_800)
                end_chainage = random.uniform(19_100.000000000, 19_300.000000000)
                reported_by = random.choice(EMAILS)   

                # -------------------------------------- JSONB DATA ------------------------------------- #
                form_ref = f'{tunnel_drive}-R{ring_number}-{datetime.now().strftime("%Y%m%d")}'
                status = random.choice(
                        ['draft', 'submitted', 'approved', 'rejected']
                    )
                tbm = 'S1347' if tunnel_drive == 'OP-EB' else 'S1348'
                chainage = random.uniform(18_000.000000000, 20_000.000000000)           
                timestamp = datetime.utcfromtimestamp(time.time())
                
                # Nested progress dict
                cumulative_mined_dist = random.uniform(-20_000.000000000, 30_000.000000000) 
                current_location = random.choice(LOCATIONS)
                end_ring = ring_number + 5
                sensitive_structures = random.choice(STRUCTURES)            
                start_chainage = random.uniform(19_400.000000000, 19_600.000000000)
                
                # Nested status duration dict
                ring_duration = random.random() * 15_000
                stopped_duration = random.random() * 25_000
                ring_duration_pc = random.random() * 15
                stopped_duration_pc = random.random() * 40

                # Nested grout injection array
                target_injection = random.random() * 9_000
                total_comp_a = random.randrange(1_000, 4_500)
                total_comp_b = random.randrange(1_000, 4_500)
                total_volume = total_comp_a + total_comp_b

                # ------------------------------------ VERSION TABLE ------------------------------------ #
                updated_at = f"'{datetime.utcfromtimestamp(time.time() + 24 * 60 * 60 * 1)}'"
                dict = {
                    "formRef": form_ref,
                    "status": status,
                    "tbm": tbm,
                    "tunnelDrive": tunnel_drive,
                    "ring": ring_number,
                    "chainage": chainage,
                    "shift": shift,
                    "timestamp": timestamp,
                    "progress": {
                        "cumulativeMinedDist": cumulative_mined_dist,
                        "currentLocation": current_location,
                        "endChainage": end_chainage,
                        "endRingNumber": end_ring,
                        "sensitiveStructures": sensitive_structures,
                        "startChainage": start_chainage,
                        "startRingNumber": ring_number,
                    },
                    "statusDurationPercentage": {
                        "durations": {
                            "ringBuild": ring_duration,
                            "stopped": stopped_duration
                        },
                        "percentages": {
                            "ringBuild": ring_duration_pc,
                            "stopped": stopped_duration_pc
                        }
                    },
                    "groutInfo": {
                        "groutInjectionVolume": [
                            {
                                "ringNumber": ring_number,
                                "target": target_injection, 
                                "totalVolume": total_volume, 
                                "totalCompA": total_comp_a,
                                "totalCompB": total_comp_b, 
                            }
                        ]
                    }
                }

                json_string = json.dumps(dict, default=str)
                data = f"'{json_string}'::jsonb"
                    
                values = f"'{report_uid}'::uuid, {data}, {updated_at}"
                versions.append(
                    f'INSERT INTO {VERSION_TABLE} ({", ".join(VERSION_COLUMNS)}) VALUES ({values})'
                )
                
                # --------------------------------------- REPORT TABLE ------------------------------------- #
                # if version == v - 1:
                report_value = [
                    f"'{report_uid}'::uuid",
                    f"'{date}'",
                    f"'{shift}'",
                    f'{end_ring}',
                    f'{end_chainage}',
                    f"'{reported_by}'",
                ]
                reports.append(
                    f'INSERT INTO {REPORT_TABLE} ({", ".join(REPORT_COLUMNS)}) VALUES ({', '.join(report_value)})'
                )

    with open('./sql/shift-report-version.sql', 'w') as file:
        for version in versions:
            file.write(version)
            file.write(';\n')

    with open('./sql/shift-report.sql', 'w') as file:
        for report in reports:
            file.write(report)
            file.write(';\n')
            


'''
CREATE TABLE IF NOT EXISTS shift_report (
   report_uid UUID NOT NULL,
   version_number INT GENERATED ALWAYS AS IDENTITY NOT NULL,
   date TIMESTAMP WITHOUT TIME ZONE NOT NULL,
   shift TEXT NOT NULL,
   end_ring INT NOT NULL,
   end_chainage REAL NOT NULL,
   reported_by TEXT NOT NULL,
   report_status_id INT,

   PRIMARY KEY (report_uid),
   CONSTRAINT report_status_id
      FOREIGN KEY (report_status_id)
         REFERENCES shift_report_status(report_status_id)
         ON DELETE CASCADE
);

C:/Users/Sarah/Desktop/python-to-postgres/sql/shift-report.sql
'''


'''
CREATE TABLE IF NOT EXISTS shift_report_version (
   report_uid UUID,
   version_number INT GENERATED ALWAYS AS IDENTITY NOT NULL, 
   data JSONB,
   updated_at TIMESTAMP WITHOUT TIME ZONE,
   id INT GENERATED ALWAYS AS IDENTITY,
   PRIMARY KEY (id),

   CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES shift_report(report_uid) ON DELETE CASCADE
);

C:/Users/Sarah/Desktop/python-to-postgres/sql/shift-report-version.sql
'''