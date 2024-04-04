from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Email, Regexp

class PatientForm(FlaskForm):
    first_name = StringField('Prénom', validators=[DataRequired()])
    last_name = StringField('Nom', validators=[DataRequired()])
    phone_number = StringField('Téléphone', validators=[DataRequired(), Regexp(r'^\d{3}-\d{3}-\d{4}$', message="Format invalide, veuillez entrer un numéro sous la forme XXX-XXX-XXXX")])
    gender = SelectField('Sexe', choices=[('Male', 'Homme'), ('Female', 'Femme'),('Genderqueer', 'Non-binaire'),('Bigender', 'Bigenre'),('Agender', 'Agenre'), ('Polygender', 'Polygenre'),('Other', 'Autre')])
    email = StringField('Email', validators=[DataRequired(), Email()])
    birth_date = DateField('Date de naissance', format='%Y-%m-%d', validators=[DataRequired()])
    RAMQ_number = StringField('RAMQ', validators=[DataRequired(), Regexp(r'^[a-zA-Z]{4}\d{8}$', message="Format invalide. Devrait être sous la forme ABCD12345678")])