from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional
from wtforms.fields.html5 import DateField
from wtforms.fields import SelectField

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


class QueryAPI(FlaskForm):
    """ Try of Form for Query Data """

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

    submit = SubmitField('Obtener datos')