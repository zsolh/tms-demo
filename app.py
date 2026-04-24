from flask import Flask, render_template, jsonify, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_
import random
import time
import os

app = Flask(__name__)

# Database configuration
database_url = os.environ.get('DATABASE_URL', 'sqlite:///tms.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

ENTRY_POINT_REDIRECTS = {
    '/templates/index': 'home_html',
    '/templates/index.html': 'home_html',
    '/templates/home': 'home_html',
    '/templates/home.html': 'home_html',
    '/static/index': 'home_html',
    '/static/index.html': 'home_html',
    '/static/home': 'home_html',
    '/static/home.html': 'home_html',
}

class Shipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    origin = db.Column(db.String(100), nullable=False)
    destination = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Pending')
    driver = db.Column(db.String(100), nullable=False)

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    vehicle = db.Column(db.String(100), nullable=False)
    driver = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(50), default='Active')


SHIPMENT_STATUS_OPTIONS = ['Pending', 'In Transit', 'Delivered', 'Delayed']
VEHICLE_STATUS_OPTIONS = ['Active', 'Maintenance', 'Inactive']
TEST_RECORDS_PER_TABLE = 50

SAMPLE_CITIES = [
    'New York', 'Los Angeles', 'Chicago', 'Miami', 'Seattle', 'Denver',
    'Dallas', 'Atlanta', 'Phoenix', 'Portland', 'Boston', 'Houston',
    'Detroit', 'Nashville', 'San Diego', 'Minneapolis', 'Charlotte',
    'Kansas City', 'Cleveland', 'Salt Lake City'
]
SAMPLE_DRIVERS = [
    'John Doe', 'Jane Smith', 'Bob Johnson', 'Alex Carter', 'Maria Lopez',
    'Chris Nguyen', 'Priya Patel', 'Sam Wilson', 'Nina Brown', 'Owen Martin',
    'Lena Fischer', 'David Clark', 'Maya Green', 'Leo Turner', 'Sara Adams'
]
SAMPLE_VEHICLES = ['Truck', 'Van', 'Reefer', 'Box Truck', 'Flatbed', 'Tanker']


def seed_test_data():
    shipment_count = Shipment.query.count()
    vehicle_count = Vehicle.query.count()

    if shipment_count < TEST_RECORDS_PER_TABLE:
        shipments = []
        for index in range(shipment_count + 1, TEST_RECORDS_PER_TABLE + 1):
            shipments.append(Shipment(
                origin=SAMPLE_CITIES[index % len(SAMPLE_CITIES)],
                destination=SAMPLE_CITIES[(index * 4 + 3) % len(SAMPLE_CITIES)],
                status=SHIPMENT_STATUS_OPTIONS[index % len(SHIPMENT_STATUS_OPTIONS)],
                driver=SAMPLE_DRIVERS[index % len(SAMPLE_DRIVERS)],
            ))
        db.session.add_all(shipments)

    if vehicle_count < TEST_RECORDS_PER_TABLE:
        vehicles = []
        for index in range(vehicle_count + 1, TEST_RECORDS_PER_TABLE + 1):
            vehicles.append(Vehicle(
                vehicle=f'{SAMPLE_VEHICLES[index % len(SAMPLE_VEHICLES)]} {index:03d}',
                driver=SAMPLE_DRIVERS[(index * 2) % len(SAMPLE_DRIVERS)],
                status=VEHICLE_STATUS_OPTIONS[index % len(VEHICLE_STATUS_OPTIONS)],
            ))
        db.session.add_all(vehicles)

    if shipment_count < TEST_RECORDS_PER_TABLE or vehicle_count < TEST_RECORDS_PER_TABLE:
        db.session.commit()


with app.app_context():
    db.create_all()
    seed_test_data()

# Mock data - removed, now using DB

@app.before_request
def redirect_mistaken_entry_points():
    target_endpoint = ENTRY_POINT_REDIRECTS.get(request.path)
    if target_endpoint is None:
        return None
    target_url = url_for(target_endpoint)
    if request.query_string:
        target_url = f"{target_url}?{request.query_string.decode('utf-8', errors='ignore')}"
    return redirect(target_url, code=302)

@app.route('/')
def home():
    stats = {
        'shipments': Shipment.query.count(),
        'fleet': Vehicle.query.count(),
        'in_transit': Shipment.query.filter_by(status='In Transit').count(),
        'active': Vehicle.query.filter_by(status='Active').count(),
    }
    return render_template('home.html', stats=stats)

@app.route('/home.html')
def home_html():
    return home()

@app.route('/home')
def home_alias():
    return redirect(url_for('home_html'))

@app.route('/index')
@app.route('/index.html')
def index():
    return redirect(url_for('home_html'))

@app.route('/templates/index')
@app.route('/templates/index.html')
def templates_index():
    return redirect(url_for('home_html'))

@app.route('/report')
def report():
    # Mock data for report
    total_shipments = Shipment.query.count()
    on_time_deliveries = Shipment.query.filter_by(status='Delivered').count()
    delayed = Shipment.query.filter_by(status='Delayed').count()
    total_vehicles = Vehicle.query.count()
    active_vehicles = Vehicle.query.filter_by(status='Active').count()
    data = {
        'total_shipments': total_shipments,
        'on_time_deliveries': on_time_deliveries,
        'delayed': delayed,
        'revenue': 50000,
        'total_vehicles': total_vehicles,
        'active_vehicles': active_vehicles
    }
    return render_template('report.html', data=data)

@app.route('/performance')
def performance():
    return render_template('performance.html')

@app.route('/api/performance_data')
def performance_data():
    # Mock real-time data
    teams = ['Team A', 'Team B', 'Team C', 'Team D']
    data = {}
    for team in teams:
        data[team] = {
            'deliveries': random.randint(10, 50),
            'efficiency': random.uniform(80, 100),
            'issues': random.randint(0, 5),
            'fuel_efficiency': random.uniform(5, 15),  # mpg
            'distance': random.randint(100, 500)  # miles
        }
    return jsonify(data)

@app.route('/shipments')
def shipments_page():
    query = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    shipments_query = Shipment.query
    if query:
        like = f'%{query}%'
        shipments_query = shipments_query.filter(
            or_(Shipment.origin.ilike(like), Shipment.destination.ilike(like), Shipment.driver.ilike(like))
        )
    if status:
        shipments_query = shipments_query.filter_by(status=status)
    shipments = shipments_query.order_by(Shipment.id.desc()).all()
    return render_template('shipments.html', shipments=shipments, search=query, status=status, statuses=SHIPMENT_STATUS_OPTIONS)

@app.route('/fleet')
def fleet_page():
    query = request.args.get('search', '').strip()
    status = request.args.get('status', '').strip()
    fleet_query = Vehicle.query
    if query:
        like = f'%{query}%'
        fleet_query = fleet_query.filter(
            or_(Vehicle.vehicle.ilike(like), Vehicle.driver.ilike(like))
        )
    if status:
        fleet_query = fleet_query.filter_by(status=status)
    fleet = fleet_query.order_by(Vehicle.id.desc()).all()
    return render_template('fleet.html', fleet=fleet, search=query, status=status, statuses=VEHICLE_STATUS_OPTIONS)

@app.route('/add_shipment', methods=['GET', 'POST'])
def add_shipment():
    if request.method == 'POST':
        new_shipment = Shipment(
            origin=request.form['origin'],
            destination=request.form['destination'],
            driver=request.form['driver']
        )
        db.session.add(new_shipment)
        db.session.commit()
        return redirect('/shipments')
    return render_template('add_shipment.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/admin/shipments')
def admin_shipments():
    shipments = Shipment.query.order_by(Shipment.id.desc()).all()
    return render_template('admin_shipments.html', shipments=shipments)

@app.route('/admin/fleet')
def admin_fleet():
    fleet = Vehicle.query.order_by(Vehicle.id.desc()).all()
    return render_template('admin_fleet.html', fleet=fleet)

@app.route('/admin/shipment/<int:id>', methods=['GET', 'POST'])
def edit_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    if request.method == 'POST':
        shipment.origin = request.form['origin']
        shipment.destination = request.form['destination']
        shipment.status = request.form['status']
        shipment.driver = request.form['driver']
        db.session.commit()
        return redirect('/admin/shipments')
    return render_template('edit_shipment.html', shipment=shipment)

@app.route('/admin/shipment/delete/<int:id>')
def delete_shipment(id):
    shipment = Shipment.query.get_or_404(id)
    db.session.delete(shipment)
    db.session.commit()
    return redirect('/admin/shipments')

@app.route('/admin/vehicle/<int:id>', methods=['GET', 'POST'])
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    if request.method == 'POST':
        vehicle.vehicle = request.form['vehicle']
        vehicle.driver = request.form['driver']
        vehicle.status = request.form['status']
        db.session.commit()
        return redirect('/admin/fleet')
    return render_template('edit_vehicle.html', vehicle=vehicle)

@app.route('/admin/vehicle/delete/<int:id>')
def delete_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)
    db.session.delete(vehicle)
    db.session.commit()
    return redirect('/admin/fleet')

if __name__ == '__main__':
    app.run(debug=True)
