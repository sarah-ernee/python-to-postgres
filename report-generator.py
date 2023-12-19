import random
import time
from datetime import datetime
import json

# 5600 SHIFT REPORTS - VERSIONS TABLE NEED TO FOLLOW
TUNNEL_DRIVES = ['OP-EB', 'OP-WB']
SHIFT = ['DS', 'NS']
RINGS = 1400
MAX_VERSIONS = 100
    
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

                v = random.randint(1, MAX_VERSIONS)
                print(v)
                for version in range(v):
                    updated_at = f'"{datetime.utcfromtimestamp(time.time() + 24 * 60 * 60 * version)}"'

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
                        
                    values = f"{data}, {updated_at}"
                    versions.append(
                        f'INSERT INTO {VERSION_TABLE} ({", ".join(VERSION_COLUMNS)}) VALUES ({values})'
                    )

                    if version == v - 1:
                        report_value = [
                            'uuid_generate_v4()',
                            f'{date}',
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

    # with open('./sql/shift-report.sql', 'w') as file:
    #     for report in reports:
    #         file.write(report)
    #         file.write(';\n')


'''
INSERT INTO shift_report (report_uid, date, shift, end_ring, end_chainage, reported_by) 
VALUES (uuid_generate_v4(), 2023-12-19 12:10:15.584209, 'DS', 6, (19114,), 'zhynn@gamuda.com.my');
'''

'''
INSERT INTO shift_report_version (data, updated_at) 
VALUES (''
{
    "formRef": "OP-EB-R1-20231219", 
    "status": "submitted",
    "tbm": "S1347", 
    "tunnelDrive": "OP-EB", 
    "ring": 1, 
    "chainage": 364.0909915911994, 
    "shift": "DS", 
    "timestamp": "2023-12-19 12:10:15.594224", 
    "progress": {
        "cumulativeMinedDist": 27750, 
        "currentLocation": "Sorascea Site", 
        "endChainage": [19114],
        "endRingNumber": 6, 
        "sensitiveStructures": "Heavy Underground Piping Networks", 
        "startChainage": 19477, 
        "startRingNumber": 1
        }, 
    "statusDurationPercentage": {
        "durations": {"ringBuild": 4585.023413000946, "stopped": 2276.5844671896907}, 
        "percentages": {"ringBuild": 9.594925034615157, "stopped": 1.1697555399236625}
        }, 
    "groutInfo": {
        "groutInjectionVolume": [
            {
                "ringNumber": 1, 
                "target": 6182.489715249773, 
                "totalVolume": 4468, 
                "totalCompA": 1031, 
                "totalCompB": 3437
            }
        ]
    }
}'::jsonb,'
    '"2023-12-19 12:10:15.594224"');
'''