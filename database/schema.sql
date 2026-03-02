-- database/schema.sql
CREATE DATABASE IF NOT EXISTS cyber_investigation;
USE cyber_investigation;

-- ─── Cases ────────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS cases (
    case_id       INT PRIMARY KEY AUTO_INCREMENT,
    case_name     VARCHAR(255) NOT NULL,
    investigator  VARCHAR(255),
    description   TEXT,
    status        ENUM('open','closed','pending') DEFAULT 'open',
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- ─── Evidence ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS evidence (
    evidence_id   INT PRIMARY KEY AUTO_INCREMENT,
    case_id       INT NOT NULL,
    file_name     VARCHAR(255) NOT NULL,
    file_type     VARCHAR(50),
    file_path     VARCHAR(500),
    uploaded_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    summary       TEXT,                    -- LLM-generated summary
    vector_ids    TEXT,                    -- ChromaDB chunk IDs (JSON array)
    chunk_count   INT DEFAULT 0,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE CASCADE
);

-- ─── Query / Audit Logs ───────────────────────────────────────
CREATE TABLE IF NOT EXISTS query_logs (
    log_id        INT PRIMARY KEY AUTO_INCREMENT,
    case_id       INT,
    investigator  VARCHAR(255),
    query_text    TEXT NOT NULL,
    response_text TEXT,
    model_used    VARCHAR(100),            -- 'ollama_phi3' or 'airllm_llama3'
    sources_cited TEXT,                    -- JSON array of source references
    timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (case_id) REFERENCES cases(case_id) ON DELETE SET NULL
);

-- ─── Cyber Law References ─────────────────────────────────────
CREATE TABLE IF NOT EXISTS law_references (
    ref_id        INT PRIMARY KEY AUTO_INCREMENT,
    act_name      VARCHAR(255) NOT NULL,   -- e.g. "IT Act 2000"
    section       VARCHAR(100),            -- e.g. "Section 66C"
    title         VARCHAR(255),            -- e.g. "Identity Theft"
    description   TEXT,
    punishment    TEXT,
    keywords      TEXT                     -- comma-separated for quick lookup
);

-- ─── System Logs ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS system_logs (
    id            INT PRIMARY KEY AUTO_INCREMENT,
    level         ENUM('INFO','WARNING','ERROR') DEFAULT 'INFO',
    module        VARCHAR(100),
    message       TEXT,
    timestamp     TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);