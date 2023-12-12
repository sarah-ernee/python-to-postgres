CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

DROP TABLE IF EXISTS reports_versions, reports, downtime, breakdown, status, cycle_time;
CREATE TABLE reports_versions (
    report_uid uuid, 
    version_number smallint NOT NULL, 
    data json NOT NULL, 
    updated_at timestamp without time zone NOT NULL);

CREATE TABLE reports (
    report_uid uuid NOT NULL PRIMARY KEY, 
    version_number smallint NOT NULL, 
    date timestamp without time zone NOT NULL, 
    shift text NOT NULL, end_ring smallint NOT NULL, 
    end_chainage real NOT NULL, 
    reported_by text NOT NULL, 
    status text NOT NULL);

INSERT INTO reports (report_uid, version_number, date, shift, end_ring, end_chainage, reported_by, status) 
VALUES 
    (uuid_generate_v4(), 1, '2023-08-04 10:41:02', 'DS', 82, 19596.54, 'mohammad.firdaus@glcwtp.com.au', 'draft'), 
    (uuid_generate_v4(), 1, '2023-11-09 04:26:00', 'NS', 100, 19658.54, 'anurag.pattekar@glcwtp.com.au', 'rejected'),
    (uuid_generate_v4(), 1, '2023-02-23 13:18:43', 'DS', 75, 19600.34, 'alvin.francis@glcwtp.com.au', 'approved'), 
    (uuid_generate_v4(), 1, '2023-07-07 08:08:06', 'DS', 57, 19172.27, 'anurag.pattekar@glcwtp.com.au', 'submitted'), 
    (uuid_generate_v4(), 1, '2023-02-02 21:03:37', 'NS', 74, 19190.92, 'mohammad.firdaus@glcwtp.com.au', 'draft');

UPDATE reports 
SET 
    version_number = null;
    date = null;



INSERT INTO reports_versions (report_uid, version_number, data, updated_at) 
VALUES 
    ('d1f4bf3b-6d2d-475c-b519-f0fce27377ca',
    1, 
    '{
        "formRef": "OPEB-DS-20231108070000",
        "savedDowntime": [
            {
                "endTimestamp": "2023-11-08T04:54:25+00:00",
                "startTimestamp": "2023-11-07T19:30:00+00:00",
                "status": "STOPPED"
            }
        ]
    }'::JSONB, 
    '2023-07-25 07:34:02'), 
    ('f8045c84-2dcf-4259-8e9f-2b57b1bb8512',
    1, 
    '{
        "formRef": "OPEB-DS-20231012070000",
        "savedDowntime": [
            {
                "endTimestamp": "2023-10-12T04:54:25+00:00",
                "startTimestamp": "2023-10-11T19:30:00+00:00",
                "status": "ADVANCE"
            }
        ]
    }'::JSONB, 
    '2023-04-16 21:43:34'), 
    ('4c5b3c5e-e094-4d94-bb78-fcedd1a9d94d',
    1, 
    '{
        "formRef": "OPEB-NS-20231207190000",
        "savedDowntime": [
            {
                "endTimestamp": "2023-12-07T07:54:35+00:00",
                "startTimestamp": "2023-12-07T07:49:10+00:00",
                "status": "ADVANCE"
            }
        ]
    }'::JSONB, 
    '2022-12-02 17:59:05'), 
    ('277002ba-0b01-47fe-8ac4-b1cf37e47c7f',
    1, 
    '{
        "formRef": "OPEB-DS-20230929070000",
        "savedDowntime": [
            {
                "endTimestamp": "2023-09-29T08:59:56+00:00",
                "startTimestamp": "2023-09-28T21:00:01+00:00",
                "status": "RINGBUILD"
            }
        ]
    }'::JSONB, 
    '2022-12-23 23:38:52'), 
    ('a8476032-2f08-46bd-96a5-c6e55506ef25',
    1,    
    '{
        "formRef": "OPWB-NS-20231024190000",
        "savedDowntime": [
            {
                "endTimestamp": "2023-10-24T11:16:12+00:00",
                "startTimestamp": "2023-10-24T11:08:00+00:00",
                "status": "REGRIP"
            }
        ]
    }'::JSONB, 
    '2023-04-04 02:49:51');

ALTER TABLE reports_versions ADD CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports (report_uid);

CREATE TABLE downtime (downtime_id smallserial PRIMARY KEY NOT NULL, name text NOT NULL);

CREATE TABLE breakdown (breakdown_id smallserial PRIMARY KEY NOT NULL, name text NOT NULL);

CREATE TABLE status (status_id smallserial PRIMARY KEY NOT NULL, name text NOT NULL);

INSERT INTO downtime (downtime_id, name) 
VALUES 
    (1, 'Mechanical Downtime'), 
    (2, 'Electrical Downtime'), 
    (3, 'Operational Downtime'), 
    (4, 'Supplier Downtime'), 
    (5, 'HK Downtime');

INSERT INTO breakdown (breakdown_id, name) 
VALUES 
    (1, 'Power Supply'), 
    (2, 'PLC/PCs'), 
    (3, 'Water Cooling Circuits'), 
    (4, 'Lubrication Grease, Gearbox Oil'), 
    (5, 'Sacrificial Grease');

INSERT INTO status (status_id, name) 
VALUES 
    (1, 'Stoppage'), 
    (2, 'Ring Build'),
    (3, 'Advance RB'), 
    (4, 'Advance'), 
    (5, 'Regrip');

CREATE TABLE cycle_time (
    report_uid uuid NOT NULL, 
    downtime_id smallint, 
    breakdown_id smallint, 
    manufacture_defect boolean, 
    remarks text, 
    start_time timestamp without time zone NOT NULL, 
    end_time timestamp without time zone NOT NULL, 
    ring_number smallint NOT NULL, 
    status_id smallint);

INSERT INTO cycle_time (report_uid, downtime_id, breakdown_id, manufacture_defect, remarks, start_time, end_time, ring_number, status_id) 
VALUES 
    ('d1f4bf3b-6d2d-475c-b519-f0fce27377ca'::UUID, 1, 1, false, 'mauris vulputate elementum nullam varius', '2023-10-25 10:40:19', '2023-01-28 21:25:16', 33, 1),
    ('f8045c84-2dcf-4259-8e9f-2b57b1bb8512'::UUID, 2, 2, true, 'pulvinar sed nisl nunc rhoncus', '2023-01-05 22:21:41', '2023-09-07 05:32:02', 118, 2), 
    ('4c5b3c5e-e094-4d94-bb78-fcedd1a9d94d'::UUID, 3, 3, true, 'volutpat sapien arcu sed augue', '2023-02-17 08:20:13', '2022-12-28 18:03:08', 44, 3), 
    ('277002ba-0b01-47fe-8ac4-b1cf37e47c7f'::UUID, 4, 4, false, 'imperdiet nullam orci pede venenatis', '2023-04-23 23:18:33', '2023-05-10 01:29:57', 104, 4), 
    ('a8476032-2f08-46bd-96a5-c6e55506ef25'::UUID, 5, 5, false, 'fringilla rhoncus mauris enim leo', '2023-08-31 21:25:37', '2023-04-30 08:55:10', 125, 5);

ALTER TABLE cycle_time ADD CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports (report_uid);
ALTER TABLE cycle_time ADD CONSTRAINT downtime_id FOREIGN KEY (downtime_id) REFERENCES downtime (downtime_id);
ALTER TABLE cycle_time ADD CONSTRAINT breakdown_id FOREIGN KEY (breakdown_id) REFERENCES breakdown (breakdown_id);
ALTER TABLE cycle_time ADD CONSTRAINT status_id FOREIGN KEY (status_id) REFERENCES status (status_id);

ALTER TABLE reports_versions
ALTER COLUMN data TYPE jsonb USING data::jsonb;

CREATE TABLE downtime_breakdown_rl (
    downtime_id smallint NOT NULL,
    breakdown_id smallint NOT NULL
);

ALTER TABLE downtime_breakdown_rl ADD CONSTRAINT downtime_id FOREIGN KEY (downtime_id) REFERENCES downtime;
ALTER TABLE downtime_breakdown_rl ADD CONSTRAINT breakdown_id FOREIGN KEY (breakdown_id) REFERENCES breakdown;

INSERT INTO downtime_breakdown_rl (downtime_id, breakdown_id) 
VALUES 
    (1, 1),
    (1, 2),
    (2, 1),
    (2, 2),
    (2, 3);


