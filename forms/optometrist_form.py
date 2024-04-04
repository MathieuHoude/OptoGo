from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Regexp, Length

class OptometristForm(FlaskForm):
    exercise_number = StringField('Numéro de pratique', validators=[DataRequired(), Length(min=10, max=10, message='Doit être un code à 10 chiffres.')])
    phone_number = StringField('Téléphone', validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$', message="Format invalide, veuillez entrer un numéro sous la forme XXX-XXX-XXXX")])