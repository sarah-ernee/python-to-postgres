\c shift-progress-data

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE reports_versions_table (report_uid uuid, version_number smallint, data json NOT NULL, updated_at timestamp with time zone NOT NULL);

CREATE TABLE reports_table (report_uid uuid PRIMARY KEY, version_number smallint, date timestamp with time zone NOT NULL, shift text NOT NULL, end_ring smallint NOT NULL, end_chainage real NOT NULL, reported_by text NOT NULL, status text NOT NULL);

INSERT INTO reports_table (report_uid, date, shift, end_ring, end_chainage, reported_by, status) VALUES ('f7cbc195-5979-49fb-8b7f-dcbce65e0ab5', '2023-08-04 06:41:02', 'sed', 82, 563.55, 'Pink', 'arcu'), ('8787d83e-56a9-4eb2-a6ec-1562b03e58b0', '2023-11-09 07:26:00', 'curae', 100, 585.68, 'Puce', 'proin'), ('16f694df-8084-45dc-b262-fbd702810d94', '2023-02-23 05:18:43', 'pharetra', 75, 322.17, 'Turquoise', 'vestibulum'), ('9e650b66-7fc4-428f-9aec-1c7d465f2b30', '2023-07-07 06:08:06', 'pede', 57, 548.9, 'Fuscia', 'integer'), ('77535057-093e-4686-9f12-1677c4174698', '2023-02-02 09:03:37', 'vulputate', 74, 969.91, 'Blue', 'orci');

INSERT INTO reports_versions_table (version_number, data, updated_at) VALUES (64, '[{},{}]', '2023-07-25 07:34:02'), (72, '[{},{}]', '2023-04-16 21:43:34'), (95, '[{},{}]', '2022-12-02 17:59:05'), (36, '[{},{}]', '2022-12-23 23:38:52'), (17, '[{},{}]', '2023-04-04 02:49:51');

ALTER TABLE reports_versions_table ADD CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports_table (report_uid);

UPDATE reports_versions_table as B SET report_uid = A.report_uid FROM reports_table as A WHERE B.report_uid = A.report_uid;

ALTER TABLE reports_table ADD CONSTRAINT version_number FOREIGN KEY (version_number) REFERENCES reports_versions_table (version_number);

UPDATE reports_table as B SET version_number = A.version_number FROM reports_versions_table as A;



INSERT INTO downtime_table (downtime_id, name) VALUES (1, 'Mechanical Downtime'), (2, 'Electrical Downtime'), (3, 'Operational Downtime'), (4, 'Supplier Downtime'), (5, 'HK Downtime');

INSERT INTO breakdown_table (breakdown_id, name) VALUES (1, 'Power Supply'), (2, 'PLC/PCs'), (3, 'Water Cooling Circuits'), (4, 'Lubrication Grease, Gearbox Oil'), (5, 'Sacrificial Grease');

INSERT INTO status_table (status_id, name) VALUES (1, 'Stoppage'), (2, 'Ring Build'), (3, 'Advance RB'), (4, 'Advance'), (5, 'Regrip');


SELECT a.attname, format_type(a.atttypid, a.atttypmod) AS data_type
FROM   pg_index i
JOIN   pg_attribute a ON a.attrelid = i.indrelid
                     AND a.attnum = ANY(i.indkey)
WHERE  i.indrelid = 'status_table'::regclass 
AND    i.indisprimary;

CREATE TABLE cycle_time_table (report_uid uuid, event varchar(10) NOT NULL, downtime_id smallint, breakdown_id smallint, manufacture_defect boolean, remarks text, start_time timestamp with time zone NOT NULL, end_time timestamp with time zone NOT NULL, ring_number smallint NOT NULL, status_id smallint);

ALTER TABLE cycle_time_table ADD CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports_table (report_uid);
ALTER TABLE cycle_time_table ADD CONSTRAINT downtime_id FOREIGN KEY (downtime_id) REFERENCES downtime_table (downtime_id);
ALTER TABLE cycle_time_table ADD CONSTRAINT breakdown_id FOREIGN KEY (breakdown_id) REFERENCES breakdown_table (breakdown_id);
ALTER TABLE cycle_time_table ADD CONSTRAINT status_id FOREIGN KEY (status_id) REFERENCES status_table (status_id);

CREATE TABLE cycle_time_table (event varchar(50), manufacture_defect varchar(50), remarks text, start_time timestamp with time zone, end_time timestamp with time zone, ring_number smallint);

INSERT INTO cycle_time_table (event, manufacture_defect, remarks, start_time, end_time, ring_number)
VALUES
    ('DefaultEvt', false, 'mauris vulputate elementum nullam varius', '2023-10-25 10:40:19', '2023-01-28 21:25:16', 33),
    ('DefaultEvt', true, 'pulvinar sed nisl nunc rhoncus', '2023-01-05 22:21:41', '2023-09-07 05:32:02', 118),
    ('DefaultEvt', true, 'volutpat sapien arcu sed augue', '2023-02-17 08:20:13', '2022-12-28 18:03:08', 44),
    ('DefaultEvt', false, 'imperdiet nullam orci pede venenatis', '2023-04-23 23:18:33', '2023-05-10 01:29:57', 104),
    ('DefaultEvt', false, 'fringilla rhoncus mauris enim leo', '2023-08-31 21:25:37', '2023-04-30 08:55:10', 125);

UPDATE cycle_time_table as B SET report_uid = A.report_uid FROM reports_table as A;

UPDATE cycle_time_table as B SET downtime_id = A.downtime_id FROM downtime_table as A;

UPDATE cycle_time_table as B SET breakdown_id = A.breakdown_id FROM breakdown_table as A;

UPDATE cycle_time_table as B SET status_id = A.status_id FROM status_table as A;



CREATE TABLE johnny (report_uid uuid, version_number smallint, data json NOT NULL, updated_at timestamp with time zone NOT NULL);

CREATE TABLE celia (report_uid uuid PRIMARY KEY, version_number smallint, date timestamp with time zone NOT NULL, shift text NOT NULL, end_ring smallint NOT NULL, end_chainage real NOT NULL, reported_by text NOT NULL, status text NOT NULL);

INSERT INTO celia (report_uid, date, shift, end_ring, end_chainage, reported_by, status) VALUES ('f7cbc195-5979-49fb-8b7f-dcbce65e0ab5', '2023-08-04 06:41:02', 'sed', 82, 563.55, 'Pink', 'arcu'), ('8787d83e-56a9-4eb2-a6ec-1562b03e58b0', '2023-11-09 07:26:00', 'curae', 100, 585.68, 'Puce', 'proin'), ('16f694df-8084-45dc-b262-fbd702810d94', '2023-02-23 05:18:43', 'pharetra', 75, 322.17, 'Turquoise', 'vestibulum'), ('9e650b66-7fc4-428f-9aec-1c7d465f2b30', '2023-07-07 06:08:06', 'pede', 57, 548.9, 'Fuscia', 'integer'), ('77535057-093e-4686-9f12-1677c4174698', '2023-02-02 09:03:37', 'vulputate', 74, 969.91, 'Blue', 'orci');

INSERT INTO johnny (version_number, data, updated_at) VALUES (64, '[{},{}]', '2023-07-25 07:34:02'), (72, '[{},{}]', '2023-04-16 21:43:34'), (95, '[{},{}]', '2022-12-02 17:59:05'), (36, '[{},{}]', '2022-12-23 23:38:52'), (17, '[{},{}]', '2023-04-04 02:49:51');

ALTER TABLE johnny ADD CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES celia (report_uid);

ALTER TABLE celia ADD CONSTRAINT version_number FOREIGN KEY (version_number) REFERENCES johnny (version_number);

-- circular dependency since one value has to exist before the other but version number is filled in REPORTS_TABLE based on report id match
-- report id is filled in REPORTS_VERSIONS_TABLE based on version number match
-- matches cannot exist until both columns of version_number and report_id is filled. chicken or the egg situation
UPDATE celia as B SET version_number = A.version_number FROM johnny as A WHERE B.report_uid = A.report_uid; 

UPDATE johnny AS B SET report_uid = A.report_uid FROM celia AS A WHERE B.version_number = A.version_number;
