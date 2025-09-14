-- Database Schema for Selenium Automation Configurations
-- This schema is designed to store configurations for Selenium scripts, including websites to navigate, tasks, sequences of actions (e.g., navigate, click, input), selectors for elements, and conditions for branching logic.
-- It allows dynamic scripting: Query the DB for a task, execute actions in order using Selenium in Python.
-- Based on best practices from test management systems (e.g., TestRail, TestLink) and automation frameworks: Normalization for reusability, indexing for performance, JSONB for flexible configs.
-- Assumes PostgreSQL; adaptable to MySQL/SQLite. Suitable for storing thousands of tasks/actions.

-- Table: Websites
-- Stores target websites for navigation.
CREATE TABLE Websites (
    website_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,  -- e.g., 'E-commerce Site'
    base_url VARCHAR(512) NOT NULL,     -- e.g., 'https://example.com'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Tasks
-- Defines automation tasks (e.g., 'Login and Checkout').
CREATE TABLE Tasks (
    task_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,  -- e.g., 'Automated Login Sequence'
    website_id INTEGER REFERENCES Websites(website_id) ON DELETE CASCADE,
    start_path VARCHAR(255) DEFAULT '/',  -- Relative path for initial navigation (e.g., '/login')
    timeout_seconds INTEGER DEFAULT 30,   -- Global timeout for actions
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: ActionTypes
-- Predefined action types for Selenium (e.g., navigate, click).
CREATE TABLE ActionTypes (
    type_id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL UNIQUE,   -- e.g., 'navigate', 'click', 'input_text', 'wait_for_element'
    description TEXT                    -- e.g., 'Navigates to a URL'
);

-- Sample Inserts for Common Actions
INSERT INTO ActionTypes (name, description) VALUES
('navigate', 'Navigates to a specific URL or path'),
('click', 'Clicks on an element using selector'),
('input_text', 'Inputs text into a form field'),
('wait_for_element', 'Waits until element is visible/clickable'),
('extract_data', 'Extracts text or attribute from element'),
('scroll_to', 'Scrolls to an element or page bottom');

-- Table: Selectors
-- Reusable element locators (e.g., XPath for buttons).
CREATE TABLE Selectors (
    selector_id SERIAL PRIMARY KEY,
    website_id INTEGER REFERENCES Websites(website_id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,         -- e.g., 'Login Button'
    selector_type ENUM('xpath', 'css', 'id', 'class', 'name') NOT NULL,
    selector_value TEXT NOT NULL,       -- e.g., '//button[@id="login"]'
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table: Actions
-- Sequence of steps for a task, telling Selenium what to do.
CREATE TABLE Actions (
    action_id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES Tasks(task_id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL,   -- Order of execution (1 = first)
    action_type_id INTEGER REFERENCES ActionTypes(type_id),
    selector_id INTEGER REFERENCES Selectors(selector_id),  -- For actions like click/input
    target_url_or_path TEXT,            -- For 'navigate': Full URL or relative path
    input_value TEXT,                   -- For 'input_text': Value to enter
    wait_condition TEXT,                -- e.g., 'visible' or 'clickable'
    timeout_seconds INTEGER,            -- Override global timeout
    optional BOOLEAN DEFAULT FALSE,     -- Skip if element not found
    description TEXT,                   -- e.g., 'Navigate to login page and click submit'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(task_id, sequence_number)    -- Ensure ordered uniqueness
);

-- Table: Conditions
-- Optional branching for actions (e.g., 'if element exists, click else skip').
CREATE TABLE Conditions (
    condition_id SERIAL PRIMARY KEY,
    action_id INTEGER REFERENCES Actions(action_id) ON DELETE CASCADE,
    condition_type ENUM('element_exists', 'text_matches', 'url_contains') NOT NULL,
    check_selector_id INTEGER REFERENCES Selectors(selector_id),
    expected_value TEXT,                -- e.g., 'Logged In' for text_matches
    on_true_action_id INTEGER REFERENCES Actions(action_id),  -- Next if true
    on_false_action_id INTEGER REFERENCES Actions(action_id), -- Next if false
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for Performance
CREATE INDEX idx_actions_task ON Actions(task_id);
CREATE INDEX idx_selectors_website ON Selectors(website_id);

-- Example Usage:
-- 1. Insert Website: INSERT INTO Websites (name, base_url) VALUES ('Demo Site', 'https://example.com');
-- 2. Insert Task: INSERT INTO Tasks (name, website_id) VALUES ('Login Task', 1);
-- 3. Insert Selector: INSERT INTO Selectors (website_id, name, selector_type, selector_value) VALUES (1, 'Login Button', 'id', 'login-btn');
-- 4. Insert Actions: 
--    - Navigate: INSERT INTO Actions (task_id, sequence_number, action_type_id, target_url_or_path) VALUES (1, 1, (SELECT type_id FROM ActionTypes WHERE name='navigate'), '/login');
--    - Click: INSERT INTO Actions (task_id, sequence_number, action_type_id, selector_id) VALUES (1, 2, (SELECT type_id FROM ActionTypes WHERE name='click'), 1);

-- In Python/Selenium: Query DB for task actions ordered by sequence_number, then execute (e.g., driver.get(base_url + target_url_or_path) for navigate).