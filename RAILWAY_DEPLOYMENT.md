# 🚂 Railway Deployment Guide - Complete Setup

## Why Railway is Perfect for Your Project

✅ Supports Docker (your existing setup works!)
✅ Built-in MySQL database
✅ Free tier available ($5 credit/month)
✅ Automatic HTTPS
✅ Easy environment variables
✅ GitHub integration
✅ No code changes needed!

---

## 📋 Prerequisites

1. GitHub account
2. Railway account (sign up at https://railway.app)
3. Your code pushed to GitHub

---

## 🚀 Deployment Steps

### Step 1: Push Your Code to GitHub

If you haven't already:

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Merger ROI Dashboard"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

---

### Step 2: Sign Up for Railway

1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign in with GitHub
4. Authorize Railway to access your repositories

---

### Step 3: Create a New Project

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Railway will detect your docker-compose.yml automatically!

---

### Step 4: Configure Services

Railway will create 3 services from your docker-compose.yml:
- `database` (MySQL)
- `backend` (FastAPI)
- `frontend` (React)

#### 4.1 Configure Database Service

1. Click on the `database` service
2. Go to "Variables" tab
3. Railway auto-generates these:
   - `MYSQL_ROOT_PASSWORD`
   - `MYSQL_DATABASE`
   - `MYSQL_USER`
   - `MYSQL_PASSWORD`

4. Note the connection details (Railway provides them automatically)

#### 4.2 Configure Backend Service

1. Click on the `backend` service
2. Go to "Variables" tab
3. Add these environment variables:
   ```
   DB_HOST=database.railway.internal
   DB_PORT=3306
   DB_USER=root
   DB_PASSWORD=${{database.MYSQL_ROOT_PASSWORD}}
   DB_NAME=merger_roi_db
   PORT=8000
   ```

4. Go to "Settings" tab
5. Under "Networking", click "Generate Domain"
6. Copy the domain (e.g., `your-backend.up.railway.app`)

#### 4.3 Configure Frontend Service

1. Click on the `frontend` service
2. Go to "Variables" tab
3. Add:
   ```
   REACT_APP_API_URL=https://your-backend.up.railway.app
   PORT=3000
   ```

4. Go to "Settings" tab
5. Under "Networking", click "Generate Domain"
6. Copy the domain (e.g., `your-frontend.up.railway.app`)

---

### Step 5: Deploy!

Railway will automatically:
1. Build your Docker containers
2. Start all services
3. Connect them together
4. Provide public URLs

**Wait 3-5 minutes for deployment to complete.**

---

## ✅ Verify Deployment

### Test Backend:
```
https://your-backend.up.railway.app/api/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

### Test API Docs:
```
https://your-backend.up.railway.app/docs
```

### Test Frontend:
```
https://your-frontend.up.railway.app
```

---

## 🔧 Configuration Files Needed

I'll create the necessary Railway configuration files for you.

---

## 💰 Pricing

**Free Tier:**
- $5 credit per month
- Enough for development/testing
- Sleeps after inactivity

**Hobby Plan ($5/month):**
- $5 credit + $5 usage
- No sleeping
- Better for production

**Pro Plan ($20/month):**
- $20 credit + usage
- Priority support
- Better performance

---

## 🐛 Troubleshooting

### Build Fails?
- Check Railway logs in the deployment tab
- Ensure docker-compose.yml is valid
- Check Dockerfile syntax

### Database Connection Fails?
- Verify DB_HOST is set to `database.railway.internal`
- Check DB_PASSWORD matches database service
- Ensure database service is running

### Frontend Can't Connect to Backend?
- Verify REACT_APP_API_URL is set correctly
- Check backend domain is public
- Ensure CORS is configured in backend

---

## 🔄 Automatic Deployments

Railway automatically redeploys when you push to GitHub:

```bash
# Make changes
git add .
git commit -m "Update feature"
git push

# Railway automatically deploys!
```

---

## 📊 Monitoring

Railway provides:
- Real-time logs
- Resource usage metrics
- Deployment history
- Service health status

Access via Railway dashboard → Your Project → Service → Logs

---

## 🎯 Next Steps After Deployment

1. ✅ Test all API endpoints
2. ✅ Verify database has sample data
3. ✅ Check frontend loads correctly
4. ✅ Test merger analysis feature
5. ✅ Share your live URL!

---

## 🔗 Useful Links

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

---

## 💡 Pro Tips

1. **Use Railway CLI** for faster deployments:
   ```bash
   npm i -g @railway/cli
   railway login
   railway up
   ```

2. **Set up custom domain** (optional):
   - Go to Service → Settings → Domains
   - Add your custom domain
   - Update DNS records

3. **Enable metrics** to monitor performance

4. **Set up alerts** for service downtime

---

## 🎉 You're Done!

Your Merger ROI Dashboard is now live on Railway!

Share your URLs:
- Frontend: `https://your-frontend.up.railway.app`
- Backend API: `https://your-backend.up.railway.app/docs`
