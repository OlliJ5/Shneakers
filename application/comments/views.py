from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager
from application.comments.models import Comment
from application.comments.forms import CommentForm

from application.threads.forms import ThreadForm
from application.threads.models import Thread

from application.auth.models import User

@app.route("/comments/<thread_id>", methods=["POST"])
@login_required()
def comment_post(thread_id):
    form = CommentForm(request.form)

    t = Thread.query.get(thread_id)
    comments = Comment.query.filter_by(thread_id=thread_id).all()

    if not form.validate():
        return render_template("threads/one.html", thread = t, form = ThreadForm(), commentForm = form, comments = comments)

    c = Comment(form.text.data)
    c.account_id = current_user.id
    c.thread_id = thread_id
    c.creator = current_user.username

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("thread_show", thread_id = thread_id))

@app.route("/comments/edit/<comment_id>")
@login_required()
def comment_editform(comment_id):
    c = Comment.query.get(comment_id)
    form = CommentForm()
    form.text.data = c.text

    return render_template("comments/edit.html", comment = c, form = form)

@app.route("/comment/edit/<comment_id>", methods=["POST"])
@login_required()
def comment_edit(comment_id):
    form = CommentForm(request.form)
    c = Comment.query.get(comment_id)

    if c.account_id != current_user.id:
        return login_manager.unauthorized()
    
    if not form.validate():
        return render_template("comments/edit.html", comment = c, form = form)

    c.text = form.text.data
    db.session().commit()

    return redirect(url_for("thread_show", thread_id=c.thread_id))

@app.route("/comments/users/<user_id>", methods=["GET"])
def comments_by_user(user_id):
    u = User.query.get(user_id)
    comments = Comment.query.filter_by(account_id = user_id).all()

    return render_template("comments/profileComments.html", user = u,
                                                        comments = comments)

@app.route("/comments/delete/<comment_id>", methods=["POST"])
@login_required()
def comment_delete(comment_id):
    c = Comment.query.get(comment_id)
    thread = c.thread_id

    if c.account_id != current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    db.session().delete(c)
    db.session().commit()

    return redirect(url_for("thread_show", thread_id=thread))
