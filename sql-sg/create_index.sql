CREATE INDEX idx_drive ON shift_report (tunnel_drive);
CREATE INDEX idx_created_at ON shift_report (created_at);
CREATE INDEX idx_end_ring ON shift_report (end_ring);

CREATE INDEX idx_downtime_id ON shift_cycle_time (downtime_id);
CREATE INDEX idx_breakdown_id ON shift_cycle_time (breakdown_id);
CREATE INDEX idx_remarks ON shift_cycle_time (remarks);