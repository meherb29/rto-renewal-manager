from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Vehicle, Customer

vehicles = Blueprint('vehicles', __name__)

VEHICLE_CATEGORIES = [
    'Force Bus', 'Force Ambulance', 'Force Cruiser',
    'Tractor', 'Two-Wheeler', 'Car/SUV', 'Other'
]

PASSING_TYPES = ['MH', 'Tourist', 'Company']

@vehicles.route('/vehicles/new')
def new_vehicle():
    customer_id = request.args.get('customer_id', type=int)
    customer = Customer.query.get_or_404(customer_id)
    return render_template('vehicles/form.html',
                           customer=customer,
                           categories=VEHICLE_CATEGORIES,
                           passing_types=PASSING_TYPES)

@vehicles.route('/vehicles/new', methods=['POST'])
def create_vehicle():
    customer_id = request.form.get('customer_id', type=int)
    customer = Customer.query.get_or_404(customer_id)

    vehicle = Vehicle(
        customer_id=customer_id,
        category=request.form.get('category'),
        model=request.form.get('model'),
        year_of_manufacture=request.form.get('year_of_manufacture', type=int),
        registration_no=request.form.get('registration_no'),
        chassis_no=request.form.get('chassis_no'),
        engine_no=request.form.get('engine_no'),
        passing_type=request.form.get('passing_type')
    )
    db.session.add(vehicle)
    db.session.commit()
    flash('Vehicle added successfully.', 'success')
    return redirect(url_for('customers.customer_detail', id=customer_id))

@vehicles.route('/vehicles/<int:id>')
def vehicle_detail(id):
    vehicle = Vehicle.query.get_or_404(id)
    return render_template('vehicles/detail.html', vehicle=vehicle)

@vehicles.route('/vehicles/<int:id>/edit', methods=['GET', 'POST'])
def edit_vehicle(id):
    vehicle = Vehicle.query.get_or_404(id)

    if request.method == 'POST':
        vehicle.category = request.form.get('category')
        vehicle.model = request.form.get('model')
        vehicle.year_of_manufacture = request.form.get('year_of_manufacture', type=int)
        vehicle.registration_no = request.form.get('registration_no')
        vehicle.chassis_no = request.form.get('chassis_no')
        vehicle.engine_no = request.form.get('engine_no')
        vehicle.passing_type = request.form.get('passing_type')

        db.session.commit()
        flash('Vehicle updated successfully.', 'success')
        return redirect(url_for('vehicles.vehicle_detail', id=vehicle.id))

    return render_template('vehicles/edit.html',
                           vehicle=vehicle,
                           categories=VEHICLE_CATEGORIES,
                           passing_types=PASSING_TYPES)