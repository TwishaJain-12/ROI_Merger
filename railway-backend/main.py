"""
Merger ROI Dashboard - Backend API for Railway Deployment
Standalone FastAPI application without Docker
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List, Dict, Any
import os
from datetime import datetime
import pymysql
from contextlib import contextmanager

# ============================================================================
# CONFIGURATION
# ============================================================================

class Config:
    """Application configuration from environment variables"""
    
    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "merger_roi_db")
    
    # API
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("PORT", "8000"))
    
    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

config = Config()

# ============================================================================
# DATABASE CONNECTION
# ============================================================================

@contextmanager
def get_db_connection():
    """Context manager for database connections"""
    connection = None
    try:
        connection = pymysql.connect(
            host=config.DB_HOST,
            port=config.DB_PORT,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_NAME,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=10
        )
        yield connection
    except pymysql.Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    finally:
        if connection:
            connection.close()

def execute_query(query: str, params: tuple = None) -> List[Dict]:
    """Execute a SELECT query and return results"""
    with get_db_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params or ())
            return cursor.fetchall()

# ============================================================================
# FASTAPI APPLICATION
# ============================================================================

app = FastAPI(
    title="Merger ROI Dashboard API",
    description="RESTful API for merger and acquisition ROI analysis",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# API ENDPOINTS
# ============================================================================

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Merger ROI Dashboard API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute("SELECT 1")
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "database": "disconnected", "error": str(e)}

@app.get("/api/firms")
async def get_firms(
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0)
):
    """Get all firms with pagination"""
    query = """
        SELECT 
            f.firm_id,
            f.firm_name,
            f.industry,
            f.founded_year,
            f.total_capital,
            f.headquarters,
            COUNT(DISTINCT s.staff_id) as staff_count,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        GROUP BY f.firm_id, f.firm_name, f.industry, f.founded_year, f.total_capital, f.headquarters
        LIMIT %s OFFSET %s
    """
    firms = execute_query(query, (limit, offset))
    
    # Convert Decimal to float for JSON serialization
    for firm in firms:
        if firm.get('total_capital'):
            firm['total_capital'] = float(firm['total_capital'])
        if firm.get('total_revenue'):
            firm['total_revenue'] = float(firm['total_revenue'])
    
    return {"firms": firms, "count": len(firms)}

@app.get("/api/firms/{firm_id}")
async def get_firm_detail(firm_id: int):
    """Get detailed information about a specific firm"""
    firm_query = """
        SELECT 
            f.*,
            COUNT(DISTINCT s.staff_id) as staff_count,
            COALESCE(SUM(s.salary), 0) as total_salary,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue,
            COUNT(DISTINCT sales.sale_id) as transaction_count
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        WHERE f.firm_id = %s
        GROUP BY f.firm_id
    """
    firms = execute_query(firm_query, (firm_id,))
    
    if not firms:
        raise HTTPException(status_code=404, detail="Firm not found")
    
    firm = firms[0]
    
    # Convert Decimal to float
    for key in ['total_capital', 'total_salary', 'total_revenue']:
        if firm.get(key):
            firm[key] = float(firm[key])
    
    # Get staff
    staff_query = "SELECT * FROM staff WHERE firm_id = %s"
    staff = execute_query(staff_query, (firm_id,))
    
    # Get sales
    sales_query = "SELECT * FROM sales WHERE firm_id = %s ORDER BY sale_date DESC LIMIT 50"
    sales = execute_query(sales_query, (firm_id,))
    
    return {
        "firm": firm,
        "staff": staff,
        "recent_sales": sales
    }

@app.get("/api/roi")
async def calculate_roi():
    """Calculate ROI for all firms"""
    query = """
        SELECT 
            f.firm_id,
            f.firm_name,
            f.total_capital,
            COALESCE(SUM(s.salary), 0) as total_costs,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        GROUP BY f.firm_id, f.firm_name, f.total_capital
    """
    firms = execute_query(query)
    
    roi_results = []
    for firm in firms:
        total_costs = float(firm['total_costs']) if firm['total_costs'] else 0
        total_revenue = float(firm['total_revenue']) if firm['total_revenue'] else 0
        total_capital = float(firm['total_capital']) if firm['total_capital'] else 0
        
        total_investment = total_costs + total_capital
        
        if total_investment > 0:
            roi_percentage = ((total_revenue - total_investment) / total_investment) * 100
        else:
            roi_percentage = 0
        
        roi_results.append({
            "firm_id": firm['firm_id'],
            "firm_name": firm['firm_name'],
            "total_revenue": total_revenue,
            "total_costs": total_costs,
            "total_capital": total_capital,
            "total_investment": total_investment,
            "roi_percentage": round(roi_percentage, 2),
            "status": "positive" if roi_percentage > 0 else "negative"
        })
    
    # Sort by ROI
    roi_results.sort(key=lambda x: x['roi_percentage'], reverse=True)
    
    return {"roi_data": roi_results}

@app.get("/api/capital-productivity")
async def analyze_capital_productivity():
    """Analyze human capital productivity"""
    query = """
        SELECT 
            f.firm_id,
            f.firm_name,
            COUNT(DISTINCT s.staff_id) as staff_count,
            COALESCE(SUM(s.salary), 0) as total_salary,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        GROUP BY f.firm_id, f.firm_name
        HAVING staff_count > 0
    """
    firms = execute_query(query)
    
    productivity_results = []
    for firm in firms:
        staff_count = firm['staff_count']
        total_revenue = float(firm['total_revenue']) if firm['total_revenue'] else 0
        total_salary = float(firm['total_salary']) if firm['total_salary'] else 0
        
        revenue_per_employee = total_revenue / staff_count if staff_count > 0 else 0
        cost_per_employee = total_salary / staff_count if staff_count > 0 else 0
        
        productivity_results.append({
            "firm_id": firm['firm_id'],
            "firm_name": firm['firm_name'],
            "staff_count": staff_count,
            "total_revenue": total_revenue,
            "total_salary": total_salary,
            "revenue_per_employee": round(revenue_per_employee, 2),
            "cost_per_employee": round(cost_per_employee, 2),
            "productivity_ratio": round(revenue_per_employee / cost_per_employee, 2) if cost_per_employee > 0 else 0
        })
    
    return {"productivity_data": productivity_results}

@app.get("/api/bottlenecks")
async def detect_bottlenecks():
    """Detect sales bottlenecks and declining trends"""
    query = """
        SELECT 
            f.firm_id,
            f.firm_name,
            DATE_FORMAT(s.sale_date, '%Y-%m') as period,
            SUM(s.total_amount) as period_revenue,
            COUNT(*) as transaction_count
        FROM firm f
        JOIN sales s ON f.firm_id = s.firm_id
        WHERE s.sale_date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
        GROUP BY f.firm_id, f.firm_name, DATE_FORMAT(s.sale_date, '%Y-%m')
        ORDER BY f.firm_id, period
    """
    data = execute_query(query)
    
    # Group by firm
    firms_data = {}
    for row in data:
        firm_id = row['firm_id']
        if firm_id not in firms_data:
            firms_data[firm_id] = {
                "firm_id": firm_id,
                "firm_name": row['firm_name'],
                "periods": []
            }
        firms_data[firm_id]["periods"].append({
            "period": row['period'],
            "revenue": float(row['period_revenue']),
            "transactions": row['transaction_count']
        })
    
    bottlenecks = []
    for firm_id, firm_data in firms_data.items():
        periods = firm_data["periods"]
        if len(periods) >= 2:
            # Check for declining trend
            recent_revenue = periods[-1]["revenue"]
            previous_revenue = periods[-2]["revenue"]
            
            if previous_revenue > 0:
                decline_percentage = ((recent_revenue - previous_revenue) / previous_revenue) * 100
                
                if decline_percentage < -10:  # More than 10% decline
                    bottlenecks.append({
                        "firm_id": firm_id,
                        "firm_name": firm_data["firm_name"],
                        "issue": "Sales Decline",
                        "severity": "high" if decline_percentage < -20 else "medium",
                        "decline_percentage": round(decline_percentage, 2),
                        "recent_revenue": recent_revenue,
                        "previous_revenue": previous_revenue
                    })
    
    return {"bottlenecks": bottlenecks}

@app.get("/api/resource-optimization")
async def optimize_resources():
    """Provide resource optimization recommendations"""
    query = """
        SELECT 
            f.firm_id,
            f.firm_name,
            COUNT(DISTINCT s.staff_id) as staff_count,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        GROUP BY f.firm_id, f.firm_name
        HAVING staff_count > 0
    """
    firms = execute_query(query)
    
    # Calculate revenue per employee for each firm
    firms_with_metrics = []
    for firm in firms:
        staff_count = firm['staff_count']
        total_revenue = float(firm['total_revenue']) if firm['total_revenue'] else 0
        revenue_per_employee = total_revenue / staff_count if staff_count > 0 else 0
        
        firms_with_metrics.append({
            "firm_id": firm['firm_id'],
            "firm_name": firm['firm_name'],
            "staff_count": staff_count,
            "total_revenue": total_revenue,
            "revenue_per_employee": revenue_per_employee
        })
    
    # Calculate average
    if firms_with_metrics:
        avg_revenue_per_employee = sum(f['revenue_per_employee'] for f in firms_with_metrics) / len(firms_with_metrics)
    else:
        avg_revenue_per_employee = 0
    
    recommendations = []
    for firm in firms_with_metrics:
        if firm['revenue_per_employee'] < avg_revenue_per_employee * 0.7:  # 30% below average
            recommendations.append({
                "firm_id": firm['firm_id'],
                "firm_name": firm['firm_name'],
                "current_staff": firm['staff_count'],
                "revenue_per_employee": round(firm['revenue_per_employee'], 2),
                "average_revenue_per_employee": round(avg_revenue_per_employee, 2),
                "recommendation": "Consider staff reduction or revenue improvement initiatives",
                "priority": "high"
            })
        elif firm['revenue_per_employee'] > avg_revenue_per_employee * 1.5:  # 50% above average
            recommendations.append({
                "firm_id": firm['firm_id'],
                "firm_name": firm['firm_name'],
                "current_staff": firm['staff_count'],
                "revenue_per_employee": round(firm['revenue_per_employee'], 2),
                "average_revenue_per_employee": round(avg_revenue_per_employee, 2),
                "recommendation": "High performer - consider expansion or staff increase",
                "priority": "medium"
            })
    
    return {"recommendations": recommendations}

@app.post("/api/merger/analyze")
async def analyze_merger(firm_a_id: int, firm_b_id: int):
    """Analyze potential merger between two firms"""
    # Get firm data
    query = """
        SELECT 
            f.firm_id,
            f.firm_name,
            f.total_capital,
            COUNT(DISTINCT s.staff_id) as staff_count,
            COALESCE(SUM(s.salary), 0) as total_salary,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        WHERE f.firm_id IN (%s, %s)
        GROUP BY f.firm_id, f.firm_name, f.total_capital
    """
    firms = execute_query(query, (firm_a_id, firm_b_id))
    
    if len(firms) != 2:
        raise HTTPException(status_code=404, detail="One or both firms not found")
    
    firm_a = firms[0] if firms[0]['firm_id'] == firm_a_id else firms[1]
    firm_b = firms[1] if firms[1]['firm_id'] == firm_b_id else firms[0]
    
    # Calculate metrics
    combined_revenue = float(firm_a['total_revenue']) + float(firm_b['total_revenue'])
    combined_costs = float(firm_a['total_salary']) + float(firm_b['total_salary'])
    combined_capital = float(firm_a['total_capital']) + float(firm_b['total_capital'])
    combined_staff = firm_a['staff_count'] + firm_b['staff_count']
    
    # Estimate synergies (10% cost reduction)
    estimated_synergies = combined_costs * 0.10
    adjusted_costs = combined_costs - estimated_synergies
    
    # Calculate ROI
    total_investment = adjusted_costs + combined_capital
    if total_investment > 0:
        merger_roi = ((combined_revenue - total_investment) / total_investment) * 100
    else:
        merger_roi = 0
    
    # Equity distribution based on capital contribution
    total_capital = float(firm_a['total_capital']) + float(firm_b['total_capital'])
    if total_capital > 0:
        firm_a_equity = (float(firm_a['total_capital']) / total_capital) * 100
        firm_b_equity = (float(firm_b['total_capital']) / total_capital) * 100
    else:
        firm_a_equity = 50
        firm_b_equity = 50
    
    return {
        "firm_a": {
            "firm_id": firm_a['firm_id'],
            "firm_name": firm_a['firm_name'],
            "revenue": float(firm_a['total_revenue']),
            "equity_percentage": round(firm_a_equity, 2)
        },
        "firm_b": {
            "firm_id": firm_b['firm_id'],
            "firm_name": firm_b['firm_name'],
            "revenue": float(firm_b['total_revenue']),
            "equity_percentage": round(firm_b_equity, 2)
        },
        "merger_analysis": {
            "combined_revenue": round(combined_revenue, 2),
            "combined_costs": round(combined_costs, 2),
            "estimated_synergies": round(estimated_synergies, 2),
            "adjusted_costs": round(adjusted_costs, 2),
            "combined_capital": round(combined_capital, 2),
            "combined_staff": combined_staff,
            "merger_roi_percentage": round(merger_roi, 2),
            "recommendation": "Proceed with merger" if merger_roi > 15 else "Reconsider merger terms"
        }
    }

@app.get("/api/dashboard/summary")
async def get_dashboard_summary():
    """Get summary statistics for dashboard"""
    # Total firms
    firms_query = "SELECT COUNT(*) as count FROM firm"
    firms_result = execute_query(firms_query)
    total_firms = firms_result[0]['count']
    
    # Total staff
    staff_query = "SELECT COUNT(*) as count FROM staff"
    staff_result = execute_query(staff_query)
    total_staff = staff_result[0]['count']
    
    # Total revenue
    revenue_query = "SELECT COALESCE(SUM(total_amount), 0) as total FROM sales"
    revenue_result = execute_query(revenue_query)
    total_revenue = float(revenue_result[0]['total'])
    
    # Average ROI
    roi_query = """
        SELECT 
            f.firm_id,
            f.total_capital,
            COALESCE(SUM(s.salary), 0) as total_costs,
            COALESCE(SUM(sales.total_amount), 0) as total_revenue
        FROM firm f
        LEFT JOIN staff s ON f.firm_id = s.firm_id
        LEFT JOIN sales ON f.firm_id = sales.firm_id
        GROUP BY f.firm_id, f.total_capital
    """
    roi_data = execute_query(roi_query)
    
    roi_values = []
    for firm in roi_data:
        total_investment = float(firm['total_costs']) + float(firm['total_capital'])
        if total_investment > 0:
            roi = ((float(firm['total_revenue']) - total_investment) / total_investment) * 100
            roi_values.append(roi)
    
    average_roi = sum(roi_values) / len(roi_values) if roi_values else 0
    
    return {
        "total_firms": total_firms,
        "total_staff": total_staff,
        "total_revenue": round(total_revenue, 2),
        "average_roi": round(average_roi, 2)
    }

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config.API_HOST, port=config.API_PORT)
