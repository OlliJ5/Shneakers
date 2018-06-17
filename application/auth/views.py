from flask import render_template, request, redirect, url_for
from flask_login import login_user, logout_user, current_user

from application import app, db, login_required
from application.auth.models import User
from application.auth.forms import LoginForm, UserForm

from application.comments.models import Comment
from application.threads.models import Thread

@app.route("/auth/login", methods = ["GET", "POST"])
def auth_login():
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())

    form = LoginForm(request.form)

    user = User.query.filter_by(username=form.username.data, password=form.password.data).first()
    if not user:
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
    return render_template("auth/new.html", form = UserForm())


@app.route("/auth/", methods = ["POST"])
def auth_create():
    form = UserForm(request.form)

    if not form.validate():
        return render_template("auth/new.html", form = form)

    u = User(form.name.data, form.username.data, form.password.data, "NORMAL")

    db.session().add(u)
    db.session().commit()
    
    return redirect(url_for("auth_login"))

@app.route("/auth/create/admin", methods = ["GET", "POST"])
@login_required("ADMIN")
def auth_create_admin():
    form = UserForm()
    
    if form.validate_on_submit():
        u = User(form.name.data, form.username.data, form.password.data, "ADMIN")

        db.session().add(u)
        db.session().commit()

        return redirect(url_for("auth_create_admin"))
    
    return render_template("auth/newAdmin.html", form = form)

@app.route("/auth/users", methods=["GET"])
@login_required("ADMIN")
def auth_show_users():
    return render_template("auth/list.html", users = User.query.all())

@app.route("/auth/delete/<user_id>", methods=["POST"])
@login_required()
def user_delete(user_id):
    u = User.query.get(user_id)

    if current_user.role != "ADMIN":
        return login_manager.unauthorized()
    
    Comment.query.filter_by(account_id = user_id).delete()
    Thread.query.filter_by(account_id = user_id).delete()

    db.session().delete(u)
    db.session().commit()

    return redirect(url_for("auth_show_users"))