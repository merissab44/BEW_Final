from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User,Restaurant

class DataForm(FlaskForm):
    location = StringField( "location", validators=[DataRequired()])
    submit = SubmitField("Enter")

class RestaurantForm(FlaskForm):
    name = StringField("name", validators=[DataRequired()])
    price = StringField("price", validators=[DataRequired()])
    address = StringField("address", validators=[DataRequired()])
    submit = SubmitField("Add")

class ReviewForm(FlaskForm):
    title = StringField("title", validators=[DataRequired()])
    content = TextAreaField("message", validators=[DataRequired()])
    submit = SubmitField("Post")