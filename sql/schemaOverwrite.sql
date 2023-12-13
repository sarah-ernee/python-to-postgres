CREATE INDEX idx_downtime_id on downtime_breakdown_rl (downtime_id);

DROP INDEX idx_shift, idx_end_ring, idx_end_chainage, idx_reported_by, idx_status ON reports;
DROP INDEX idx_downtime_cycle, idx_manufacture_dft, idx_start_time, idx_end_time, idx_status_id ON reports;

GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public to sarah, marcus, hanfai;
GRANT postgres to sarah, marcus, hanfai;

ALTER TABLE cycle_time ADD COLUMN id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL;
ALTER TABLE cycle_time ADD COLUMN tbm_status_id INTEGER GENERATED ALWAYS AS IDENTITY;

CREATE TABLE tbm_status (tbm_status_id INTEGER GENERATED ALWAYS AS IDENTITY NOT NULL PRIMARY KEY, name TEXT NOT NULL);



