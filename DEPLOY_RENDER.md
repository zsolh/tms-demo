# Deployment Guide: TMS Demo App on Render

This guide will walk you through deploying your TMS demo app to Render in 5 simple steps.

## Prerequisites
- GitHub account
- Render account (free at https://render.com)
- Your code pushed to GitHub

## Step 1: Initialize Git and Push to GitHub

1. **Initialize local git repository:**
   ```bash
   cd /Users/zsoltholman/VisualStudioProjects/TMS
   git init
   git add .
   git commit -m "Initial commit: TMS demo app ready for deployment"
   ```

2. **Create a new repository on GitHub:**
   - Go to https://github.com/new
   - Name: `tms-demo`
   - Description: `Transportation Management Software Demo`
   - Make it Public (for easier sharing)
   - Click "Create repository"

3. **Push to GitHub:**
   ```bash
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/tms-demo.git
   git push -u origin main
   ```
   (Replace YOUR_USERNAME with your actual GitHub username)

## Step 2: Create Render Account

1. Go to https://render.com
2. Click "Sign up with GitHub" for seamless integration
3. Authorize GitHub access

## Step 3: Connect Your Repository to Render

1. In Render dashboard, click "New +" → "Web Service"
2. Click "Connect a repository"
3. Select your GitHub account
4. Find and select `tms-demo` repository
5. Click "Connect"

## Step 4: Configure Deployment Settings

1. **Name:** `tms-demo` (or your preferred name)
2. **Environment:** Python 3
3. **Region:** Select closest to your users
4. **Branch:** main
5. **Build Command:** `pip install -r requirements.txt`
6. **Start Command:** `gunicorn app:app`
7. **Plan:** Free tier

## Step 5: Set Environment Variables (Optional)

1. In the Render dashboard, scroll down to "Environment Variables"
2. Add these variables:
   ```
   FLASK_ENV = production
   ```

3. Click "Create Web Service"

## Deployment Complete!

Render will automatically:
- Build your application
- Install dependencies
- Start the app
- Provide you with a public URL (e.g., https://tms-demo.onrender.com)

Your app is now live!

## Access Your App

- **Public URL:** Check the Render dashboard for your assigned URL
- **Share with users:** Send them the public URL
- **Automatic updates:** Every push to `main` branch triggers automatic deployment

## Monitoring

In the Render dashboard you can:
- View live logs
- Check CPU/Memory usage
- View deployment history
- Manage environment variables

## Database Notes

- The app uses SQLite locally
- For production with multiple users, consider upgrading to PostgreSQL
- Render provides free PostgreSQL with paid plans
- Current setup works fine for evaluation with free tier

## Troubleshooting

### Build fails?
- Check the build logs in Render dashboard
- Ensure all dependencies are in requirements.txt
- Verify render.yaml syntax

### App won't start?
- Check runtime logs in Render dashboard
- Ensure PORT environment variable is being used (Render sets this automatically)
- Verify app.py runs without errors locally

### Database issues?
- SQLite works on free tier for testing
- For production, upgrade to PostgreSQL

## Next Steps

1. **Custom Domain:** Upgrade to paid plan to add custom domain
2. **Database:** Consider PostgreSQL for production
3. **Monitoring:** Set up notifications for deployments
4. **Optimization:** Monitor free hours usage on free tier

## Cost Summary

- **Free Tier:** $0/month, 750 hours/month (enough for continuous operation)
- **Pro Plan:** $7/month, unlimited hours
- **Upgrade when:** You need more than 750 hours or custom domain

---

**Your app is now publicly accessible!** 🎉
