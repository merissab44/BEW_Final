from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

class DataForm(FlaskForm):
    location = StringField( "location", validators=[DataRequired()])
    submit = SubmitField("Enter")