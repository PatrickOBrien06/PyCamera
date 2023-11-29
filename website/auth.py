from flask import Blueprint, request, render_template, redirect, url_for, flash
from .models import User
from . import db
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
            user = User(email=email, password=password_hash)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))

    return render_template("signup.html")

# Login
@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":

        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if user:
            if check_password_hash(user.password, password):
                flash("Signed In", "success")
        else: 
            flash("Incorrect email or password", "danger")

    return render_template("login.html")


@auth.route("/dashboard/<user>", methods=["POST", "GET"])
def dashboard():
    pass
