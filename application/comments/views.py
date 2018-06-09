from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.comments.models import Comment
from application.comments.forms import CommentForm

from application.threads.forms import ThreadForm
from application.threads.models import Thread

@app.route("/comments/<thread_id>", methods=["POST"])
@login_required
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