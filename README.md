# TMS Demo App

A minimalistic Transportation Management Software demo application with database persistence and PWA capabilities.

## Features

- Browser-based access
- Smartphone responsive design
- Management report with key metrics (shipments, deliveries, revenue, vehicles)
- Real-time diagrams of team performance (deliveries, efficiency, issues, fuel efficiency, distance)
- Shipment management: View and add shipments
- Fleet management: View vehicles and assignments
- Admin Console: Full CRUD operations on shipments and fleet data
- SQLite database for data persistence
- Progressive Web App (PWA) features for mobile installation

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Run the app:
   ```
   python3 app.py
   ```

3. Open http://127.0.0.1:5000 in your browser.

## Database

The app uses SQLite (`tms.db`) for data storage. Initial data is automatically populated on first run.

## Mobile App Installation (PWA)

The app is now a Progressive Web App that can be installed on smartphones:

### Android:
1. Open the app in Chrome browser on your Android device
2. Tap the menu (three dots) > "Add to Home screen"
3. Follow the prompts to install

### iOS:
1. Open the app in Safari on your iPhone/iPad
2. Tap the share button > "Add to Home Screen"
3. Follow the prompts to install

Once installed, the app will run like a native app with offline capabilities.

## Public Deployment

To deploy this app publicly and make it accessible to multiple users:

**See [DEPLOY_RENDER.md](DEPLOY_RENDER.md) for step-by-step deployment to Render (free tier available).**

Quick summary:
1. Push code to GitHub
2. Connect Render to your repository
3. Deploy with one click
4. Get a public URL immediately

No credit card required for free tier!

## Usage

- Home: Overview
- Management Report: View shipment and fleet statistics
- Team Performance: Real-time charts updating every 5 seconds
- Shipments: List of shipments, add new ones
- Fleet: List of vehicles and their status
- Admin Console: Full CRUD operations on shipments and fleet data