from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from .models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators = [DataRequired(), Length(min=3, max=20)])
    email = StringField('Email',validators = [DataRequired(), Email()])
    password = PasswordField('Password', validators = [DataRequired(),Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    '''these userdefined calidate methods are automatically called when 
    form.validateonsubmit runs and if any error is raised then page rerenders 
    and if its valid then only user is created '''
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken')
        
    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already in use')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class JournalEntryForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=200)])
    content = TextAreaField('Content', validators=[DataRequired()])
    severity = SelectField('severity',choices=[('Low','Low'), ('Medium', 'Medium'), ('High', 'High')],
                           validators=[DataRequired()])#(value, label)
    
    submit = SubmitField('Save Entry')

class MedicationForm(FlaskForm):
    name = StringField('Medication Name',validators=[DataRequired()])
    dosage = StringField('Dosage')
    frequency = StringField('Frequency (e.g., Twice a day)')
    notes = TextAreaField('Notes (Optional)')
    submit = SubmitField('Save Medication')
    