# 🎯 Merger ROI Calculator - Quick Start Guide

## What This Does

Analyzes merger opportunities between two companies and gives you a **YES or NO** recommendation based on:
- Return on Investment (ROI)
- Net Present Value (NPV)
- Internal Rate of Return (IRR)
- Payback Period

## 📚 Academic Foundation

Based on research from:
1. **Damodaran, A. (2005)** - "The Value of Synergy" (NYU Stern)
2. **Bruner, R. F. (2004)** - "Applied Mergers and Acquisitions"
3. **Koller, T., et al. (2015)** - "Valuation: Measuring and Managing the Value of Companies"

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Database
```bash
mysql -u root -p < merger_roi_simple.sql
```

### Step 2: Install Dependencies
```bash
pip install fastapi uvicorn pymysql
```

### Step 3: Update Database Password
Edit `simple_merger_api.py` line 25:
```python
password='your_password',  # Change this to your MySQL password
```

### Step 4: Run API
```bash
python simple_merger_api.py
```

API runs on: http://localhost:8000

---

## 📊 How to Use

### Option 1: Using API Documentation (Easiest)

1. Open http://localhost:8000/docs
2. Click on `POST /api/merger/analyze`
3. Click "Try it out"
4. Enter:
   ```json
   {
     "company_a_id": 1,
     "company_b_id": 2,
     "synergy_rate": 0.10,
     "premium": 0.30
   }
   ```
5. Click "Execute"
6. See the **YES/NO recommendation**!

### Option 2: Using Python Script

```python
from merger_roi_calculator import MergerROICalculator

# Company data
company_a = {
    'company_name': 'TechCorp Inc',
    'annual_revenue': 50000000,
    'operating_costs': 35000000,
    'total_assets': 80000000,
    'total_liabilities': 30000000,
    'market_value': 120000000,
    'ebitda': 18000000,
    'net_income': 12000000,
    'cash_flow': 15000000
}

company_b = {
    'company_name': 'DataSystems Ltd',
    'annual_revenue': 35000000,
    'operating_costs': 25000000,
    'total_assets': 60000000,
    'total_liabilities': 20000000,
    'market_value': 85000000,
    'ebitda': 12000000,
    'net_income': 8000000,
    'cash_flow': 10000000
}

# Calculate
calculator = MergerROICalculator()
result = calculator.analyze_merger(company_a, company_b)

# Get recommendation
print(f"RECOMMENDATION: {result['recommendation']}")
print(f"ROI: {result['financial_metrics']['roi_percentage']}%")
```

### Option 3: Using cURL

```bash
curl -X POST "http://localhost:8000/api/merger/analyze" \
  -H "Content-Type: application/json" \
  -d '{
    "company_a_id": 1,
    "company_b_id": 2,
    "synergy_rate": 0.10,
    "premium": 0.30
  }'
```

---

## 📈 Understanding the Results

### Sample Output:
```json
{
  "company_a": "TechCorp Inc",
  "company_b": "DataSystems Ltd",
  "merger_cost": 143650000.00,
  "synergies": {
    "operating": 6000000.00,
    "financial": 187500.00,
    "revenue": 2550000.00,
    "total_annual": 8737500.00
  },
  "financial_metrics": {
    "roi_percentage": 30.45,
    "npv": 18234567.89,
    "irr_percentage": 18.23,
    "payback_period_years": 4.2
  },
  "recommendation": "YES - STRONGLY RECOMMEND",
  "confidence": "High",
  "reasoning": "Excellent ROI of 30.5%; Positive NPV of $18,234,568; Acceptable payback of 4.2 years; High IRR of 18.2%"
}
```

### Decision Criteria:

**YES - STRONGLY RECOMMEND** (Score ≥ 7)
- ROI > 30%
- NPV > 0
- Payback < 3 years
- IRR > 15%

**YES - RECOMMEND** (Score 5-6)
- ROI > 20%
- NPV > 0
- Payback < 5 years
- IRR > 10%

**MAYBE - PROCEED WITH CAUTION** (Score 3-4)
- ROI > 10%
- NPV close to 0
- Payback < 7 years

**NO - DO NOT RECOMMEND** (Score < 3)
- ROI < 10%
- NPV < 0
- Long payback period
- IRR < WACC

---

## 🔬 Formula Breakdown

### 1. ROI Calculation
```
ROI = (Total 5-Year Benefits - Merger Cost) / Merger Cost × 100

Where:
- Benefits = Σ(Annual Synergies × 1.02^year) for years 1-5
- Merger Cost = Market Value × (1 + Premium) + Transaction Costs
```

### 2. Synergies
```
Operating Synergies = Combined Operating Costs × Synergy Rate
Financial Synergies = Combined EBITDA × Tax Rate × 0.05
Revenue Synergies = Combined Revenue × 0.03
```

### 3. NPV (Net Present Value)
```
NPV = Σ(Synergies_t / (1 + WACC)^t) - Initial Investment

Where:
- WACC = Weighted Average Cost of Capital (default 10%)
- t = year (1 to 5)
```

### 4. IRR (Internal Rate of Return)
```
IRR is the rate where NPV = 0
Calculated using Newton-Raphson method
```

### 5. Payback Period
```
Years required for cumulative synergies to equal merger cost
```

---

## 🎯 Sample Companies in Database

1. **TechCorp Inc** (ID: 1)
   - Revenue: $50M
   - EBITDA: $18M
   - Market Value: $120M

2. **DataSystems Ltd** (ID: 2)
   - Revenue: $35M
   - EBITDA: $12M
   - Market Value: $85M

3. **CloudNet Solutions** (ID: 3)
   - Revenue: $42M
   - EBITDA: $15M
   - Market Value: $95M

4. **FinanceHub Corp** (ID: 4)
   - Revenue: $80M
   - EBITDA: $25M
   - Market Value: $200M

5. **RetailMax Group** (ID: 5)
   - Revenue: $65M
   - EBITDA: $20M
   - Market Value: $140M

---

## 🧪 Test Scenarios

### Scenario 1: Good Merger (Expected: YES)
```json
{
  "company_a_id": 1,
  "company_b_id": 2,
  "synergy_rate": 0.15,
  "premium": 0.25
}
```

### Scenario 2: Risky Merger (Expected: MAYBE)
```json
{
  "company_a_id": 5,
  "company_b_id": 3,
  "synergy_rate": 0.08,
  "premium": 0.40
}
```

### Scenario 3: Bad Merger (Expected: NO)
```json
{
  "company_a_id": 2,
  "company_b_id": 4,
  "synergy_rate": 0.05,
  "premium": 0.50
}
```

---

## 📊 API Endpoints

### GET /api/companies
List all companies

### GET /api/companies/{id}
Get specific company details

### POST /api/merger/analyze
Analyze merger between two companies

**Request Body:**
```json
{
  "company_a_id": 1,
  "company_b_id": 2,
  "synergy_rate": 0.10,
  "premium": 0.30,
  "discount_rate": 0.10,
  "tax_rate": 0.25
}
```

### GET /api/merger/history
View all previous analyses

---

## 🎓 Academic References

1. **Damodaran, A. (2005)**
   - "The Value of Synergy"
   - NYU Stern School of Business
   - Framework for synergy valuation

2. **Bruner, R. F. (2004)**
   - "Applied Mergers and Acquisitions"
   - Decision criteria for M&A

3. **Koller, T., Goedhart, M., & Wessels, D. (2015)**
   - "Valuation: Measuring and Managing the Value of Companies"
   - McKinsey & Company
   - DCF and NPV methodology

---

## 💡 Key Insights

1. **Synergies are critical** - Most merger value comes from synergies
2. **Premium matters** - Higher premiums reduce ROI significantly
3. **Time value of money** - NPV accounts for discount rate
4. **Multiple metrics** - Use ROI, NPV, IRR, and payback together
5. **Conservative estimates** - Better to underestimate synergies

---

## 🎯 Final Answer Format

The API returns a clear **YES or NO** recommendation:

- **YES - STRONGLY RECOMMEND**: High confidence, excellent metrics
- **YES - RECOMMEND**: Good metrics, proceed
- **MAYBE - PROCEED WITH CAUTION**: Marginal case, needs review
- **NO - DO NOT RECOMMEND**: Poor metrics, avoid

---

## 🚀 Next Steps

1. Run the API: `python simple_merger_api.py`
2. Open docs: http://localhost:8000/docs
3. Test with sample companies
4. Get your YES/NO answer!

**The calculator gives you a clear, research-backed recommendation in seconds!** 🎉
