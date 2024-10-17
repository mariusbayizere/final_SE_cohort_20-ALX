# routes/user.py
# routes/user.py

# from flask import Blueprint, render_template, request, redirect, url_for, flash, session
# from flask_login import current_user, login_user, logout_user, login_required
# from werkzeug.security import check_password_hash
# from form.forms import UserForm, LoginForm, UpdateUserForm
# from models.User import User
# from models import db
# from bcrypt import hashpw, gensalt, checkpw

# user_bp = Blueprint('user', __name__)

# @user_bp.route('/add_user', methods=['GET', 'POST'])
# def add_user():
#     form = UserForm()
#     if form.validate_on_submit():
#         hashed_password = hashpw(form.password.data.encode('utf-8'), gensalt()).decode('utf-8')

#         new_user = User(
#             user_id=form.user_id.data,
#             firstname=form.firstname.data,
#             lastname=form.lastname.data,
#             email=form.email.data,
#             UserRole=form.userrole.data,
#             password=hashed_password,
#             address=form.address.data,
#             phone_number=form.phone_number.data
#         )

#         db.session.add(new_user)
#         try:
#             db.session.commit()
#             flash('User added successfully!', 'success')
#             return redirect(url_for('user.login'))
#         except Exception as e:
#             db.session.rollback()
#             flash(f'Error adding user: {str(e)}', 'danger')

#     return render_template('add_user.html', form=form)

# @user_bp.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('user.dashboard'))

#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         if user and checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
#             login_user(user)
#             flash('Login successful', 'success')

#             session.permanent = True  # Make session permanent for timeout
#             if user.UserRole == 'admin':
#                 return redirect(url_for('user.dashboard'))
#             elif user.UserRole == 'user':
#                 return redirect(url_for('user.view_all_users'))
#         else:
#             flash('Invalid email or password', 'danger')

#     return render_template('login.html', form=form)

# @user_bp.route('/dashboard')
# @login_required
# def dashboard():
#     return render_template('all_books.html', name=current_user.firstname)







# user.py
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from form.forms import UserForm, LoginForm, UpdatePasswordForm
from models.User import User
from datetime import timedelta
from datetime import datetime
from models import db
from form.forms import UpdateUserForm
from bcrypt import hashpw, gensalt, checkpw

user_bp = Blueprint('user', __name__)

@user_bp.route('/add_user', methods=['GET', 'POST'])
def add_user():
    form = UserForm()
    if form.validate_on_submit():
        print("Form is valid")
        hashed_password = hashpw(form.password.data.encode('utf-8'), gensalt()).decode('utf-8')  # Use bcrypt for hashing
        print(hashed_password)

        new_user = User(
            user_id=form.user_id.data,
            firstname=form.firstname.data,
            lastname=form.lastname.data,
            email=form.email.data,
            UserRole=form.userrole.data,
            password=hashed_password,
            address=form.address.data,
            phone_number=form.phone_number.data
        )
        print(f'Adding user: {new_user}')
        db.session.add(new_user)
        try:
            db.session.commit()
            flash('User added successfully!', 'success')
            return redirect(url_for('user.login'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error adding user: {str(e)}', 'danger')
            print(f'Error adding user: {str(e)}')
    else:
        print("Form errors:", form.errors)

    return render_template('add_user.html', form=form)

def mark_session_permanent():
    session.permanent = True
    session['last_activity'] = datetime.utcnow().timestamp()


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('user.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        print(f"User found: {user}")
        if user:
            print(f"User password hash: {user.password}")

        if user and checkpw(form.password.data.encode('utf-8'), user.password.encode('utf-8')):
            login_user(user)
            mark_session_permanent()  # Mark session as permanent and set last_activity
            print(f"Current user authenticated: {current_user.is_authenticated}")
            flash('Login successful', 'success')

            # Redirect based on user role
            if user.UserRole == 'admin':
                return redirect(url_for('user.dashboard'))
            elif user.UserRole == 'user':
                return redirect(url_for('book.all_books'))
        else:
            print("Invalid credentials")
            flash('Invalid email or password', 'danger')

    return render_template('login.html', form=form)


@user_bp.route('/update_password', methods=['GET', 'POST'])
@login_required
def update_password():
    form = UpdatePasswordForm()
    
    if request.method == 'POST' and form.validate_on_submit():
        # Get the currently logged-in user's email
        email = current_user.email
        user = User.query.filter_by(email=email).first()

        if user:
            # Check if the entered current password matches the stored password hash
            if check_password_hash(user.password, form.current_password.data):
                # Hash the new password and update it in the database
                user.password = generate_password_hash(form.new_password.data)
                db.session.commit()
                
                flash('Your password has been updated successfully!', 'success')
                return redirect(url_for('login'))  # Redirect to profile or any other page after success
            else:
                flash('Incorrect current password.', 'danger')
        else:
            flash('User not found.', 'danger')
    
    return render_template('update_password.html', form=form)


@user_bp.route('/dashboard')
@login_required
def dashboard():
    # eturn render_template('dashboard.html', name=current_user.firstname)
    return render_template('admin_dashboard.html')

@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('user.login'))

@user_bp.route('/admin')
@login_required
def admin():
    if current_user.userrole != 'admin':
        flash('You do not have permission to access this page', 'danger')
        return redirect(url_for('user.dashboard'))
    return render_template('admin.html')


@user_bp.route('/update_user/<string:id>', methods=['GET', 'POST'])
def update_user(id):
    user = User.query.get(id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('user.add_user'))
    
    form = UpdateUserForm(
        original_email=user.email,
        original_phone_number=user.phone_number,
        obj=user
    )

    if form.validate_on_submit():
        form.populate_obj(user)
        
        try:
            db.session.commit()
            flash('User updated successfully!', 'success')
            return redirect(url_for('user.update_user', id=id))
        except Exception as e:
            db.session.rollback()
            flash(f'Error updating user: {e}', 'danger')

    return render_template('update_user.html', form=form, user=user)


@user_bp.route('/delete_user/<string:id>', methods=['POST'])
def delete_user(id):
    user = User.query.get(id)
    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('user.view_all_users'))
    
    db.session.delete(user)
    try:
        db.session.commit()
        flash('User deleted successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Error deleting user: {}'.format(e), 'danger')
    
    return redirect(url_for('user.view_all_users'))


@user_bp.route('/view_all_users', methods=['GET'])
def view_all_users():
    users = User.query.all()
    return render_template('view_all_users.html', users=users)

@user_bp.route('/header')
@login_required
def header():
    return render_template('all_books.html')

@user_bp.route('/about')
@login_required
def about():
    return render_template('about.html')

@user_bp.route('/contact')
@login_required
def contact():
    return render_template('contact.html')

@user_bp.route('/services')
@login_required
def services():
    return render_template('services.html')