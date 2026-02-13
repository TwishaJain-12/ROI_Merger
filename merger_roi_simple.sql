-- Simple Merger ROI Database
-- Two companies with financial data for merger analysis

CREATE DATABASE IF NOT EXISTS merger_roi_simple;
USE merger_roi_simple;

-- Company financial data table
CREATE TABLE companies (
    company_id INT PRIMARY KEY AUTO_INCREMENT,
    company_name VARCHAR(255) NOT NULL,
    annual_revenue DECIMAL(15, 2) NOT NULL,
    operating_costs DECIMAL(15, 2) NOT NULL,
    total_assets DECIMAL(15, 2) NOT NULL,
    total_liabilities DECIMAL(15, 2) NOT NULL,
    market_value DECIMAL(15, 2) NOT NULL,
    ebitda DECIMAL(15, 2) NOT NULL,
    net_income DECIMAL(15, 2) NOT NULL,
    cash_flow DECIMAL(15, 2) NOT NULL,
    industry VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample companies
INSERT INTO companies (company_name, annual_revenue, operating_costs, total_assets, total_liabilities, market_value, ebitda, net_income, cash_flow, industry) VALUES
('TechCorp Inc', 50000000.00, 35000000.00, 80000000.00, 30000000.00, 120000000.00, 18000000.00, 12000000.00, 15000000.00, 'Technology'),
('DataSystems Ltd', 35000000.00, 25000000.00, 60000000.00, 20000000.00, 85000000.00, 12000000.00, 8000000.00, 10000000.00, 'Technology'),
('CloudNet Solutions', 42000000.00, 30000000.00, 70000000.00, 25000000.00, 95000000.00, 15000000.00, 10000000.00, 12000000.00, 'Technology'),
('FinanceHub Corp', 80000000.00, 60000000.00, 150000000.00, 50000000.00, 200000000.00, 25000000.00, 18000000.00, 22000000.00, 'Finance'),
('RetailMax Group', 65000000.00, 50000000.00, 100000000.00, 40000000.00, 140000000.00, 20000000.00, 13000000.00, 16000000.00, 'Retail');

-- Merger scenarios table (for storing analysis results)
CREATE TABLE merger_scenarios (
    scenario_id INT PRIMARY KEY AUTO_INCREMENT,
    company_a_id INT NOT NULL,
    company_b_id INT NOT NULL,
    merger_cost DECIMAL(15, 2) NOT NULL,
    synergy_percentage DECIMAL(5, 2) DEFAULT 10.00,
    roi_percentage DECIMAL(10, 2),
    npv DECIMAL(15, 2),
    payback_period DECIMAL(5, 2),
    recommendation VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (company_a_id) REFERENCES companies(company_id),
    FOREIGN KEY (company_b_id) REFERENCES companies(company_id)
);
