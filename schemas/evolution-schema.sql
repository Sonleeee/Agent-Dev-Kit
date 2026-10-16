-- ADK Evolution Database Schema
-- SQLite + FTS5
-- Version: 1.0.0

PRAGMA journal_mode = WAL;
PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS sessions (
    id TEXT PRIMARY KEY,
    timestamp TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    project TEXT,
    user_intent TEXT,
    workflow_used TEXT,
    outcome TEXT CHECK(outcome IN ('SUCCESS','PARTIAL','FAILED','ABANDONED')),
    total_turns INTEGER DEFAULT 0,
    total_tokens INTEGER DEFAULT 0,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS traces (
    id TEXT PRIMARY KEY,
    session_id TEXT NOT NULL REFERENCES sessions(id),
    task_description TEXT NOT NULL,
    workflow TEXT,
    complexity TEXT CHECK(complexity IN ('Low','Medium','High')),
    outcome TEXT CHECK(outcome IN ('SUCCESS','PARTIAL','FAILED')),
    duration_turns INTEGER DEFAULT 0,
    tokens_used INTEGER DEFAULT 0,
    acceptance_evidence TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS trace_steps (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id TEXT NOT NULL REFERENCES traces(id),
    step_order INTEGER NOT NULL,
    step_type TEXT NOT NULL CHECK(step_type IN ('clarify','plan','impl','review','fix','test','deploy','research','other')),
    description TEXT,
    tool_used TEXT,
    input_summary TEXT,
    output_summary TEXT,
    outcome TEXT CHECK(outcome IN ('pass','fail','skip','retry')),
    tokens INTEGER DEFAULT 0,
    duration_ms INTEGER DEFAULT 0,
    friction_note TEXT
);

CREATE TABLE IF NOT EXISTS friction_points (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id TEXT NOT NULL REFERENCES traces(id),
    step_id INTEGER REFERENCES trace_steps(id),
    category TEXT NOT NULL CHECK(category IN ('skill_gap','unclear_instruction','wrong_tool','missing_context','user_correction','rule_violation','tool_error')),
    description TEXT NOT NULL,
    severity TEXT CHECK(severity IN ('low','medium','high')),
    related_skill TEXT,
    related_rule TEXT,
    suggested_fix TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    name TEXT PRIMARY KEY,
    skill_group TEXT CHECK(skill_group IN ('core','meta','devops','security','testing','research','domain')),
    current_version TEXT DEFAULT '1.0',
    times_used INTEGER DEFAULT 0,
    times_succeeded INTEGER DEFAULT 0,
    times_failed INTEGER DEFAULT 0,
    success_rate REAL GENERATED ALWAYS AS (
        CASE WHEN times_used > 0 THEN CAST(times_succeeded AS REAL) / times_used ELSE 0.0 END
    ) STORED,
    last_used_at TEXT,
    last_evolved_at TEXT
);

CREATE TABLE IF NOT EXISTS skills_used (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trace_id TEXT NOT NULL REFERENCES traces(id),
    skill_name TEXT NOT NULL REFERENCES skills(name),
    outcome TEXT CHECK(outcome IN ('success','partial','failed'))
);

CREATE TABLE IF NOT EXISTS skill_versions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    skill_name TEXT NOT NULL REFERENCES skills(name),
    version TEXT NOT NULL,
    content_hash TEXT,
    change_reason TEXT CHECK(change_reason IN ('manual','synthesis','gepa_evolution','user_feedback','meta_evolution')),
    change_description TEXT,
    performance_before TEXT,
    performance_after TEXT,
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pattern_type TEXT NOT NULL CHECK(pattern_type IN ('recurring_friction','success_pattern','anti_pattern','reusable_procedure')),
    description TEXT NOT NULL,
    occurrence_count INTEGER DEFAULT 1,
    first_seen TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    last_seen TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    status TEXT CHECK(status IN ('active','resolved','evolved','archived')) DEFAULT 'active',
    resolution TEXT
);

CREATE TABLE IF NOT EXISTS evolution_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    target_type TEXT NOT NULL CHECK(target_type IN ('skill','workflow','rule')),
    target_name TEXT NOT NULL,
    trigger TEXT CHECK(trigger IN ('manual','auto','scheduled')),
    strategy TEXT CHECK(strategy IN ('synthesize','optimize','refine')),
    candidates_generated INTEGER DEFAULT 0,
    candidates_evaluated INTEGER DEFAULT 0,
    best_candidate_id INTEGER,
    outcome TEXT CHECK(outcome IN ('upgraded','kept_current','rejected')),
    created_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now'))
);

CREATE TABLE IF NOT EXISTS evolution_candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL REFERENCES evolution_runs(id),
    variant_label TEXT NOT NULL,
    mutation_type TEXT CHECK(mutation_type IN ('reorder','clarify','simplify','add_guard','remove_step','merge_steps','add_example','split_step','conditional')),
    content_diff TEXT,
    score_clarity REAL,
    score_completeness REAL,
    score_conciseness REAL,
    score_trace_replay REAL,
    score_overall REAL,
    evaluation_notes TEXT
);

CREATE TABLE IF NOT EXISTS user_preferences (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    preference_key TEXT NOT NULL UNIQUE,
    preference_value TEXT NOT NULL,
    confidence REAL DEFAULT 0.5,
    source_session TEXT,
    learned_at TEXT NOT NULL DEFAULT (strftime('%Y-%m-%dT%H:%M:%SZ', 'now')),
    last_confirmed TEXT
);

-- Indexes
CREATE INDEX IF NOT EXISTS idx_traces_session ON traces(session_id);
CREATE INDEX IF NOT EXISTS idx_traces_outcome ON traces(outcome);
CREATE INDEX IF NOT EXISTS idx_traces_workflow ON traces(workflow);
CREATE INDEX IF NOT EXISTS idx_traces_created ON traces(created_at);
CREATE INDEX IF NOT EXISTS idx_steps_trace ON trace_steps(trace_id);
CREATE INDEX IF NOT EXISTS idx_friction_trace ON friction_points(trace_id);
CREATE INDEX IF NOT EXISTS idx_friction_category ON friction_points(category);
CREATE INDEX IF NOT EXISTS idx_friction_skill ON friction_points(related_skill);
CREATE INDEX IF NOT EXISTS idx_skills_used_trace ON skills_used(trace_id);
CREATE INDEX IF NOT EXISTS idx_evolution_target ON evolution_runs(target_type, target_name);

-- FTS5 Virtual Tables
CREATE VIRTUAL TABLE IF NOT EXISTS traces_fts USING fts5(
    task_description,
    content='traces',
    content_rowid='rowid'
);

CREATE VIRTUAL TABLE IF NOT EXISTS friction_fts USING fts5(
    description,
    suggested_fix,
    content='friction_points',
    content_rowid='id'
);

-- Triggers to keep FTS in sync
CREATE TRIGGER IF NOT EXISTS traces_ai AFTER INSERT ON traces BEGIN
    INSERT INTO traces_fts(rowid, task_description) VALUES (new.rowid, new.task_description);
END;

CREATE TRIGGER IF NOT EXISTS traces_ad AFTER DELETE ON traces BEGIN
    INSERT INTO traces_fts(traces_fts, rowid, task_description) VALUES('delete', old.rowid, old.task_description);
END;

CREATE TRIGGER IF NOT EXISTS friction_ai AFTER INSERT ON friction_points BEGIN
    INSERT INTO friction_fts(rowid, description, suggested_fix) VALUES (new.id, new.description, new.suggested_fix);
END;

CREATE TRIGGER IF NOT EXISTS friction_ad AFTER DELETE ON friction_points BEGIN
    INSERT INTO friction_fts(friction_fts, rowid, description, suggested_fix) VALUES('delete', old.id, old.description, old.suggested_fix);
END;

-- Useful views
CREATE VIEW IF NOT EXISTS v_skill_health AS
SELECT 
    s.name,
    s.skill_group,
    s.current_version,
    s.times_used,
    s.success_rate,
    s.last_used_at,
    s.last_evolved_at,
    COUNT(DISTINCT fp.id) as total_friction_points,
    CASE
        WHEN s.success_rate >= 0.9 THEN 'healthy'
        WHEN s.success_rate >= 0.7 THEN 'warning'
        ELSE 'critical'
    END as health_status
FROM skills s
LEFT JOIN skills_used su ON s.name = su.skill_name
LEFT JOIN friction_points fp ON su.trace_id = fp.trace_id AND fp.related_skill = s.name
GROUP BY s.name;

CREATE VIEW IF NOT EXISTS v_evolution_effectiveness AS
SELECT
    er.target_type,
    er.strategy,
    COUNT(*) as total_runs,
    SUM(CASE WHEN er.outcome = 'upgraded' THEN 1 ELSE 0 END) as upgrades,
    ROUND(CAST(SUM(CASE WHEN er.outcome = 'upgraded' THEN 1 ELSE 0 END) AS REAL) / COUNT(*) * 100, 1) as upgrade_rate_pct
FROM evolution_runs er
GROUP BY er.target_type, er.strategy;
