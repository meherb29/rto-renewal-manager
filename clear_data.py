from app import create_app, db
from app.models import Customer, Vehicle, Renewal, FollowupLog, Document, Employee

app = create_app()

with app.app_context():
    FollowupLog.query.delete()
    Document.query.delete()
    Renewal.query.delete()
    Vehicle.query.delete()
    Customer.query.delete()
    db.session.commit()
    print('All data cleared. Insurers kept.')