CREATE INDEX idx_breakdown_id ON downtime_breakdown_rl (breakdown_id);
CREATE INDEX idx_version_number on reports_versions (version_number);

CREATE INDEX idx_date on reports (date);
CREATE INDEX idx_shift on reports (shift);
CREATE INDEX idx_end_ring on reports (end_ring);
CREATE INDEX idx_end_chainage on reports (end_chainage);
CREATE INDEX idx_reported_by on reports (reported_by);
CREATE INDEX idx_status on reports (status);

CREATE INDEX idx_downtime_cycle on cycle_time (downtime_id);
CREATE INDEX idx_manufacture_dft on cycle_time(manufacture_defect);
CREATE INDEX idx_start_time on cycle_time(start_time);
CREATE INDEX idx_end_time on cycle_time(end_time);
CREATE INDEX idx_status_id on cycle_time(status_id);