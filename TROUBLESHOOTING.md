# 🔧 Troubleshooting Guide

## Issue: "localhost refused to connect"

### What Happened:
You had TWO docker-compose files:
- `compose.yaml` (old Postgres/Grafana setup)
- `docker-compose.yml` (new MySQL setup for Merger ROI Dashboard)

Docker was using the OLD file, which didn't have the correct services.

### What I Fixed:
✅ Renamed `compose.yaml` to `compose.yaml.old`
✅ Now using `docker-compose.yml` with correct MySQL configuration
✅ Started the containers with `docker-compose up --build`

---

## Current Status:

Docker is now:
1. ⏳ Downloading MySQL 8.0 image (first time only, ~250MB)
2. ⏳ Building backend container
3. ⏳ Building frontend container
4. ⏳ Initializing database with schema and data

**This takes 3-5 minutes on first run.**

---

## How to Check Progress:

### Option 1: View logs in real-time
```cmd
docker-compose logs -f
```

### Option 2: Check container status
```cmd
docker-compose ps
```

You should see:
```
NAME                STATUS              PORTS
database            Up (healthy)        0.0.0.0:3306->3306/tcp
backend             Up                  0.0.0.0:8000->8000/tcp
frontend            Up                  0.0.0.0:3000->3000/tcp
```

### Option 3: Check specific service
```cmd
docker-compose logs database
docker-compose logs backend
docker-compose logs frontend
```

---

## When Services Are Ready:

### 1. Database is ready when you see:
```
database  | MySQL init process done. Ready for start up.
database  | Database initialized successfully!
```

### 2. Backend is ready when you see:
```
backend   | INFO:     Uvicorn running on http://0.0.0.0:8000
backend   | INFO:     Application startup complete.
```

### 3. Frontend is ready when you see:
```
frontend  | webpack compiled successfully
frontend  | Compiled successfully!
```

---

## Testing After Startup:

### Test 1: Check containers are running
```cmd
docker-compose ps
```

### Test 2: Check backend health
```cmd
curl http://localhost:8000/api/health
```

Or open in browser: http://localhost:8000/api/health

Expected response:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test 3: Check API docs
Open: http://localhost:8000/docs

### Test 4: Check dashboard
Open: http://localhost:3000

---

## Common Issues & Solutions:

### Issue: "Port 3306 already in use"
**Cause:** Another MySQL instance is running

**Solution:**
```cmd
# Stop other MySQL service
net stop MySQL80

# Or change port in docker-compose.yml
ports:
  - "3307:3306"  # Use 3307 instead
```

### Issue: "Port 8000 already in use"
**Cause:** Another application using port 8000

**Solution:**
```cmd
# Find what's using the port
netstat -ano | findstr :8000

# Kill the process (replace PID with actual number)
taskkill /PID <PID> /F

# Or change port in docker-compose.yml
```

### Issue: "Port 3000 already in use"
**Cause:** Another React app or service running

**Solution:**
```cmd
# Find and kill the process
netstat -ano | findstr :3000
taskkill /PID <PID> /F
```

### Issue: Database initialization fails
**Symptoms:** Backend can't connect to database

**Solution:**
```cmd
# Check database logs
docker-compose logs database

# If you see errors, reset everything:
docker-compose down -v
docker-compose up --build
```

### Issue: Backend shows "ModuleNotFoundError"
**Cause:** Python dependencies not installed

**Solution:**
```cmd
# Rebuild backend container
docker-compose build backend
docker-compose up backend
```

### Issue: Frontend shows blank page
**Cause:** npm packages not installed or still installing

**Solution:**
```cmd
# Wait 2-3 minutes for npm install to complete
# Check logs:
docker-compose logs frontend

# If stuck, rebuild:
docker-compose build frontend
docker-compose up frontend
```

### Issue: "Database connection failed"
**Cause:** Database not ready or wrong password

**Solution:**
```cmd
# Check .env file has DB_PASSWORD set
type .env

# Check database is healthy
docker-compose ps

# Restart services
docker-compose restart
```

---

## Complete Reset (Nuclear Option):

If nothing works, do a complete reset:

```cmd
# Stop and remove everything
docker-compose down -v

# Remove old images
docker-compose rm -f

# Rebuild from scratch
docker-compose build --no-cache

# Start fresh
docker-compose up
```

---

## Useful Commands:

### Start services
```cmd
docker-compose up -d          # Detached mode (background)
docker-compose up --build     # Rebuild and start
```

### Stop services
```cmd
docker-compose stop           # Stop without removing
docker-compose down           # Stop and remove containers
docker-compose down -v        # Stop and remove volumes (data)
```

### View logs
```cmd
docker-compose logs -f                    # All services
docker-compose logs -f backend            # Backend only
docker-compose logs -f --tail=100 backend # Last 100 lines
```

### Restart services
```cmd
docker-compose restart                # All services
docker-compose restart backend        # Backend only
```

### Execute commands in container
```cmd
# Access database
docker-compose exec database mysql -u root -p merger_roi_db

# Access backend shell
docker-compose exec backend bash

# Check backend Python version
docker-compose exec backend python --version
```

### Check resource usage
```cmd
docker stats
```

---

## Expected Timeline:

### First Run (Cold Start):
- Download images: 2-3 minutes
- Build containers: 1-2 minutes
- Initialize database: 30 seconds
- Start services: 30 seconds
**Total: 4-6 minutes**

### Subsequent Runs:
- Start containers: 10 seconds
- Initialize services: 20 seconds
**Total: 30-60 seconds**

---

## How to Know Everything is Working:

### ✅ All checks pass:

1. **Containers running:**
   ```cmd
   docker-compose ps
   ```
   All show "Up" status

2. **Health check passes:**
   ```cmd
   curl http://localhost:8000/api/health
   ```
   Returns: `{"status":"healthy","database":"connected"}`

3. **API docs accessible:**
   http://localhost:8000/docs shows Swagger UI

4. **Dashboard loads:**
   http://localhost:3000 shows KPI cards and charts

5. **Data exists:**
   ```cmd
   curl http://localhost:8000/api/firms
   ```
   Returns 10 firms

---

## Still Having Issues?

### Check Docker Desktop:
1. Open Docker Desktop
2. Go to Containers tab
3. Look for `roi_merger` containers
4. Click on each to see logs
5. Check for error messages

### Check System Resources:
- Docker needs at least 4GB RAM
- Check Docker Desktop → Settings → Resources
- Increase if needed

### Check Firewall:
- Windows Firewall might block Docker
- Allow Docker Desktop through firewall
- Allow ports 3000, 8000, 3306

### Get Detailed Logs:
```cmd
docker-compose logs --no-color > logs.txt
```
Then review `logs.txt` for errors

---

## Success Indicators:

When everything is working, you'll see:

### In Terminal:
```
database  | ready for connections
backend   | Uvicorn running on http://0.0.0.0:8000
frontend  | webpack compiled successfully
```

### In Browser:
- http://localhost:8000/api/health → Green "healthy" status
- http://localhost:8000/docs → Interactive API documentation
- http://localhost:3000 → Dashboard with data

---

## Next Steps After Success:

1. ✅ Verify all endpoints work
2. ✅ Test merger analysis
3. ✅ Explore the dashboard
4. ✅ Review sample data
5. ✅ Prepare demo script

**You're almost there! Just wait for the containers to finish building.** 🚀
