from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager
from application.comments.models import Comment
from application.comments.forms import CommentForm

from application.threads.forms import ThreadForm
from application.threads.models import Thread

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

@app.route("/comments/delete/<comment_id>", methods=["POST"])
@login_required()
def comment_delete(comment_id):
    c = Comment.query.get(comment_id)

    if c.account_id != current_user.id:
        return login_manager.unauthorized()

    Comment.query.filter_by(id = comment_id).delete()

    db.session().delete(c)
    db.session().commit()

    return redirect(url_for("threads_index"))
