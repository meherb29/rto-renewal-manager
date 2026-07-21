from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from app.models import Renewal, Vehicle, Insurer, Employee, FollowupLog
from datetime import datetime, date, timedelta

renewals = Blueprint('renewals', __name__)

@renewals.route('/renewals')
def list_renewals():
    all_renewals = Renewal.query.order_by(Renewal.policy_end).all()
    return render_template('renewals/list.html', renewals=all_renewals)

@renewals.route('/renewals/new')
def new_renewal():
    vehicle_id = request.args.get('vehicle_id', type=int)
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    insurers = Insurer.query.order_by(Insurer.name).all()
    employees = Employee.query.order_by(Employee.name).all()
    return render_template('renewals/form.html',
                           vehicle=vehicle,
                           insurers=insurers,
                           employees=employees)

@renewals.route('/renewals/new', methods=['POST'])
def create_renewal():
    vehicle_id = request.form.get('vehicle_id', type=int)
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    policy_end_str = request.form.get('policy_end')
    policy_end = datetime.strptime(policy_end_str, '%Y-%m-%d').date() if policy_end_str else None
    policy_start_str = request.form.get('policy_start')
    policy_start = datetime.strptime(policy_start_str, '%Y-%m-%d').date() if policy_start_str else None

    reminder_due = policy_end - timedelta(days=60) if policy_end else None

    renewal = Renewal(
        vehicle_id=vehicle_id,
        insurer_id=request.form.get('insurer_id', type=int),
        employee_id=request.form.get('employee_id', type=int),
        policy_number=request.form.get('policy_number'),
        policy_start=policy_start,
        policy_end=policy_end,
        reminder_due=reminder_due,
        idv=request.form.get('idv', type=float),
        status='open',
        data_confirmed=request.form.get('data_confirmed') == 'confirmed',
        last_known_year=request.form.get('last_known_year', type=int),
        notes=request.form.get('notes')
    )
    db.session.add(renewal)
    db.session.commit()
    flash('Renewal created successfully.', 'success')
    return redirect(url_for('renewals.renewal_detail', id=renewal.id))

@renewals.route('/renewals/<int:id>')
def renewal_detail(id):
    renewal = Renewal.query.get_or_404(id)
    return render_template('renewals/detail.html', 
                           renewal=renewal,
                           today=date.today())

@renewals.route('/renewals/<int:id>/edit', methods=['GET', 'POST'])
def edit_renewal(id):
    renewal = Renewal.query.get_or_404(id)
    insurers = Insurer.query.order_by(Insurer.name).all()
    employees = Employee.query.order_by(Employee.name).all()

    if request.method == 'POST':
        policy_end_str = request.form.get('policy_end')
        policy_end = datetime.strptime(policy_end_str, '%Y-%m-%d').date() if policy_end_str else None
        policy_start_str = request.form.get('policy_start')
        policy_start = datetime.strptime(policy_start_str, '%Y-%m-%d').date() if policy_start_str else None

        renewal.insurer_id = request.form.get('insurer_id', type=int)
        renewal.employee_id = request.form.get('employee_id', type=int)
        renewal.policy_number = request.form.get('policy_number')
        renewal.policy_start = policy_start
        renewal.policy_end = policy_end
        renewal.reminder_due = policy_end - timedelta(days=60) if policy_end else None
        renewal.idv = request.form.get('idv', type=float)
        renewal.status = request.form.get('status')
        renewal.data_confirmed = request.form.get('data_confirmed') == 'confirmed'
        renewal.last_known_year = request.form.get('last_known_year', type=int)
        renewal.notes = request.form.get('notes')

        db.session.commit()
        flash('Renewal updated successfully.', 'success')
        return redirect(url_for('renewals.renewal_detail', id=renewal.id))

    return render_template('renewals/edit.html',
                           renewal=renewal,
                           insurers=insurers,
                           employees=employees)

@renewals.route('/renewals/<int:id>/followup', methods=['POST'])
def add_followup(id):
    renewal = Renewal.query.get_or_404(id)

    contacted_on_str = request.form.get('contacted_on')
    contacted_on = datetime.strptime(contacted_on_str, '%Y-%m-%d').date() if contacted_on_str else date.today()

    followup = FollowupLog(
        renewal_id=renewal.id,
        employee_id=request.form.get('employee_id', type=int),
        contacted_on=contacted_on,
        outcome=request.form.get('outcome'),
        notes=request.form.get('notes')
    )
    db.session.add(followup)

    new_status = request.form.get('status')
    if new_status:
        renewal.status = new_status

    db.session.commit()
    flash('Follow-up logged.', 'success')
    return redirect(url_for('renewals.renewal_detail', id=renewal.id))

@renewals.route('/renewals/<int:id>/pdf', methods=['GET', 'POST'])
def generate_pdf(id):
    renewal = Renewal.query.get_or_404(id)

    if request.method == 'POST':
        premium = request.form.get('premium', type=float)
        return render_template('renewals/pdf.html',
                               renewal=renewal,
                               premium=premium)

    return render_template('renewals/pdf_form.html', renewal=renewal)