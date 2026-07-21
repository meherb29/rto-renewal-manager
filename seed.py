from app import create_app, db
from app.models import Customer, Vehicle, Insurer, Employee, Renewal, FollowupLog
from datetime import date, timedelta

app = create_app()

with app.app_context():

    # Clear existing data (keeps nothing)
    FollowupLog.query.delete()
    Renewal.query.delete()
    Vehicle.query.delete()
    Customer.query.delete()
    db.session.commit()

    # Insurers (keep existing or recreate)
    insurer_names = [
        'Bajaj Allianz', 'Go Digit', 'IFFCO-Tokio',
        'Reliance General', 'United India', 'National Insurance',
        'Cholamandalam', 'Kotak General', 'New India Assurance', 'Zuno'
    ]
    insurers = {}
    for name in insurer_names:
        i = Insurer.query.filter_by(name=name).first()
        if not i:
            i = Insurer(name=name)
            db.session.add(i)
            db.session.flush()
        insurers[name] = i

    # Admin employee
    admin = Employee.query.filter_by(email='admin@demo.com').first()
    if not admin:
        admin = Employee(name='Prachi Mhatre', branch='Navi Mumbai', role='admin', email='admin@demo.com')
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.flush()

    emp2 = Employee.query.filter_by(email='sonali@demo.com').first()
    if not emp2:
        emp2 = Employee(name='Sonali Patil', branch='Pen', role='employee', email='sonali@demo.com')
        emp2.set_password('employee123')
        db.session.add(emp2)
        db.session.flush()

    db.session.commit()

    today = date.today()

    # Customers
    customers_data = [
        ('Pamtec Enviro Systems Pvt Ltd', '9820111111', 'Navi Mumbai', True,  '27AABCP1234F1Z5', 'AABCP1234F'),
        ('Helpage India',                 '9820222222', 'Navi Mumbai', True,  '27AABHP5678G2Z6', 'AABHP5678G'),
        ('Rajmata Construction',          '9820333333', 'Pen',         True,  '27AABRP9012H3Z7', 'AABRP9012H'),
        ('Shri Balaji International',     '9820444444', 'Navi Mumbai', True,  '27AABSP3456I4Z8', 'AABSP3456I'),
        ('Orange Construction Co',        '9820555555', 'Pen',         True,  '27AABOP7890J5Z9', 'AABOP7890J'),
        ('Ashok D. Koli',                 '9821111111', 'Navi Mumbai', False, None,              None),
        ('Vaibhav Borkar',                '9821222222', 'Pen',         False, None,              None),
        ('Santosh Mhatre',                '9821333333', 'Navi Mumbai', False, None,              None),
        ('Pradeep Sawant',                '9821444444', 'Pen',         False, None,              None),
        ('Ramesh Patil',                  '9821555555', 'Navi Mumbai', False, None,              None),
    ]

    customers = []
    for name, phone, branch, is_company, gst, pan in customers_data:
        c = Customer(name=name, phone=phone, branch=branch, is_company=is_company, gst_number=gst, pan_number=pan)
        db.session.add(c)
        db.session.flush()
        customers.append(c)

    db.session.commit()

    # Vehicles
    vehicles_data = [
        # (customer_index, category, model, reg_no, chassis, engine, passing_type, year)
        (0, 'Tractor',    'Tiger 75 4WD',       'MH-06-XX-1111', 'EZHDKXXXXX', '4107BMXXXXX', 'MH',      2021),
        (0, 'Tractor',    'Tiger 75 4WD',       'MH-06-XX-1112', 'EZHDKYYYYYY','4107BMYYYYY', 'MH',      2021),
        (0, 'Tractor',    'DI 47 RX',           'MH-06-XX-1113', 'DIHDKXXXXX', 'DI07BMXXXXX', 'Company', 2020),
        (1, 'Force Bus',  'T1 4020 20+D',       'MH-02-FX-4535', 'FTBUSXXXXX', 'FT20BMXXXXX', 'MH',      2019),
        (1, 'Force Bus',  'Urbania 16+D',       'MH-02-FX-4536', 'FURBIXXXXX', 'FU16BMXXXXX', 'Tourist', 2022),
        (2, 'Force Bus',  'Monobus 33+D',       'MH-46-CL-2550', 'FMONXXXXX',  'FM33BMXXXXX', 'MH',      2018),
        (2, 'Tractor',    'VST Shakti 130 DI',  'MH-46-CL-2551', 'VSTSHXXXXX', 'VST0BMXXXXX', 'MH',      2020),
        (3, 'Force Bus',  'T1 4020 26+D',       'MH-12-AB-1234', 'FT26BUSXXX', 'FT26BMXXXXX', 'Company', 2021),
        (3, 'Force Bus',  'T1 4020 26+D',       'MH-12-AB-1235', 'FT26BUSYYY', 'FT26BMYYYYY', 'Company', 2021),
        (4, 'Tractor',    'Sonalika DI 47',     'MH-46-DL-7890', 'SONALIXXXXX','SONA7BMXXXXX','MH',      2019),
        (5, 'Two-Wheeler','Honda CB Shine',      'MH-02-GH-5678', 'CBSHIXXXXX', 'CB12BMXXXXX', 'MH',      2022),
        (6, 'Car/SUV',    'Maruti Swift',        'MH-46-KL-3456', 'SWIFTXXXXX', 'SW15BMXXXXX', 'MH',      2020),
        (7, 'Force Bus',  'T1 4020 20+D',       'MH-02-PQ-9012', 'FT20BUSXXX', 'FT20BMZZZZZ', 'MH',      2018),
        (8, 'Tractor',    'Tiger 75 4WD',       'MH-46-RS-1234', 'TIGERXXXXX', 'TIG7BMXXXXX', 'MH',      2021),
        (9, 'Two-Wheeler','Honda Activa',        'MH-02-TU-5678', 'ACTIVXXXXX', 'AC11BMXXXXX', 'MH',      2023),
    ]

    vehicles = []
    for ci, cat, model, reg, chassis, engine, passing, year in vehicles_data:
        v = Vehicle(
            customer_id=customers[ci].id,
            category=cat,
            model=model,
            registration_no=reg,
            chassis_no=chassis,
            engine_no=engine,
            passing_type=passing,
            year_of_manufacture=year
        )
        db.session.add(v)
        db.session.flush()
        vehicles.append(v)

    db.session.commit()

    # Renewals
    # Spread across overdue, urgent, upcoming, and completed statuses
    renewals_data = [
        # (vehicle_index, insurer_name, policy_no, start_offset_days, end_offset_days, status, employee, data_confirmed)
        (0,  'Reliance General',     'RG-2024-001', -365, -5,   'open',        admin, True),   # overdue
        (1,  'Reliance General',     'RG-2024-002', -365, -10,  'in_progress', admin, True),   # overdue
        (2,  'IFFCO-Tokio',          'IT-2024-003', -365, 3,    'open',        emp2,  True),   # urgent
        (3,  'Go Digit',             'GD-2024-004', -365, 5,    'in_progress', admin, True),   # urgent
        (4,  'Bajaj Allianz',        'BA-2024-005', -365, 7,    'open',        emp2,  True),   # urgent
        (5,  'IFFCO-Tokio',          'IT-2024-006', -365, 20,   'open',        admin, True),   # upcoming
        (6,  'Kotak General',        'KG-2024-007', -365, 30,   'in_progress', emp2,  True),   # upcoming
        (7,  'United India',         'UI-2024-008', -365, 45,   'open',        admin, True),   # upcoming
        (8,  'New India Assurance',  'NIA-2024-009',-365, 55,   'open',        emp2,  True),   # upcoming
        (9,  'Cholamandalam',        'CH-2024-010', -365, 58,   'in_progress', admin, True),   # upcoming
        (10, 'Zuno',                 'ZN-2024-011', -365, -30,  'lapsed',      emp2,  True),   # lapsed
        (11, 'Go Digit',             'GD-2024-012', -365, -60,  'completed',   admin, True),   # completed
        (12, 'Bajaj Allianz',        'BA-2024-013', -365, 90,   'open',        emp2,  False),  # estimated
        (13, 'National Insurance',   'NI-2024-014', -365, 100,  'open',        admin, True),   # far upcoming
        (14, 'Reliance General',     'RG-2024-015', -365, 120,  'open',        emp2,  True),   # far upcoming
    ]

    renewals = []
    for vi, ins_name, policy_no, start_offset, end_offset, status, emp, confirmed in renewals_data:
        policy_start = today + timedelta(days=start_offset)
        policy_end = today + timedelta(days=end_offset)
        reminder_due = policy_end - timedelta(days=60)
        insurer = insurers[ins_name]
        r = Renewal(
            vehicle_id=vehicles[vi].id,
            insurer_id=insurer.id,
            employee_id=emp.id,
            policy_number=policy_no,
            policy_start=policy_start,
            policy_end=policy_end,
            reminder_due=reminder_due,
            idv=round(10000 + (vi * 1500), 2),
            status=status,
            data_confirmed=confirmed,
            last_known_year=2024 if not confirmed else None
        )
        db.session.add(r)
        db.session.flush()
        renewals.append(r)

    db.session.commit()

    # Follow-up logs for some renewals
    followups_data = [
        (1, admin, today - timedelta(days=5),  'called_no_answer', 'Called on mobile, no response.'),
        (1, admin, today - timedelta(days=3),  'whatsapp_sent',    'Sent renewal reminder on WhatsApp with policy end date.'),
        (3, emp2,  today - timedelta(days=8),  'called_spoke',     'Spoke to owner. Interested in renewing with Go Digit. Will confirm by end of week.'),
        (3, emp2,  today - timedelta(days=5),  'quote_sent',       'Sent Go Digit quote. Awaiting confirmation.'),
        (6, admin, today - timedelta(days=15), 'called_spoke',     'Customer confirmed renewal. Processing with Kotak General.'),
        (6, admin, today - timedelta(days=10), 'confirmed',        'Policy confirmed. Documents sent to insurer.'),
        (9, admin, today - timedelta(days=20), 'called_no_answer', 'No answer. Will try again tomorrow.'),
        (9, admin, today - timedelta(days=18), 'whatsapp_sent',    'Sent WhatsApp message with renewal details.'),
        (9, emp2,  today - timedelta(days=10), 'called_spoke',     'Customer asked for Cholamandalam quote. Quote sent.'),
    ]

    for ri, emp, contacted_on, outcome, notes in followups_data:
        f = FollowupLog(
            renewal_id=renewals[ri].id,
            employee_id=emp.id,
            contacted_on=contacted_on,
            outcome=outcome,
            notes=notes
        )
        db.session.add(f)

    db.session.commit()
    print('Seed complete.')
    print('Admin login: admin@demo.com / admin123')
    print('Employee login: sonali@demo.com / employee123')
    print(f'Customers: {len(customers)}')
    print(f'Vehicles: {len(vehicles)}')
    print(f'Renewals: {len(renewals)}')
    