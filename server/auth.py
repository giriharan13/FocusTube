from flask import Blueprint,render_template,redirect,url_for,jsonify,request,flash
from flask_login import login_user,login_required,logout_user
from .models import User
from .forms import LoginForm,SignUpForm
from . import login_manager

auth = Blueprint('auth',__name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

@auth.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            if(user.check_password_hash(form.password.data)):
                flash("Logged in successfully!")
                login_user(user)

                return redirect(url_for("main.home"))


        flash("Invalid Credentials")

    return render_template("login.html",form=form)



@auth.route('/signup')
def signup():
    form = SignUpForm()
    return render_template("signup.html",form=form)

@auth.route('/signup',methods=['POST'])
def signup_post():

    data = request.form

    user = User.query.filter_by(username=data.get('username')).first()

    if user is not None:
        flash("Username already taken!")
        return redirect(url_for('auth.signup'))
    
    if data.get('password') != data.get('confirm_password'):
        flash("Both passwords must match!")
        return redirect(url_for('auth.signup'))
    

    new_user = User(
        username = data['username']
    )

    new_user.set_password(data.get('password'))

    new_user.save()
    
    flash("User created!")
    return redirect(url_for("auth.login"))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))