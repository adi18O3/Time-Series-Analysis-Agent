CREATE DATABASE IF NOT EXISTS timeseries_agent;

USE timeseries_agent;

CREATE TABLE IF NOT EXISTS conversation_memory (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_query TEXT NOT NULL,
    analysis_plan JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);