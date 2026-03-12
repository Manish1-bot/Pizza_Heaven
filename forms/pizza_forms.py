from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, FloatField, BooleanField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired

class PizzaForm(FlaskForm):
    name = StringField('Pizza Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[('veg', 'Vegetarian'), ('non-veg', 'Non-Vegetarian')], validators=[DataRequired()])
    size_small_price = FloatField('Small Price', validators=[DataRequired()])
    size_medium_price = FloatField('Medium Price', validators=[DataRequired()])
    size_large_price = FloatField('Large Price', validators=[DataRequired()])
    image = FileField('Pizza Image', validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    is_available = BooleanField('Is Available')
    submit = SubmitField('Save Pizza')

class ToppingForm(FlaskForm):
    name = StringField('Topping Name', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    is_available = BooleanField('Is Available')
    submit = SubmitField('Save Topping')
