"""
Simple Merger ROI API
FastAPI endpoint to analyze merger between two companies
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import pymysql
from merger_roi_calculator import MergerROICalculator

app = FastAPI(title="Merger ROI Calculator API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database connection
def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='your_password',  # Change this
        database='merger_roi_simple',
        cursorclass=pymysql.cursors.DictCursor
    )

class MergerRequest(BaseModel):
    company_a_id: int
    company_b_id: int
    synergy_rate: Optional[float] = 0.10
    premium: Optional[float] = 0.30
    discount_rate: Optional[float] = 0.10
    tax_rate: Optional[float] = 0.25


@app.get("/")
def root():
    return {
        "message": "Merger ROI Calculator API",
        "version": "1.0.0",
        "endpoints": {
            "companies": "/api/companies",
            "analyze": "/api/merger/analyze"
        }
    }


@app.get("/api/companies")
def get_companies():
    """Get all companies from database"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM companies")
            companies = cursor.fetchall()
        conn.close()
        
        return {
            "companies": companies,
            "count": len(companies)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/companies/{company_id}")
def get_company(company_id: int):
    """Get specific company details"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM companies WHERE company_id = %s", (company_id,))
            company = cursor.fetchone()
        conn.close()
        
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        
        return company
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/merger/analyze")
def analyze_merger(request: MergerRequest):
    """
    Analyze merger between two companies
    
    Returns comprehensive ROI analysis with YES/NO recommendation
    """
    try:
        # Get company data from database
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM companies WHERE company_id = %s", (request.company_a_id,))
            company_a = cursor.fetchone()
            
            cursor.execute("SELECT * FROM companies WHERE company_id = %s", (request.company_b_id,))
            company_b = cursor.fetchone()
        conn.close()
        
        if not company_a:
            raise HTTPException(status_code=404, detail=f"Company A (ID: {request.company_a_id}) not found")
        if not company_b:
            raise HTTPException(status_code=404, detail=f"Company B (ID: {request.company_b_id}) not found")
        
        # Initialize calculator
        calculator = MergerROICalculator(
            discount_rate=request.discount_rate,
            tax_rate=request.tax_rate
        )
        
        # Perform analysis
        result = calculator.analyze_merger(
            company_a,
            company_b,
            synergy_rate=request.synergy_rate,
            premium=request.premium
        )
        
        # Save to database
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO merger_scenarios 
                    (company_a_id, company_b_id, merger_cost, synergy_percentage, 
                     roi_percentage, npv, payback_period, recommendation)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    request.company_a_id,
                    request.company_b_id,
                    result['merger_cost'],
                    request.synergy_rate * 100,
                    result['financial_metrics']['roi_percentage'],
                    result['financial_metrics']['npv'],
                    result['financial_metrics']['payback_period_years'],
                    result['recommendation']
                ))
                conn.commit()
            conn.close()
        except Exception as e:
            print(f"Warning: Could not save to database: {e}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/merger/history")
def get_merger_history():
    """Get all previous merger analyses"""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    ms.*,
                    ca.company_name as company_a_name,
                    cb.company_name as company_b_name
                FROM merger_scenarios ms
                JOIN companies ca ON ms.company_a_id = ca.company_id
                JOIN companies cb ON ms.company_b_id = cb.company_id
                ORDER BY ms.created_at DESC
            """)
            scenarios = cursor.fetchall()
        conn.close()
        
        return {
            "scenarios": scenarios,
            "count": len(scenarios)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
