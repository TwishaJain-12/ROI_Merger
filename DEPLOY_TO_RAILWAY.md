# 🚂 Quick Railway Deployment - 5 Steps

## Step 1: Push to GitHub (5 minutes)

```bash
# If you don't have git initialized
git init
git add .
git commit -m "Ready for Railway deployment"

# Create a new repo on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/merger-roi-dashboard.git
git branch -M main
git push -u origin main
```

---

## Step 2: Sign Up for Railway (2 minutes)

1. Go to https://railway.app
2. Click "Login" → "Login with GitHub"
3. Authorize Railway

---

## Step 3: Create New Project (3 minutes)

1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your `merger-roi-dashboard` repository
4. Railway detects docker-compose.yml automatically!

---

## Step 4: Configure Environment Variables (5 minutes)

### For Database Service:
Railway auto-creates these - no action needed!

### For Backend Service:
Click on `backend` → Variables → Add these:

```
DB_HOST=database.railway.internal
DB_PORT=3306
DB_USER=root
DB_PASSWORD=${{database.MYSQL_ROOT_PASSWORD}}
DB_NAME=merger_roi_db
```

Then:
- Go to Settings → Generate Domain
- Copy the backend URL (e.g., `backend-abc123.up.railway.app`)

### For Frontend Service:
Click on `frontend` → Variables → Add:

```
REACT_APP_API_URL=https://YOUR_BACKEND_URL_HERE
```

Then:
- Go to Settings → Generate Domain
- Copy the frontend URL

---

## Step 5: Deploy & Test (5 minutes)

Railway automatically deploys. Wait 3-5 minutes, then test:

### Test Backend:
```
https://your-backend-url.up.railway.app/api/health
```

### Test Frontend:
```
https://your-frontend-url.up.railway.app
```

---

## 🎉 Done!

Your app is live on Railway!

**Total Time: ~20 minutes**

---

## 🔄 Future Updates

Just push to GitHub:
```bash
git add .
git commit -m "Update feature"
git push
```

Railway automatically redeploys!

---

## 💰 Cost

- **Free**: $5 credit/month (good for testing)
- **Hobby**: $5/month (good for small projects)
- **Pro**: $20/month (production ready)

---

## ⚠️ Important Notes

1. **Database Persistence**: Railway databases are persistent
2. **Environment Variables**: Use Railway's variable references like `${{database.MYSQL_ROOT_PASSWORD}}`
3. **Domains**: Railway provides free `.up.railway.app` domains
4. **Logs**: Check logs in Railway dashboard if something fails

---

## 🆘 Need Help?

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Check `RAILWAY_DEPLOYMENT.md` for detailed guide
