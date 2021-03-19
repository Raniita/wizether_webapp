from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.fields.html5 import DateField
from wtforms.fields import SelectField, DecimalField

class SignupForm(FlaskForm):
    """ User sign-up Form """

    name = StringField(
        'Nombre',
        validators=[DataRequired()]
    )

    email = StringField(
        'Email',
        validators=[
            Length(min=6),
            Email(message='Introduce un email válido.'),
            DataRequired()
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6, message='Utiliza una contraseña más fuerte.')
        ]
    )

    confirm = PasswordField(
        'Confirma tu contraseña',
        validators=[
            DataRequired(),
            EqualTo('password', message='Las contraseñas deben coincidir.')
        ]
    )

    website = StringField(
        'Website',
        validators=[Optional()]
    )

    submit = SubmitField('Registrar')

class LoginForm(FlaskForm):
    """ User Log-in Form. """

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(message='Introduce un email válido.')
        ]
    )

    password = PasswordField(
        'Contraseña',
        validators=[DataRequired()]
    )

    submit = SubmitField('Acceder')

class ChangePasswordForm(FlaskForm):
    """ User change password """

    password = PasswordField(
        'Contraseña',
        validators=[
            DataRequired(),
            Length(min=6, message='Utiliza una contraseña más fuerte.')
        ]
    )

    confirm = PasswordField(
        'Confirma tu contraseña',
        validators=[
            DataRequired(),
            EqualTo('password', message='Las contraseñas deben coincidir.')
        ]
    )

    new_password = PasswordField(
        'Nueva contraseña',
        validators=[
            DataRequired(),
            Length(min=6, message='Utiliza una contraseña más fuerte.')
        ]
    )

    confirm_new = PasswordField(
        'Confirma tu nueva contraseña',
        validators=[
            DataRequired(),
            EqualTo('new_password', message='Las contraseñas deben coincidir.')
        ]
    )

    submit = SubmitField('Cambiar contraseña')

#
#   Nueva estación
#
class NewStation(FlaskForm):
    """ Add a new station to the system """

    device_name = StringField(
        'Número de seríe de tu nueva estación'
    )

    lat = DecimalField(
        'Latitud aproximada', places=2
    )

    lon = DecimalField(
        'Longitud aproximada', places=2
    )

    place = SelectField(
        'Selecciona su emplazamiento', choices=[('in-door','Interior'), ('out-door', 'Exterior')]
    )

    submit = SubmitField('Confirmar')

#
#   Solicitar estación
#
class AskStation(FlaskForm):
    """ Ask to a Station """

    email = StringField(
        'Email de contacto',
        validators=[
            Length(min=6),
            Email(message='Introduce un email válido.'),
            DataRequired()
        ]
    )

    submit = SubmitField('Confirmar')

#
#   Nuevo gateway
#
class NewGateway(FlaskForm):
    """ Add a new gateway to the system """

    device_name = StringField(
        'Número de seríe del nuevo gateway'
    )

    lat = DecimalField(
        'Latitud aproximada', places=2
    )

    lon = DecimalField(
        'Longitud aproximada', places=2
    )

    place = SelectField(
        'Selecciona su emplazamiento', choices=[('in-door','Interior'), ('out-door', 'Exterior')]
    )

    power = SelectField(
        'Selecciona la potencia de transmisión', choices=[('21', '21 dBm'), ('16','16 dBm')]
    )

    submit = SubmitField('Confirmar')


#
#   OpenAPI
#

class QueryAPI_DateRange_Field(FlaskForm):
    """ Get one field on a date range """

    start_date = DateField(
        'Fecha de inicio'
    )

    stop_date = DateField(
        'Fecha de fin'
    )

    fields = SelectField(
        'Selecciona el dato', choices=[('temperature', 'Temperatura'),
                                                    ('pressure', 'Presión'),
                                                    ('humidity', 'Humedad'),
                                                    ('loudness', 'Ruido'),
                                                    ('air_quality', 'Calidad de aire')]
    )

    sensors = SelectField(
        'Filtrar por sensor', choices=[('20212230','20212230')]
    )

    submit = SubmitField('Obtener datos')

class QueryAPI_DateRange_All(FlaskForm):
    """ Get all fields on a date range """

    start_date = DateField(
        'Fecha de inicio'
    )

    stop_date = DateField(
        'Fecha de fin'
    )

    sensors = SelectField(
        'Filtrar por sensor', choices=[('20212230','20212230')]
    )

    submit = SubmitField('Obtener datos')

class QueryAPI_history_device(FlaskForm):
    """ Get all values measured by a device """

    sensors = SelectField(
        'Filtrar por sensor', choices=[('20212230','20212230')]
    )

    submit = SubmitField('Obtener datos')

class QueryAPI_lastweek_device(FlaskForm):
    """ Get all values measured over the last week """

    sensors = SelectField(
        'Filtrar por sensor', choices=[('20212230','20212230')]
    )

    submit = SubmitField('Obtener datos')

class QueryAPI_lastweek_device_max(FlaskForm):
    """ Get all values measured over the last week """

    sensors = SelectField(
        'Filtrar por sensor', choices=[('20212230','20212230')]
    )

    submit = SubmitField('Obtener datos')