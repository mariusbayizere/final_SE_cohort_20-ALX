# # from flask import Flask, session
# from flask import Flask, redirect, url_for, flash, session  # Add session here
# from datetime import timedelta
# from flask_migrate import Migrate
# from flask_login import LoginManager, current_user,logout_user
# from models import db
# import os

# app = Flask(__name__)

# # Configure the database
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:auca%402023@localhost/final_project_ALX'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Set the secret key for session management and CSRF protection
# app.config['SECRET_KEY'] = b'\xa1\xcb%\x96) \xb8\x97\x96,Hq\xe1\xf7Z\xf2\x13\x97\x8d6\xb3\x9c\x8bM'
# app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
# # Initialize the database with the Flask app
# db.init_app(app)

# migrate = Migrate(app, db)

# login_manager = LoginManager()
# login_manager.init_app(app)

# login_manager.login_view = 'user.login'

# @login_manager.user_loader
# def load_user(user_id):
#     from models.User import User  # Import here to avoid circular imports
#     return User.query.get(user_id)


# @app.before_request
# def check_session_timeout():
#     if current_user.is_authenticated and not session.get('permanent'):
#         # If the session is not permanent, log out the user
#         logout_user()
#         flash('Your session has expired. Please log in again.', 'warning')
#         return redirect(url_for('user.login'))

# # Initialize Flask-Migrate

# # Now that db is initialized, import models to ensure they are registered with Flask-SQLAlchemy
# from models.User import User
# from models.Books import Books
# from models.Borrowed import Borrow

# # Import and register the blueprint after initializing db and models
# from routes.user import user_bp
# from routes.Books import book_bp
# from routes.borrow import borrow_bp

# app.register_blueprint(user_bp)
# app.register_blueprint(book_bp)
# app.register_blueprint(borrow_bp)

# if __name__ == "__main__":
#     with app.app_context():
#         db.create_all()
#     app.run(debug=True)


# run.py
from flask import Flask, redirect, url_for, flash, session, current_app
from datetime import timedelta, datetime
from flask_migrate import Migrate
from flask_login import LoginManager, current_user, logout_user, login_user
from models import db
import os

app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:auca%402023@localhost/final_project_ALX'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Set the secret key for session management and CSRF protection
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_default_secret_key')  # Replace with environment variable
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)  # Set to desired timeout

# Initialize the database with the Flask app
db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'user.login'

@login_manager.user_loader
def load_user(user_id):
    from models.User import User  # Import here to avoid circular imports
    return db.session.get(User, user_id)

# Define mark_session_permanent once
def mark_session_permanent():
    session.permanent = True
    session['last_activity'] = datetime.utcnow().timestamp()

@app.before_request
def check_session_timeout():
    if current_user.is_authenticated:
        last_activity = session.get('last_activity')
        now = datetime.utcnow().timestamp()
        if last_activity:
            elapsed = now - last_activity
            if elapsed > app.config['PERMANENT_SESSION_LIFETIME'].total_seconds():
                logout_user()
                flash('Your session has expired. Please log in again.', 'warning')
                return redirect(url_for('user.login'))
        # Update last_activity time
        session['last_activity'] = now

# Import and register the blueprint after initializing db and models
from routes.user import user_bp
from routes.Books import book_bp
from routes.borrow import borrow_bp

app.register_blueprint(user_bp)
app.register_blueprint(book_bp)
app.register_blueprint(borrow_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)

