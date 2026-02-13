"""
Database module for PostgreSQL
Railway automatically provides DATABASE_URL
"""

import os
import asyncpg
from typing import Dict, List, Optional


class Database:
    """Async PostgreSQL database handler"""
    
    def __init__(self):
        self.pool = None
        self.database_url = os.environ.get(
            "DATABASE_URL",
            "postgresql://localhost/merger_roi"
        )
    
    async def connect(self):
        """Create connection pool"""
        try:
            self.pool = await asyncpg.create_pool(self.database_url)
            print("✅ Database connected successfully")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            raise
    
    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            print("Database disconnected")
    
    def is_connected(self) -> bool:
        """Check if database is connected"""
        return self.pool is not None
    
    async def create_tables(self):
        """Create database tables if they don't exist"""
        async with self.pool.acquire() as conn:
            # Companies table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS companies (
                    company_id SERIAL PRIMARY KEY,
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
                )
            ''')
            
            # Merger analyses table
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS merger_analyses (
                    analysis_id SERIAL PRIMARY KEY,
                    company_a_id INTEGER REFERENCES companies(company_id),
                    company_b_id INTEGER REFERENCES companies(company_id),
                    merger_cost DECIMAL(15, 2),
                    synergy_rate DECIMAL(5, 2),
                    premium DECIMAL(5, 2),
                    roi_percentage DECIMAL(10, 2),
                    npv DECIMAL(15, 2),
                    irr_percentage DECIMAL(10, 2),
                    payback_period DECIMAL(5, 2),
                    recommendation VARCHAR(100),
                    confidence VARCHAR(50),
                    reasoning TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            print("✅ Tables created successfully")
    
    async def seed_sample_data(self):
        """Add sample companies if database is empty"""
        async with self.pool.acquire() as conn:
            count = await conn.fetchval('SELECT COUNT(*) FROM companies')
            
            if count == 0:
                companies = [
                    ('TechCorp Inc', 50000000, 35000000, 80000000, 30000000, 
                     120000000, 18000000, 12000000, 15000000, 'Technology'),
                    ('DataSystems Ltd', 35000000, 25000000, 60000000, 20000000, 
                     85000000, 12000000, 8000000, 10000000, 'Technology'),
                    ('CloudNet Solutions', 42000000, 30000000, 70000000, 25000000, 
                     95000000, 15000000, 10000000, 12000000, 'Technology'),
                    ('FinanceHub Corp', 80000000, 60000000, 150000000, 50000000, 
                     200000000, 25000000, 18000000, 22000000, 'Finance'),
                    ('RetailMax Group', 65000000, 50000000, 100000000, 40000000, 
                     140000000, 20000000, 13000000, 16000000, 'Retail'),
                ]
                
                await conn.executemany('''
                    INSERT INTO companies 
                    (company_name, annual_revenue, operating_costs, total_assets, 
                     total_liabilities, market_value, ebitda, net_income, cash_flow, industry)
                    VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                ''', companies)
                
                print(f"✅ Seeded {len(companies)} sample companies")
    
    async def get_all_companies(self) -> List[Dict]:
        """Get all companies"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('SELECT * FROM companies ORDER BY company_id')
            return [dict(row) for row in rows]
    
    async def get_company(self, company_id: int) -> Optional[Dict]:
        """Get specific company by ID"""
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT * FROM companies WHERE company_id = $1',
                company_id
            )
            return dict(row) if row else None
    
    async def add_company(self, company: Dict) -> int:
        """Add a new company"""
        async with self.pool.acquire() as conn:
            company_id = await conn.fetchval('''
                INSERT INTO companies 
                (company_name, annual_revenue, operating_costs, total_assets, 
                 total_liabilities, market_value, ebitda, net_income, cash_flow, industry)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
                RETURNING company_id
            ''', 
                company['company_name'],
                company['annual_revenue'],
                company['operating_costs'],
                company['total_assets'],
                company['total_liabilities'],
                company['market_value'],
                company['ebitda'],
                company['net_income'],
                company['cash_flow'],
                company['industry']
            )
            return company_id
    
    async def save_analysis(self, company_a_id: int, company_b_id: int, 
                           result: Dict, synergy_rate: float, premium: float):
        """Save merger analysis to database"""
        async with self.pool.acquire() as conn:
            await conn.execute('''
                INSERT INTO merger_analyses 
                (company_a_id, company_b_id, merger_cost, synergy_rate, premium,
                 roi_percentage, npv, irr_percentage, payback_period, 
                 recommendation, confidence, reasoning)
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12)
            ''',
                company_a_id,
                company_b_id,
                result['merger_cost'],
                synergy_rate * 100,
                premium * 100,
                result['financial_metrics']['roi_percentage'],
                result['financial_metrics']['npv'],
                result['financial_metrics']['irr_percentage'],
                result['financial_metrics']['payback_period_years'],
                result['recommendation'],
                result['confidence'],
                result['reasoning']
            )
    
    async def get_analysis_history(self) -> List[Dict]:
        """Get all merger analyses"""
        async with self.pool.acquire() as conn:
            rows = await conn.fetch('''
                SELECT 
                    ma.*,
                    ca.company_name as company_a_name,
                    cb.company_name as company_b_name
                FROM merger_analyses ma
                JOIN companies ca ON ma.company_a_id = ca.company_id
                JOIN companies cb ON ma.company_b_id = cb.company_id
                ORDER BY ma.created_at DESC
            ''')
            return [dict(row) for row in rows]
    
    async def delete_analysis(self, analysis_id: int):
        """Delete a specific analysis"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                'DELETE FROM merger_analyses WHERE analysis_id = $1',
                analysis_id
            )
