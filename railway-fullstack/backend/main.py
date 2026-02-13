"""
Merger ROI Calculator - FastAPI Backend
Full-stack application for Railway deployment
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import os
from calculator import MergerROICalculator
from database import Database

app = FastAPI(
    title="Merger ROI Calculator API",
    description="Analyze merger opportunities with research-backed ROI calculations",
    version="1.0.0"
)

# CORS - Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
db = Database()

# Pydantic models
class Company(BaseModel):
    company_name: str
    annual_revenue: float
    operating_costs: float
    total_assets: float
    total_liabilities: float
    market_value: float
    ebitda: float
    net_income: float
    cash_flow: float
    industry: str

class MergerRequest(BaseModel):
    company_a_id: int
    company_b_id: int
    synergy_rate: Optional[float] = 0.10
    premium: Optional[float] = 0.30
    discount_rate: Optional[float] = 0.10
    tax_rate: Optional[float] = 0.25


@app.on_event("startup")
async def startup():
    """Initialize database on startup"""
    await db.connect()
    await db.create_tables()
    await db.seed_sample_data()


@app.on_event("shutdown")
async def shutdown():
    """Close database connection on shutdown"""
    await db.disconnect()


@app.get("/")
def root():
    """API root endpoint"""
    return {
        "name": "Merger ROI Calculator API",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "companies": "/api/companies",
            "analyze": "/api/analyze",
            "history": "/api/history",
            "docs": "/docs"
        }
    }


@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "database": "connected" if db.is_connected() else "disconnected"
    }


@app.get("/api/companies")
async def get_companies():
    """Get all companies"""
    try:
        companies = await db.get_all_companies()
        return {
            "companies": companies,
            "count": len(companies)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/companies/{company_id}")
async def get_company(company_id: int):
    """Get specific company by ID"""
    try:
        company = await db.get_company(company_id)
        if not company:
            raise HTTPException(status_code=404, detail="Company not found")
        return company
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/companies")
async def create_company(company: Company):
    """Add a new company"""
    try:
        company_id = await db.add_company(company.dict())
        return {
            "message": "Company created successfully",
            "company_id": company_id
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/analyze")
async def analyze_merger(request: MergerRequest):
    """
    Analyze merger between two companies
    Returns comprehensive ROI analysis with YES/NO recommendation
    """
    try:
        # Get company data
        company_a = await db.get_company(request.company_a_id)
        company_b = await db.get_company(request.company_b_id)
        
        if not company_a:
            raise HTTPException(
                status_code=404,
                detail=f"Company A (ID: {request.company_a_id}) not found"
            )
        if not company_b:
            raise HTTPException(
                status_code=404,
                detail=f"Company B (ID: {request.company_b_id}) not found"
            )
        
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
        
        # Save analysis to database
        await db.save_analysis(
            company_a_id=request.company_a_id,
            company_b_id=request.company_b_id,
            result=result,
            synergy_rate=request.synergy_rate,
            premium=request.premium
        )
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/history")
async def get_analysis_history():
    """Get all previous merger analyses"""
    try:
        history = await db.get_analysis_history()
        return {
            "analyses": history,
            "count": len(history)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/api/history/{analysis_id}")
async def delete_analysis(analysis_id: int):
    """Delete a specific analysis"""
    try:
        await db.delete_analysis(analysis_id)
        return {"message": "Analysis deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
