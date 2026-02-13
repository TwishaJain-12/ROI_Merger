# 🚀 Quick Start Guide - Merger ROI Dashboard

## Prerequisites
- Docker Desktop installed
- 5 minutes of your time

## Step 1: Configure Environment (2 minutes)

### Windows:
```cmd
copy .env.example .env
notepad .env
```

### Mac/Linux:
```bash
cp .env.example .env
nano .env
```

**Edit the .env file and set:**
```
DB_PASSWORD=YourSecurePassword123
```

Save and close the file.

## Step 2: Start the Application (1 minute)

### Windows:
```cmd
start.bat
```

### Mac/Linux:
```bash
chmod +x start.sh
./start.sh
```

Or manually:
```bash
docker-compose up --build
```

## Step 3: Access the Dashboard (30 seconds)

Wait 30-60 seconds for services to start, then open:

- **Dashboard**: http://localhost:3000
- **API Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/api/health

## Step 4: Verify Everything Works

### Check Backend Health:
```cmd
curl http://localhost:8000/api/health
```

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Check Data Loaded:
```cmd
curl http://localhost:8000/api/firms
```

Should return 10 firms.

### Check Dashboard:
Open http://localhost:3000 and you should see:
- 4 KPI cards with metrics
- ROI chart with firm rankings
- Bottleneck detection
- Resource recommendations

## Troubleshooting

### "Docker is not running"
- Start Docker Desktop
- Wait for it to fully start
- Try again

### "Database connection failed"
- Check .env file has DB_PASSWORD set
- Restart containers: `docker-compose restart`

### "Port already in use"
- Stop other services using ports 3000, 8000, or 3306
- Or change ports in docker-compose.yml

### "No data showing"
- Wait 60 seconds for database to initialize
- Check logs: `docker-compose logs database`
- Verify init scripts ran: `docker-compose logs database | grep "initialized"`

## Stopping the Application

```cmd
docker-compose down
```

## Viewing Logs

```cmd
docker-compose logs -f
```

Or for specific service:
```cmd
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f database
```

## Resetting Everything

```cmd
docker-compose down -v
docker-compose up --build
```

This will delete all data and start fresh.

## What's Included

### Sample Data:
- 10 firms across different industries
- 40+ staff members with salaries
- 50+ sales transactions over 12 months

### Features Working:
- ✅ Executive dashboard with KPIs
- ✅ ROI calculations for all firms
- ✅ Capital productivity analysis
- ✅ Bottleneck detection
- ✅ Resource allocation recommendations
- ✅ Merger analysis API
- ✅ Interactive API documentation

## Next Steps

1. **Explore the API**: http://localhost:8000/docs
2. **Test merger analysis**: 
   ```
   POST http://localhost:8000/api/merger/analyze?firm_a_id=1&firm_b_id=2
   ```
3. **Customize the data**: Edit `database/seed_data.sql`
4. **Add your own data**: Use the API or connect to your MySQL database

## Demo Script

For presentations:

1. Show dashboard with real-time KPIs
2. Highlight ROI rankings (visual chart)
3. Point out bottleneck detection
4. Show resource recommendations
5. Demo merger analysis in API docs
6. Emphasize: "No AI/ML - Pure statistical analysis"

## Support

If you encounter issues:
1. Check logs: `docker-compose logs`
2. Verify .env file is configured
3. Ensure Docker has enough resources (4GB RAM minimum)
4. Check firewall isn't blocking ports

---

**Total Setup Time: 3-5 minutes**
**You're ready to demo! 🎉**
