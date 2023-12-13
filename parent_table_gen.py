import random
import time
from datetime import datetime

TUNNEL_DRIVES = ['OP-EB', 'OP-WB']
RINGS = 2800
MAX_VERSIONS = 100

DOWNTIME_TABLE = 'downtime'
BREAKDOWN_TABLE = 'breakdown'
TBM_STATUS_TABLE = 'shift_tbm_status'
REPORT_STATUS_TABLE = 'shift_report_status'
 
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

EMAILS = [
    'hanfai@hoyoverse.com',
    'marcus@gmail.com',
    'sarah@tiktok.com',
    'kaiwen@reddit.com',
    'kenny@facebook.com',
    'zhynn@twitter.com',
    'sam@gamuda.com',
    'chu@planetfitness.com',
    'dana@runescape.com',
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




def nullable(*args):
    return random.choice(['null', *args])


if __name__ == '__main__':
    downtime = []
    breakdown = []  
    tbm_status = []
    report_status = [] # list of latest report versions

    for ring_number in range(1, RINGS):
        for tunnel_drive in TUNNEL_DRIVES:
            form_ref = f'{tunnel_drive}-R{ring_number}-{datetime.now().strftime("%Y%m%d")}'
            tbm = 'S1347' if tunnel_drive == 'OP-EB' else 'S1348'
            chainage = random.random() * 20_000
            shift = random.choice(['Day', 'Night'])
            created_by = random.choice(EMAILS)
            created_at = datetime.utcfromtimestamp(time.time())

            v = random.randint(1, MAX_VERSIONS)

            for version in range(v):
                status = random.choice(
                    ['draft', 'submitted', 'approved', 'rejected']
                )

                updated_by = nullable(f'"{random.choice(EMAILS)}"')
                if updated_by != 'null':
                    updated_at = f'"{datetime.utcfromtimestamp(time.time() + 24 * 60 * 60 * version)}"'
                else:
                    updated_at = 'null'

                submitted_by = nullable(f'"{random.choice(EMAILS)}"')
                if submitted_by != 'null':
                    submitted_at = f'"{datetime.utcfromtimestamp(time.time() + 24 * 60 * 60 * version)}"'
                else:
                    submitted_at = 'null'

                rejected_by = nullable(f'"{random.choice(EMAILS)}"')
                if rejected_by != 'null':
                    rejected_at = f'"{datetime.utcfromtimestamp(time.time() + 24 * 60 * 60 * version)}"'
                else:
                    rejected_at = 'null'

                approved_by = nullable(f'"{random.choice(EMAILS)}"')
                if approved_by != 'null':
                    approved_at = f'"{datetime.utcfromtimestamp(time.time() + 24 * 60 * 60 * version)}"'
                else:
                    approved_at = 'null'

                added = random.choice(
                    list(
                        filter(
                            lambda x: x['by'] != 'null',
                            [
                                {'by': created_by, 'at': created_at},
                                {'by': updated_by, 'at': updated_at},
                                {'by': submitted_by, 'at': submitted_at},
                                {'by': rejected_by, 'at': rejected_at},
                                {'by': approved_by, 'at': approved_at},
                            ]
                        )
                    )
                )

                data = f'''\'{{
    "formRef": "{form_ref}",
    "status": "{status}",
    "tbm": "{tbm}",
    "tunnelDrive": "{tunnel_drive}",
    "ring": {ring_number},
    "chainage": {chainage},
    "shift": "{shift}",
    "createdBy": "{created_by}",
    "timestamp": "{created_at}",
    "updatedBy": {updated_by},
    "updatedTimestamp": {updated_at},
    "submittedBy": {submitted_by},
    "submittedTimestamp": {submitted_at},
    "rejectedBy": {rejected_by},
    "rejectedTimestamp": {rejected_at},
    "approvedBy": {approved_by},
    "approvedTimestamp": {approved_at}
}}\'::jsonb'''

                values = f"'{tunnel_drive}', {ring_number}, '{added['at']}', '{added['by']}', {data}"
                versions.append(
                    f'INSERT INTO {VERSION_TABLE} ({", ".join(VERSION_COLUMNS)}) VALUES ({values})'
                )

                if version == v - 1:
                    report_value = [
                        f"'{tunnel_drive}'",
                        f'{ring_number}',
                        f"'{form_ref}'",
                        f"'{created_at}'",
                        f"'{created_by}'",
                        f'{chainage}',
                        f"'{status}'",
                        data,
                    ]
                    reports.append(
                        f'INSERT INTO {REPORT_TABLE} ({", ".join(REPORT_COLUMNS)}) VALUES ({", ".join(report_value)})'
                    )

    with open('./ring-report-version.sql', 'w') as file:
        for version in versions:
            file.write(version)
            file.write(';\n')

    with open('./ring-report.sql', 'w') as file:
        for report in reports:
            file.write(report)
            file.write(';\n')


# paginate ring report
# note: query with offset is noticeably slower
'''
EXPLAIN ANALYZE
SELECT
    *
FROM
    ring_report
WHERE
    tunnel_drive = 'OP-EB'
ORDER BY
   ring_number DESC
OFFSET
    1000
LIMIT
    10;
'''

# paginate ring report
# with filters
'''
EXPLAIN ANALYZE
SELECT
    *
FROM
    ring_report
WHERE
    tunnel_drive = 'OP-EB'
    AND status = 'rejected'
    AND ring_number BETWEEN 400 AND 1200
ORDER BY
   ring_number DESC
OFFSET
    1000
LIMIT
    10;
'''

# ring report version history timeline
'''
EXPLAIN ANALYZE
SELECT 
    *
FROM
    ring_report_version
WHERE
    tunnel_drive = 'OP-EB'
    AND ring_number = 500
ORDER BY
    added_timestamp DESC;
'''

# ring report table
'''
CREATE TABLE report (
    tunnel_drive VARCHAR(10),
    ring_number INT,
    form_ref VARCHAR(40) NOT NULL,
    created_timestamp TIMESTAMP NOT NULL,
    created_by VARCHAR(255) NOT NULL,
    chainage REAL,
    status VARCHAR(20) NOT NULL,
    data JSONB NOT NULL,
    PRIMARY KEY(tunnel_drive, ring_number)
);
'''

# ring report version table
'''
CREATE TABLE report_version (
    id INT GENERATED ALWAYS AS IDENTITY,
    tunnel_drive VARCHAR(10),
    ring_number INT,
    added_timestamp TIMESTAMP NOT NULL,
    added_by VARCHAR(255) NOT NULL,
    data JSONB NOT NULL,
    PRIMARY KEY(id),
    CONSTRAINT report_version_fkey 
        FOREIGN KEY(tunnel_drive, ring_number)
            REFERENCES report(tunnel_drive, ring_number)
            ON DELETE CASCADE
);
'''
