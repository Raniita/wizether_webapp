from flask import Blueprint, render_template, redirect, url_for
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from app import tasks
from app.permission import restricted_role
from app.forms import QueryAPI

dashboard_bp = Blueprint('dashboard', __name__)

#
# Home page
#
@dashboard_bp.route('/dashboard')
@login_required
def home():
    return render_template('dashboard/home.html', user=current_user)


#
# Open API
#
@dashboard_bp.route('/openapi')
@login_required
def open_api():

    form = QueryAPI()

    return render_template('dashboard/api.html', user=current_user, form=form)