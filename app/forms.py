from flask_wtf import Form
from wtforms import SubmitField, StringField, RadioField
from wtforms.validators import DataRequired, Required


class DeleteForm(Form):
    delete = SubmitField('delete')


class RestaurantForm(Form):
    name = StringField('name', validators=[DataRequired()])
    submit = SubmitField('submit')


class MenuForm(Form):
    name = StringField('name', validators=[DataRequired()])
    description = StringField('name', validators=[DataRequired()])
    price = StringField('name', validators=[DataRequired()])
    course = RadioField('course',
                        validators=[Required()],
                        choices=[('Appetizer', 'Appetizer'),
                                 ('Entree', 'Entree'),
                                 ('Dessert', 'Dessert'),
                                 ('Beverage', 'Beverage')])
    submit = SubmitField('submit')
