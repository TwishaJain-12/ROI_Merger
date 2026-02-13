# Merger ROI Dashboard

A comprehensive Business & Management SaaS platform for analyzing merger opportunities, measuring capital efficiency, and optimizing resource allocation using pure statistical analysis (no AI/ML).

## Features

- **ROI Analysis**: Calculate return on investment for firms and merger opportunities
- **Capital Measurement**: Measure aggregate production functions for strategic planning
- **Real-Time Dashboard**: Track team tasks, resource allocation, and performance metrics
- **Bottleneck Detection**: Identify workflow constraints using statistical analysis
- **Resource Optimization**: Data-driven recommendations for staff and capital allocation
- **Merger Analysis**: Evaluate equity distribution and synergies for merger opportunities

## Technology Stack

### Backend
- Python 3.9+
- FastAPI
- MySQL 8.0
- PyMySQL

### Frontend
- React 18
- Recharts for visualizations
- Axios for API calls

## Installation

### Prerequisites
- Python 3.9+
- Node.js 18+
- MySQL 8.0+
- Docker (optional)

### Setup with Docker

1. Clone the repository
2. Copy `.env.example` to `.env` and configure your database password
3. Run with Docker Compose:

```bash
docker-compose up --build
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

### Manual Setup

#### Backend

```bash
cd backend
pip install -r requirements.txt

# Configure environment variables
cp ../.env.example .env
# Edit .env with your database credentials

# Run the API server
uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend

```bash
cd frontend
npm install

# Configure API URL
echo "REACT_APP_API_URL=http://localhost:8000" > .env

# Start development server
npm start
```

## Database Setup

1. Create MySQL database:
```sql
CREATE DATABASE merger_roi_db;
```

2. Import your existing schema (firm, staff, sales tables)

3. Update connection details in `.env`

## API Endpoints

- `GET /api/dashboard/summary` - Executive summary metrics
- `GET /api/firms` - List all firms
- `GET /api/roi` - ROI metrics for all firms or specific firm
- `GET /api/capital/productivity` - Capital productivity analysis
- `GET /api/bottlenecks` - Identified bottlenecks
- `GET /api/resources/recommendations` - Resource allocation recommendations
- `POST /api/merger/analyze` - Analyze merger opportunity

Full API documentation available at `/docs` when running the backend.

## Statistical Methods Used

- **Moving Averages**: 3-month, 6-month, 12-month for trend analysis
- **Linear Regression**: For trend prediction
- **Standard Deviation**: For outlier detection
- **Percentile Rankings**: For comparative analysis

No AI/ML algorithms are used - all insights are based on transparent statistical calculations.

## Project Structure

```
├── backend/
│   ├── api.py                 # FastAPI application
│   ├── config.py              # Configuration
│   ├── database.py            # Database connection
│   ├── data_loader.py         # Data loading and validation
│   ├── roi_calculator.py      # ROI calculations
│   ├── capital_analyzer.py    # Capital metrics
│   ├── bottleneck_detector.py # Bottleneck detection
│   ├── resource_optimizer.py  # Resource recommendations
│   ├── merger_analyzer.py     # Merger analysis
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── services/          # API client
│   │   └── App.js             # Main application
│   └── package.json           # Node dependencies
├── requirements.md            # Consolidated requirements
├── design.md                  # System design document
└── docker-compose.yml         # Docker configuration
```

## Hackathon Theme

**Frostbyte Hackathon 2026 - Business & Management Tools**

This project demonstrates:
- SaaS platform for business intelligence
- ERP-like optimization suggestions
- Workflow optimization through data analysis
- Strategic planning support for mergers and resource allocation

## License

MIT License
