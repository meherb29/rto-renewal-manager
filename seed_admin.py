from app import create_app, db
from app.models import Employee

app = create_app()

with app.app_context():
    if Employee.query.first():
        print('Admin already exists, skipping.')
    else:
        admin = Employee(
            name='RTO Incharge',
            branch='Pen',
            role='admin',
            email='admin@baldev.com'
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print('Admin created. Email: admin@baldev.com | Password: admin123')