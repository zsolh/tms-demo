# Deployment Guide: TMS Demo App on Render

This guide walks through deploying the Flask app as a Render Web Service. Do not use a Static Site for this project, because the app relies on Flask/Jinja template rendering.

## Prerequisites
- GitHub account
- Render account (free at https://render.com)
- Your code pushed to GitHub

## Important: Use a Web Service, Not a Static Site

If Render shows a `Publish Directory` field, you are creating a Static Site. That is the wrong service type for this project and will cause Render to serve template files like `templates/index.html` as plain text instead of rendering them.

For this app, create a new `Web Service`.

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

If your GitHub repository root is the `TMS` folder itself, leave `Root Directory` blank.

If your GitHub repository root is the parent folder that contains `TMS`, set `Root Directory` to:

```text
TMS
```

## Step 4: Configure Deployment Settings

1. **Name:** `tms-demo` (or your preferred name)
2. **Environment:** Python 3
3. **Region:** Select closest to your users
4. **Branch:** main
5. **Root Directory:** blank, or `TMS` if this is a monorepo
6. **Build Command:** `pip install -r requirements.txt`
7. **Start Command:** `gunicorn --bind 0.0.0.0:$PORT app:app`
8. **Plan:** Free tier

There is no `Publish Directory` for this setup, because it is not a Static Site.

## Step 5: Set Environment Variables

1. In the Render dashboard, scroll down to "Environment Variables"
2. Add these variables:
   ```
   FLASK_ENV = production
   DATABASE_URL = sqlite:///tms.db
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
- Render web services use an ephemeral filesystem by default, so SQLite data can reset on redeploy or restart
- For a short-lived demo this is acceptable, because the app auto-seeds sample data on startup
- For production or persistent edits, use PostgreSQL or attach a persistent disk on a paid plan

## Troubleshooting

### Seeing raw template text such as `{% extends "base.html" %}`?

That means the request is hitting a Static Site or directly served file, not the Flask app.

Fix it by:

1. Creating a new `Web Service`
2. Making sure the service type is not `Static Site`
3. Leaving `Publish Directory` unused
4. Opening the Web Service URL, not the old Static Site URL
5. If you use a custom domain, reattach it to the Web Service after removing it from the Static Site

### Build fails?
- Check the build logs in Render dashboard
- Ensure all dependencies are in requirements.txt
- Verify render.yaml syntax

### App won't start?
- Check runtime logs in Render dashboard
- Ensure the start command binds to `0.0.0.0:$PORT`
- Verify app.py runs without errors locally

### Database issues?
- SQLite is acceptable for a temporary demo
- If your data disappears after a restart or redeploy, that is expected on Render without persistent storage
- For persistent data, upgrade to PostgreSQL or attach a persistent disk

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
