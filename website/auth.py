from flask import Blueprint, request, render_template, redirect, url_for, flash, session
from .models import User
from . import db
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint('auth', __name__, template_folder="templates")

# Home
@auth.route("/home")
@auth.route("/")
def home():
    return render_template("index.html")

# Signup
@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":

        # Request data
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # Errors
        email_exists = User.query.filter_by(email=email).first()
        if email_exists:
            flash("Email already exists!", "danger")
        
        elif password1 != password2:
            flash("Passwords do not match!", "danger")

        # User creation
        else:
            password_hash = generate_password_hash(password1, method="sha256")
            user = User(email=email, username=username, password=password_hash)
            session[email] = password_hash
            db.session.add(user)
            db.session.commit()
            login_user(user, remember=True)
            flash("User Created!", "success")
            return redirect(url_for("auth.dashboard"))

    return render_template("signup.html")


# Login
@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        
        # If Email found
        if user:

            # Check for correct password
            if check_password_hash(user.password, password):
                flash("Signed In", "success")
                login_user(user, remember=True)
                return redirect(url_for("auth.dashboard"))
            else: 
                flash("Incorrect email or password!", "danger")
        else: 
            flash("Incorrect email or password!", "danger")

    return render_template("login.html")

# Logout
@auth.route("/logout", methods=["POST", "GET"])
def logout():
    logout_user()
    flash("Logged out!", "success")
    return redirect(url_for("auth.home"))

# Dashboard
@auth.route("/dashboard", methods=["POST", "GET"])
@login_required
def dashboard():
    return render_template("dashboard.html", username1 = current_user.username)
