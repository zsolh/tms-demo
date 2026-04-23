from flask import Flask, render_template, jsonify, request, redirect
from flask_sqlalchemy import SQLAlchemy
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

with app.app_context():
    db.create_all()
    if not Shipment.query.first():
        initial_shipments = [
            Shipment(origin='New York', destination='Los Angeles', status='In Transit', driver='John Doe'),
            Shipment(origin='Chicago', destination='Miami', status='Delivered', driver='Jane Smith'),
            Shipment(origin='Seattle', destination='Denver', status='Pending', driver='Bob Johnson'),
        ]
        db.session.add_all(initial_shipments)
        db.session.commit()
    if not Vehicle.query.first():
        initial_fleet = [
            Vehicle(vehicle='Truck A', driver='John Doe', status='Active'),
            Vehicle(vehicle='Truck B', driver='Jane Smith', status='Maintenance'),
            Vehicle(vehicle='Van C', driver='Bob Johnson', status='Active'),
        ]
        db.session.add_all(initial_fleet)
        db.session.commit()

# Mock data - removed, now using DB

@app.route('/')
def home():
    return render_template('home.html')

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
    shipments = Shipment.query.all()
    return render_template('shipments.html', shipments=shipments)

@app.route('/fleet')
def fleet_page():
    fleet = Vehicle.query.all()
    return render_template('fleet.html', fleet=fleet)

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
    shipments = Shipment.query.all()
    return render_template('admin_shipments.html', shipments=shipments)

@app.route('/admin/fleet')
def admin_fleet():
    fleet = Vehicle.query.all()
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