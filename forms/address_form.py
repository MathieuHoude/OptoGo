from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, Regexp

class AddressForm(FlaskForm):
    street_number = StringField('Numéro civique', validators=[
        DataRequired(message="Street number is required")
    ], render_kw={'class': "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:value-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"})
    street_name = StringField('Rue', validators=[
        DataRequired(message="Street name is required"),
        Length(min=1, max=50, message="Street name must be between 1 and 50 characters")
    ], render_kw={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:value-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
    city = StringField('Ville', validators=[
        DataRequired(message="City is required"),
        Length(min=1, max=50, message="City must be between 1 and 50 characters")
    ], render_kw={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:value-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
    province = StringField('Province', validators=[
        DataRequired(message="Province is required"),
        Length(min=1, max=20, message="Province must be between 1 and 20 characters")
    ], render_kw={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:value-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
    postal_code = StringField('Code Postal', validators=[
        DataRequired(message="Postal code is required"),
        Length(min=6, max=6, message="Postal code must be 6 characters long"),
        Regexp('^[A-Za-z][0-9][A-Za-z][0-9][A-Za-z][0-9]$', message="Invalid postal code format")
    ], render_kw={'class': 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:value-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'})
