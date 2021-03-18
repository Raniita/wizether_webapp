from flask import Blueprint, render_template, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from app import tasks
from app.permission import restricted_role
from app.forms import NewStation, NewGateway, QueryAPI_DateRange_Field, QueryAPI_DateRange_All

dashboard_bp = Blueprint('dashboard', __name__)

#
# Home page
#
@dashboard_bp.route('/dashboard')
@login_required
def home():
    return render_template('dashboard/home.html', user=current_user)

#
# Mis estaciones
#
@dashboard_bp.route('/my_stations')
@login_required
def my_stations():
    return render_template('dashboard/my_stations.html', user=current_user)


#
# Nueva Estación
#
@dashboard_bp.route('/new_station', methods=['GET', 'POST'])
@login_required
def new_station():

    form = NewStation()
    if form.validate_on_submit():
        lat = form.lat.data
        lon = form.lon.data
        place = form.place.data

        flash('Estación registrada con éxito en latitud: {}, longitud:{} y {}'.format(lat, lon, place))
        return redirect(url_for('dashboard.new_station'))

    return render_template('dashboard/new_station.html', user=current_user, form=form)


#
# Nuevo Gateway
#
@dashboard_bp.route('/new_gateway', methods=['GET', 'POST'])
@login_required
def new_gateway():
    form = NewGateway()
    if form.validate_on_submit():
        lat = form.lat.data
        lon = form.lon.data
        place = form.place.data
        power = form.power.data

        flash('Gateway registrado con éxito en latitud: {}, longitud:{}, {} y con potencia {}'.format(lat, lon, place, power))
        return redirect(url_for('dashboard.new_gateway'))

    return render_template('dashboard/new_gateway.html', user=current_user, form=form)


#
# Open API
#
@dashboard_bp.route('/openapi')
@login_required
def open_api():

    form1 = QueryAPI_DateRange_Field()
    form2 = QueryAPI_DateRange_All()

    return render_template('dashboard/api.html', user=current_user, form1=form1,
                                                                    form2=form2)