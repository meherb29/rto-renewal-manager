from app import create_app, db
from app.models import Insurer

app = create_app()

with app.app_context():
    insurers = [
        'Bajaj Allianz', 'Go Digit', 'IFFCO-Tokio',
        'Reliance General', 'United India', 'National Insurance',
        'Cholamandalam', 'Kotak General', 'New India Assurance', 'Zuno'
    ]
    for name in insurers:
        db.session.add(Insurer(name=name))
    db.session.commit()
    print('Insurers added.')