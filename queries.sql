\c shift-progress-data

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE reports_versions_table (version_number smallint NOT NULL, data json NOT NULL, updated_at timestamp with time zone NOT NULL);

CREATE TABLE reports_table (report-uid uuid NOT NULL PRIMARY KEY, version_number smallint NOT NULL, date timestamp with time zone NOT NULL, shift text NOT NULL, end_ring smallint NOT NULL, end_chainage real NOT NULL, reported_by text NOT NULL, status text NOT NULL);

INSERT INTO reports_table (date, shift, end_ring, end_chainage, reported_by, status) VALUES ('2023-08-04 06:41:02', 'sed', 82, 563.55, 'Pink', 'arcu'), ('2023-11-09 07:26:00', 'curae', 100, 585.68, 'Puce', 'proin'), ('2023-02-23 05:18:43', 'pharetra', 75, 322.17, 'Turquoise', 'vestibulum'), ('2023-07-07 06:08:06', 'pede', 57, 548.9, 'Fuscia', 'integer'), ('2023-02-02 09:03:37', 'vulputate', 74, 969.91, 'Blue', 'orci');

INSERT INTO reports_versions_table (version_number, data, updated_at) VALUES (64, '[{},{}]', '2023-07-25 07:34:02'), (72, '[{},{}]', '2023-04-16 21:43:34'), (95, '[{},{}]', '2022-12-02 17:59:05'), (36, '[{},{}]', '2022-12-23 23:38:52'), (17, '[{},{}]', '2023-04-04 02:49:51');

ALTER TABLE reports_versions_table ADD COLUMN report_uid uuid;

ALTER TABLE reports_versions_table ADD CONSTRAINT report_uid FOREIGN KEY (report_uid) REFERENCES reports_table (report_uid);

UPDATE reports_versions_table as B SET report_uid = A.report_uid FROM reports_table as A;

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

UPDATE cycle_time_table as B SET report_uid = A.report_uid FROM reports_versions_table as A;

UPDATE cycle_time_table as B SET downtime_id = A.downtime_id FROM downtime_table as A;

UPDATE cycle_time_table as B SET breakdown_id = A.breakdown_id FROM breakdown_table as A;

UPDATE cycle_time_table as B SET status_id = A.status_id FROM status_table as A;

