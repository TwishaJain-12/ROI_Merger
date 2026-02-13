# Quick Setup Guide

## For Hackathon Demo

### Option 1: Docker (Recommended)

1. **Install Docker Desktop** (if not already installed)
   - Download from https://www.docker.com/products/docker-desktop

2. **Configure Database**
   ```bash
   copy .env.example .env
   ```
   Edit `.env` and set your database password

3. **Start Everything**
   ```bash
   docker-compose up --build
   ```

4. **Access the Application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup (Windows)

#### Backend Setup

1. **Install Python 3.9+**
   - Download from https://www.python.org/downloads/

2. **Setup Backend**
   ```cmd
   cd backend
   pip install -r requirements.txt
   ```

3. **Configure Database**
   - Create `.env` file in backend folder
   - Add your MySQL credentials:
   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=your_password
   DB_NAME=merger_roi_db
   ```

4. **Run Backend**
   ```cmd
   uvicorn backend.api:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Install Node.js 18+**
   - Download from https://nodejs.org/

2. **Setup Frontend**
   ```cmd
   cd frontend
   npm install
   ```

3. **Configure API URL**
   Create `.env` file in frontend folder:
   ```
   REACT_APP_API_URL=http://localhost:8000
   ```

4. **Run Frontend**
   ```cmd
   npm start
   ```

## Database Setup

Your existing MySQL database should have these tables:
- `firm` (firm_id, firm_name, ...)
- `staff` (staff_id, firm_id, salary, ...)
- `sales` (sale_id, firm_id, total_amount, sale_date, ...)

Update the database credentials in `.env` to connect to your existing database.

## Testing the API

Once the backend is running, visit:
- http://localhost:8000/docs - Interactive API documentation
- http://localhost:8000/api/health - Health check

## Troubleshooting

### Backend won't start
- Check if MySQL is running
- Verify database credentials in `.env`
- Check if port 8000 is available

### Frontend won't start
- Check if Node.js is installed: `node --version`
- Delete `node_modules` and run `npm install` again
- Check if port 3000 is available

### Database connection errors
- Verify MySQL is running
- Check database name exists
- Verify user has permissions
- Test connection: `mysql -u root -p`

## Demo Data

If you need sample data, you can use the existing data from your uploaded files:
- Firm data
- Staff data  
- Sales data

The system will automatically calculate ROI, detect bottlenecks, and provide recommendations based on this data.

## Hackathon Presentation Tips

1. **Start with the Dashboard** - Show the KPI cards with real metrics
2. **Demonstrate ROI Analysis** - Show the bar chart with firm rankings
3. **Highlight Bottlenecks** - Show detected issues and recommendations
4. **Show Merger Analysis** - Use the API to analyze a merger between two firms
5. **Emphasize No AI/ML** - All calculations use transparent statistical methods

## Key Features to Demo

✅ Real-time dashboard with KPIs
✅ ROI calculations for all firms
✅ Capital productivity analysis
✅ Bottleneck detection using statistical methods
✅ Resource allocation recommendations
✅ Merger equity analysis
✅ All based on historical data (no AI/ML)

Good luck with your hackathon! 🚀
