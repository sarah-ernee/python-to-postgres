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

INSERT INTO downtime (name) VALUES ('Mechanical Downtime');
INSERT INTO downtime (name) VALUES ('Electrical Downtime');
INSERT INTO downtime (name) VALUES ('Operational Downtime');
INSERT INTO downtime (name) VALUES ('Supplier Downtime');
INSERT INTO downtime (name) VALUES ('HK Downtime');
INSERT INTO downtime (name) VALUES ('H+E Downtime');
INSERT INTO breakdown (name) VALUES ('Power Supply');
INSERT INTO breakdown (name) VALUES ('PLC/PCs');
INSERT INTO breakdown (name) VALUES ('Water Cooling Circuits');
INSERT INTO breakdown (name) VALUES ('Lubrication Grease, Gearbox Oil');
INSERT INTO breakdown (name) VALUES ('Sacrificial Grease (Tailskin, Shield Articulation, Main Drive, etc)');
INSERT INTO breakdown (name) VALUES ('Hydraulic Systems (Main, Auxiliary)');
INSERT INTO breakdown (name) VALUES ('Gripper functions (Main, Stabilizer)');
INSERT INTO breakdown (name) VALUES ('Roll Correction');
INSERT INTO breakdown (name) VALUES ('Thrust Cylinder (Main and Auxiliary)');
INSERT INTO breakdown (name) VALUES ('Cutting Wheel');
INSERT INTO shift_tbm_status (name) VALUES ('Stoppage');
INSERT INTO shift_tbm_status (name) VALUES ('Ring Build');
INSERT INTO shift_tbm_status (name) VALUES ('Advance RB');
INSERT INTO shift_tbm_status (name) VALUES ('Advance');
INSERT INTO shift_tbm_status (name) VALUES ('Regrip');
INSERT INTO shift_report_status (name) VALUES ('draft');
INSERT INTO shift_report_status (name) VALUES ('submitted');
INSERT INTO shift_report_status (name) VALUES ('rejected');
INSERT INTO shift_report_status (name) VALUES ('approved');
