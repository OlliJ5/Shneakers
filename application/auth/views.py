from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required, bcrypt
from application.auth.models import User
from application.auth.forms import LoginForm, UserForm

from application.comments.models import Comment
from application.threads.models import Thread

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data).first()
    if not user or not bcrypt.check_password_hash(user.password, form.password.data):
        return render_template("auth/loginform.html", form = form,
                               error = "No such username or password")


    login_user(user)
    return redirect(url_for("index"))

@app.route("/auth/logout")
def auth_logout():
    logout_user()
    return redirect(url_for("index")) 


@app.route("/auth/create", methods = ["GET"])
def auth_form():
    return render_template("auth/new.html", form = UserForm(), userType="NORMAL")


@app.route("/auth/", methods = ["POST"])
def auth_create():
    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form = form)

    pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
    u = User(form.name.data, form.username.data, pw_hash, "NORMAL")

    db.session().add(u)
    db.session().commit()
    
    return redirect(url_for("auth_login"))

@app.route("/auth/create/admin", methods = ["GET", "POST"])
@login_required("ADMIN")
def auth_create_admin():
    form = UserForm()
    
    if form.validate_on_submit():
        pw_hash = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        u = User(form.name.data, form.username.data, pw_hash, "ADMIN")

        db.session().add(u)
        db.session().commit()

        return redirect(url_for("auth_create_admin"))
    
    return render_template("auth/new.html", form = form, userType= "ADMIN")

@app.route("/auth/users", methods=["GET"])
@login_required("ADMIN")
def auth_show_users():
    return render_template("auth/list.html", users = User.query.all())

@app.route("/auth/users/<user_id>", methods=["GET"])
def user_profile(user_id):
    u = User.query.get(user_id)

    return render_template("auth/profile.html", user = u)

@app.route("/auth/delete/<user_id>", methods=["POST"])
@login_required()
def user_delete(user_id):
    u = User.query.get(user_id)

    if current_user.role != "ADMIN":
        return login_manager.unauthorized()
    
    Comment.query.filter_by(account_id = user_id).delete()

    threads = Thread.query.filter_by(account_id = user_id).all()

    for thread in threads:
        Comment.query.filter_by(thread_id = thread.id).delete()

    Thread.query.filter_by(account_id = user_id).delete()

    db.session().delete(u)
    db.session().commit()

    return redirect(url_for("auth_show_users"))