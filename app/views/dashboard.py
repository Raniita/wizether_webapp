from flask import Blueprint, render_template, redirect, url_for, flash
from flask import current_app as app
from flask_login import login_required, logout_user, current_user

from app import tasks, DEVICES
from app.permission import restricted_role
from app.forms import *

dashboard_bp = Blueprint('dashboard', __name__)

#
# Home page
#
@dashboard_bp.route('/dashboard')
@login_required
def home():

    src_temp = "https://grafana.wize.ranii.pro/d-solo/SUaxNOwMk/portal-graphs-20212230?orgId=1&refresh=5m&panelId=2"
    src_hum = "https://grafana.wize.ranii.pro/d-solo/SUaxNOwMk/portal-graphs-20212230?orgId=1&refresh=5m&panelId=4"
    src_air = "https://grafana.wize.ranii.pro/d-solo/SUaxNOwMk/portal-graphs-20212230?orgId=1&refresh=5m&panelId=6"
    src_press = "https://grafana.wize.ranii.pro/d-solo/SUaxNOwMk/portal-graphs-20212230?orgId=1&refresh=5m&panelId=9"
    src_loud = "https://grafana.wize.ranii.pro/d-solo/SUaxNOwMk/portal-graphs-20212230?orgId=1&refresh=5m&panelId=10"

    return render_template('dashboard/home.html', user=current_user, src_temp=src_temp,
                                                                     src_hum=src_hum,
                                                                     src_air=src_air,
                                                                     src_press=src_press,
                                                                     src_loud=src_loud)

#
# Mis estaciones
#
@dashboard_bp.route('/my_stations')
@login_required
def my_stations():
    return render_template('dashboard/my_stations.html', user=current_user, devices=DEVICES)


#
# Nueva Estación
#
@dashboard_bp.route('/new_station', methods=['GET', 'POST'])
@login_required
def new_station():

    form = NewStation()
    if form.validate_on_submit():
        device = form.device_name.data
        lat = form.lat.data
        lon = form.lon.data
        place = form.place.data

        new_station = {'device': device,
                'latitude': lat,
                'longitude': lon,
                'location': place,
                'version': 'v1'}

        # On production --> De-sync of WSGI
        #DEVICES.append(new_station)

        flash('Estación registrada con éxito en latitud: {}, longitud:{} y {}'.format(lat, lon, place))
        return redirect(url_for('dashboard.new_station'))

    return render_template('dashboard/new_station.html', user=current_user, form=form)

#
# Solicitar Nueva estación
#
@dashboard_bp.route('/ask_station', methods=['GET', 'POST'])
@login_required
def ask_station():
    form = AskStation()
    if form.validate_on_submit():
        email = form.email.data

        flash('Hemos registrado tu solicitud. Nos pondremos en contacto con {}. ¡Muchas gracias!'.format(email))
        return redirect(url_for('dashboard.ask_station'))

    return render_template('dashboard/ask_station.html', user=current_user, form=form)

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
    form3 = QueryAPI_history_device()

    form4 = QueryAPI_lastweek_device()
    form5 = QueryAPI_lastweek_device_max()

    return render_template('dashboard/api.html', user=current_user, form1=form1,
                                                                    form2=form2,
                                                                    form3=form3,
                                                                    form4=form4,
                                                                    form5=form5)