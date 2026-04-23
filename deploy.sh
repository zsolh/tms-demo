#!/bin/bash
# Quick deployment script for TMS Demo App to Render

echo "TMS Demo App - Render Deployment Setup"
echo "======================================="
echo ""

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: TMS demo app ready for deployment"
else
    echo "✅ Git repository already initialized"
fi

echo ""
echo "📋 Next steps:"
echo "1. Create a repository on GitHub: https://github.com/new"
echo "2. Run these commands:"
echo "   git branch -M main"
echo "   git remote add origin https://github.com/YOUR_USERNAME/tms-demo.git"
echo "   git push -u origin main"
echo ""
echo "3. Go to Render: https://render.com"
echo "4. Create new Web Service and connect your GitHub repo"
echo "5. Follow the deployment guide in DEPLOY_RENDER.md"
echo ""
echo "✨ For detailed instructions, see DEPLOY_RENDER.md"
