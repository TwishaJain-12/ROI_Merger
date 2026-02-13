# 🚂 Merger ROI Calculator - Full Stack Railway Deployment

## Project Overview

A complete full-stack web application for analyzing merger ROI with:
- **Frontend**: React dashboard with beautiful UI
- **Backend**: FastAPI REST API
- **Database**: PostgreSQL (Railway managed)
- **Deployment**: Railway (no Docker needed!)

## Features

✅ Interactive merger analysis
✅ Real-time ROI calculations
✅ Beautiful dashboard with charts
✅ Company comparison
✅ Historical analysis tracking
✅ YES/NO recommendations based on research

## Tech Stack

- **Frontend**: React 18 + TailwindCSS + Chart.js
- **Backend**: Python FastAPI
- **Database**: PostgreSQL (Railway)
- **Deployment**: Railway

## Project Structure

```
railway-fullstack/
├── backend/
│   ├── main.py              # FastAPI app
│   ├── calculator.py        # ROI calculation logic
│   ├── database.py          # Database connection
│   ├── models.py            # Data models
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── services/        # API service
│   │   ├── App.js          # Main app
│   │   └── index.js        # Entry point
│   └── package.json        # Node dependencies
├── database/
│   └── schema.sql          # Database schema
└── railway.json            # Railway config
```

## Quick Deploy to Railway

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin YOUR_GITHUB_REPO
git push -u origin main
```

### Step 2: Deploy on Railway
1. Go to https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Choose this repository
5. Railway auto-detects and deploys!

### Step 3: Add Database
1. Click "New" → "Database" → "PostgreSQL"
2. Railway automatically connects it
3. Database URL is auto-configured

**Live in 5 minutes!** 🎉

## Local Development

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Runs on http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm start
```
Runs on http://localhost:3000

## Environment Variables

Railway auto-configures these:
- `DATABASE_URL` - PostgreSQL connection
- `PORT` - Application port

## Features

### 1. Company Management
- View all companies
- Add new companies
- Edit company details

### 2. Merger Analysis
- Select two companies
- Adjust synergy rate and premium
- Get instant ROI calculation
- See YES/NO recommendation

### 3. Dashboard
- View all analyses
- Compare scenarios
- Track historical data
- Export results

### 4. Visualizations
- ROI comparison charts
- NPV analysis
- Payback period graphs
- Synergy breakdown

## API Endpoints

- `GET /api/companies` - List all companies
- `POST /api/companies` - Add new company
- `POST /api/analyze` - Analyze merger
- `GET /api/history` - Get analysis history

## Academic Foundation

Based on research from:
- Damodaran (NYU) - Synergy valuation
- Bruner - M&A decision criteria
- Koller (McKinsey) - DCF methodology

## Cost

Railway offers:
- **Free**: $5 credit/month
- **Hobby**: $5/month
- **Pro**: $20/month

Perfect for this project!
