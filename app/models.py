from app import db
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Customer(db.Model):
    __tablename__ = 'customer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    branch = db.Column(db.String(100), nullable=False)
    is_company = db.Column(db.Boolean, default=False)
    gst_number = db.Column(db.String(20), nullable=True)
    pan_number = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    vehicles = db.relationship('Vehicle', backref='customer', lazy=True)
    documents = db.relationship('Document', backref='customer', lazy=True)

    def __repr__(self):
        return f'<Customer {self.name}>'
    
class Insurer(db.Model):
    __tablename__ = 'insurer'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    renewals = db.relationship('Renewal', backref='insurer', lazy=True)

    def __repr__(self):
        return f'<Insurer {self.name}>'

class Employee(db.Model,UserMixin):
    __tablename__ = 'employee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    branch = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='employee')
    email = db.Column(db.String(120), nullable=False, unique=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    renewals = db.relationship('Renewal', backref='employee', lazy=True)
    followups = db.relationship('FollowupLog', backref='employee', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<Employee {self.name}>'

class Vehicle(db.Model):
    __tablename__ = 'vehicle'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    year_of_manufacture = db.Column(db.Integer, nullable=True)
    registration_no = db.Column(db.String(20), nullable=True)
    chassis_no = db.Column(db.String(50), nullable=True)
    engine_no = db.Column(db.String(50), nullable=True)
    passing_type = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    renewals = db.relationship('Renewal', backref='vehicle', lazy=True)

    def __repr__(self):
        return f'<Vehicle {self.registration_no} - {self.model}>'

class Renewal(db.Model):
    __tablename__ = 'renewal'

    id = db.Column(db.Integer, primary_key=True)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicle.id'), nullable=False)
    insurer_id = db.Column(db.Integer, db.ForeignKey('insurer.id'), nullable=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=True)
    policy_number = db.Column(db.String(100), nullable=True)
    policy_start = db.Column(db.Date, nullable=True)
    policy_end = db.Column(db.Date, nullable=True)
    reminder_due = db.Column(db.Date, nullable=True)
    idv = db.Column(db.Float, nullable=True)
    premium = db.Column(db.Float, nullable=True)
    status = db.Column(db.String(20), nullable=False, default='open')
    data_confirmed = db.Column(db.Boolean, default=True)
    last_known_year = db.Column(db.Integer, nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    followups = db.relationship('FollowupLog', backref='renewal', lazy=True)

    def __repr__(self):
        return f'<Renewal {self.id} - {self.status}>'

class FollowupLog(db.Model):
    __tablename__ = 'followup_log'

    id = db.Column(db.Integer, primary_key=True)
    renewal_id = db.Column(db.Integer, db.ForeignKey('renewal.id'), nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('employee.id'), nullable=False)
    contacted_on = db.Column(db.Date, nullable=False)
    outcome = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<FollowupLog {self.id} - {self.outcome}>'

class Document(db.Model):
    __tablename__ = 'document'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    doc_type = db.Column(db.String(50), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Document {self.doc_type} - {self.filename}>'                        