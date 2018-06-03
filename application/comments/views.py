from flask import render_template, request, redirect, url_for
from flask_login import login_required, current_user

from application import app, db
from application.comments.models import Comment
from application.comments.forms import CommentForm

@app.route("/comments/<thread_id>", methods=["POST"])
@login_required
def comment_post(thread_id):
    form = CommentForm(request.form)

    c = Comment(form.text.data)
    c.account_id = current_user.id
    c.thread_id = thread_id

    db.session().add(c)
    db.session().commit()

    return redirect(url_for("thread_show", thread_id = thread_id))