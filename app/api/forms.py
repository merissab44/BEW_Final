from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User,Restaurant

class DataForm(FlaskForm):
    location = StringField( "location", validators=[DataRequired()])
    submit = SubmitField("Enter")

class RestaurantForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    price_range = StringField("price range", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])
    submit = SubmitField("Add")