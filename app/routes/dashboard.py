from flask import Blueprint, render_template
from flask_login import login_required
from app.models import Renewal
from datetime import date, timedelta

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/')
@login_required
def index():
    today = date.today()
    seven_days = today + timedelta(days=7)
    sixty_days = today + timedelta(days=60)

    urgent = Renewal.query.filter(
        Renewal.policy_end <= seven_days,
        Renewal.policy_end >= today,
        Renewal.status.notin_(['completed', 'lapsed'])
    ).order_by(Renewal.policy_end).all()

    upcoming = Renewal.query.filter(
        Renewal.policy_end > seven_days,
        Renewal.policy_end <= sixty_days,
        Renewal.status.notin_(['completed', 'lapsed'])
    ).order_by(Renewal.policy_end).all()

    overdue = Renewal.query.filter(
        Renewal.policy_end < today,
        Renewal.status.notin_(['completed', 'lapsed'])
    ).order_by(Renewal.policy_end).all()

    return render_template('dashboard/index.html',
                           urgent=urgent,
                           upcoming=upcoming,
                           overdue=overdue,
                           today=today)