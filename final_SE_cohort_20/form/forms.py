# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, DateField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Length, Email, Optional, ValidationError, EqualTo
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp, URL, ValidationError
from models.User import User
from datetime import date

# User Form
class UserForm(FlaskForm):
    # user_id = StringField('User ID', validators=[DataRequired(), Length(max=8)], render_kw={'readonly': True})
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=8)])
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    userrole = SelectField('User Role', choices=[('admin', 'Admin'), ('user', 'User')])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message='Passwords must match.')
    ])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

    def __init__(self, original_email=None, original_user_id=None,original_phone_number=None, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
        self.original_phone_number = original_phone_number
        self.original_user_id = original_user_id

    def validate_email(self, field):
        if field.data != self.original_email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email is already in use.')

    def validate_phone_number(self, field):
        if field.data != self.original_phone_number:
            if User.query.filter_by(phone_number=field.data).first():
                raise ValidationError('Phone number is already in use.')
    
    def validate_user_id(self, field):
        if field.data != self.original_user_id:
            if User.query.filter_by(user_id=field.data).first():
                raise ValidationError('This ID is already in use.')

class UpdateUserForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=8)], render_kw={'readonly': True})
    firstname = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    lastname = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    email = StringField('Email', validators=[DataRequired(), Email(), Length(max=100)])
    address = StringField('Address', validators=[DataRequired(), Length(max=255)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Update')

    def __init__(self, original_email=None, original_phone_number=None, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)
        self.original_email = original_email
        self.original_phone_number = original_phone_number

    def validate_email(self, field):
        if field.data != self.original_email:
            if User.query.filter_by(email=field.data).first():
                raise ValidationError('Email is already in use.')

    def validate_phone_number(self, field):
        if field.data != self.original_phone_number:
            if User.query.filter_by(phone_number=field.data).first():
                raise ValidationError('Phone number is already in use.')


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=8, max=255)])
    confirm_password = PasswordField('Confirm New Password', validators=[
        DataRequired(),
        EqualTo('new_password', message='Passwords must match.')
    ])
    submit = SubmitField('Update Password')
    


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


# class BookForm(FlaskForm):
#     book_id = StringField('Book ID', validators=[DataRequired(), Length(max=8)])
#     title = StringField('Title', validators=[DataRequired(), Length(max=255)])
#     Rating = IntegerField('Rating', validators=[Optional()])
#     BookImages = StringField('Book Images', validators=[DataRequired(), Length(max=255)])
#     author = StringField('Author', validators=[DataRequired(), Length(max=255)])
#     publication_year = StringField('Publication Year', validators=[DataRequired(), Length(max=10)])
#     Description = StringField('Description', validators=[DataRequired(), Length(max=255)])
#     page = IntegerField('Pages', validators=[DataRequired()])
#     # book_status = SelectField('Status', choices=[('available', 'Available'), ('borrowed', 'Borrowed')])
#     user_id = StringField('User ID (if borrowed)', validators=[Length(max=8)])
#     submit = SubmitField('Submit')

class BookForm(FlaskForm):
    # Book ID must be alphanumeric and max 8 characters
    book_id = StringField('Book ID', validators=[
        DataRequired(), 
        Length(max=8), 
        Regexp('^[A-Za-z0-9]+$', message="Book ID must be alphanumeric")
    ])
    
    # Title is required and has a max length of 255
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    
    # Rating is optional, but if provided it must be between 1 and 5
    Rating = IntegerField('Rating', validators=[Optional(), NumberRange(min=1, max=5, message="Rating must be between 1 and 5")])
    
    # Book Images is required and should be a valid URL (or filepath)
    BookImages = StringField('Book Images', validators=[
        DataRequired() ])
    
    # Author is required and has a max length of 255
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    
    # Publication year must be a valid 4-digit year
    publication_year = StringField('Publication Year', validators=[
        DataRequired(), 
        Regexp('^\d{4}$', message="Publication year must be a valid 4-digit year")
    ])
    
    # Description is required and max 255 characters
    Description = StringField('Description', validators=[DataRequired(), Length(max=255)])
    
    # Pages must be a positive integer
    page = IntegerField('Pages', validators=[DataRequired(), NumberRange(min=1, message="Pages must be greater than 0")])
    
    # User ID is optional but if provided must be alphanumeric and max 8 characters
    user_id = StringField('User ID (if borrowed)', validators=[
        Optional(), 
        Length(max=8), 
        Regexp('^[A-Za-z0-9]+$', message="User ID must be alphanumeric")
    ])
    
    submit = SubmitField('Submit')

def validate_book_id(self, field):
        book = Books.query.filter_by(book_id=field.data).first()
        if book:
            raise ValidationError('Book ID already exists. Please use a different ID.')

class UpdateBookForm(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired(), Length(max=8)], render_kw={'readonly': True})
    title = StringField('Title', validators=[DataRequired(), Length(max=255)])
    BookImages = StringField('Book Images', validators=[DataRequired(), Length(max=255)])
    author = StringField('Author', validators=[DataRequired(), Length(max=255)])
    publication_year = StringField('Publication Year', validators=[DataRequired(), Length(max=10)])
    page = IntegerField('Pages', validators=[DataRequired()])
    book_status = SelectField('Status', choices=[('available', 'Available'), ('borrowed', 'Borrowed')])
    user_id = StringField('User ID (if borrowed)', validators=[Length(max=8)])
    submit = SubmitField('Update')

class BorrowForm(FlaskForm):
    book_id = StringField('Book ID', validators=[DataRequired(), Length(max=8)])
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=8)])
    borrow_date = DateField('Borrow Date', validators=[DataRequired()])
    return_date = DateField('Return Date', validators=[DataRequired()])
    # fine = IntegerField('Fine', validators=[DataRequired()])
    fine = IntegerField('Fine', validators=[Optional()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Returned', 'Returned')])
    submit = SubmitField('Submit')
    
    def validate_borrow_date(form, field):
        if field.data < date.today():
            raise ValidationError('Borrow date cannot be in the past.')

    # Custom validator to check if the return date is in the past or before the borrow date
    def validate_return_date(form, field):
        if field.data < form.borrow_date.data:
            raise ValidationError('Return date cannot be before the borrow date.')
        if field.data < date.today():
            raise ValidationError('Return date cannot be in the past.')

    # Custom validator to check if the fine is paid on a valid date (e.g., in the future)
    def validate_fine(form, field):
        if form.return_date.data < date.today():
            raise ValidationError('Fine cannot be paid for a return date in the past.')
        
    def validate_user_id(form, field):
        user = User.query.filter_by(user_id=field.data).first()  # Query to check if user exists
        if not user:
            raise ValidationError('User not found. Please enter a valid User ID.')
    
class UpdateBorrowForm(FlaskForm):
    # ID = IntegerField('ID', validators=[DataRequired(), Length(max=8)], render_kw={'readonly': True})
    book_id = StringField('Book ID', validators=[DataRequired(), Length(max=8)])
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=8)])
    borrow_date = DateField('Borrow Date', validators=[DataRequired()])
    return_date = DateField('Return Date', validators=[DataRequired()])
    # fine = IntegerField('Fine', validators=[DataRequired()])
    fine = IntegerField('Fine', validators=[Optional()])
    status = SelectField('Status', choices=[('Pending', 'Pending'), ('Returned', 'Returned')])
    submit = SubmitField('Update')
    
    def validate_borrow_date(form, field):
        if field.data < date.today():
            raise ValidationError('Borrow date cannot be in the past.')

    # Custom validator to check if the return date is in the past or before the borrow date
    def validate_return_date(form, field):
        if field.data < form.borrow_date.data:
            raise ValidationError('Return date cannot be before the borrow date.')
        if field.data < date.today():
            raise ValidationError('Return date cannot be in the past.')

    # Custom validator to check if the fine is paid on a valid date (e.g., in the future)
    def validate_fine(form, field):
        if form.return_date.data < date.today():
            raise ValidationError('Fine cannot be paid for a return date in the past.')
        
    def validate_user_id(form, field):
        user = User.query.filter_by(user_id=field.data).first()  # Query to check if user exists
        if not user:
            raise ValidationError('User not found. Please enter a valid User ID.')
    
    
class ReturnForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired(), Length(max=8)])
    books_to_return = SelectMultipleField('Select Books to Return', choices=[], validators=[DataRequired()])
    submit = SubmitField('Return Books')

