from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from flask_login import login_required 
from app.models import Customer, Document 
import os
from flask import current_app
from werkzeug.utils import secure_filename
from flask import send_from_directory

customers = Blueprint('customers', __name__)

@customers.route('/customers')
@login_required
def list_customers():
    all_customers = Customer.query.order_by(Customer.name).all()
    return render_template('customers/list.html', customers=all_customers)

@customers.route('/customers/new', methods=['GET', 'POST'])
@login_required
def new_customer():
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        branch = request.form.get('branch')
        is_company = request.form.get('is_company') == 'on'
        gst_number = request.form.get('gst_number')
        pan_number = request.form.get('pan_number')

        customer = Customer(
            name=name,
            phone=phone,
            branch=branch,
            is_company=is_company,
            gst_number=gst_number,
            pan_number=pan_number
        )
        db.session.add(customer)
        db.session.commit()
        flash('Customer added successfully.', 'success')
        return redirect(url_for('customers.list_customers'))

    return render_template('customers/form.html')

@customers.route('/customers/<int:id>')
@login_required 
def customer_detail(id):
    customer = Customer.query.get_or_404(id)
    return render_template('customers/detail.html', customer=customer)

@customers.route('/customers/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_customer(id):
    customer = Customer.query.get_or_404(id)

    if request.method == 'POST':
        customer.name = request.form.get('name')
        customer.phone = request.form.get('phone')
        customer.branch = request.form.get('branch')
        customer.is_company = request.form.get('is_company') == 'on'
        customer.gst_number = request.form.get('gst_number')
        customer.pan_number = request.form.get('pan_number')

        db.session.commit()
        flash('Customer updated successfully.', 'success')
        return redirect(url_for('customers.customer_detail', id=customer.id))

    return render_template('customers/form.html', customer=customer)

ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@customers.route('/customers/<int:id>/upload', methods=['POST'])
@login_required
def upload_document(id):
    customer = Customer.query.get_or_404(id)
    doc_type = request.form.get('doc_type')
    file = request.files.get('file')

    if not file or file.filename == '':
        flash('No file selected.', 'error')
        return redirect(url_for('customers.customer_detail', id=id))

    if not allowed_file(file.filename):
        flash('Only JPG and PNG files are allowed.', 'error')
        return redirect(url_for('customers.customer_detail', id=id))

    filename = secure_filename(f"{id}_{doc_type}_{file.filename}")
    file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    existing = Document.query.filter_by(customer_id=id, doc_type=doc_type).first()
    if existing:
        old_path = os.path.join(current_app.config['UPLOAD_FOLDER'], existing.filename)
        if os.path.exists(old_path):
            os.remove(old_path)
        existing.filename = filename
    else:
        doc = Document(customer_id=id, doc_type=doc_type, filename=filename)
        db.session.add(doc)

    db.session.commit()
    flash(f'{doc_type.replace("_", " ").title()} uploaded successfully.', 'success')
    return redirect(url_for('customers.customer_detail', id=id))

@customers.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)