from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager
from application.threads.models import Thread
from application.threads.forms import ThreadForm, ThreadEditForm

from application.comments.forms import CommentForm
from application.comments.models import Comment

from application.categories.models import Category

@app.route("/threads/all", methods=["GET"])
def threads_index():
    return render_template("threads/list.html",
                            threads = Thread.query.all())

@app.route("/threads/all/<category_name>", methods=["GET"])
def threads_by_category(category_name):
    return render_template("threads/list.html",
                            threads = Thread.query.filter_by(category_name=category_name).all())

@app.route("/threads/<thread_id>")
def thread_show(thread_id):
    t = Thread.query.get(thread_id)
    comments = Comment.query.filter_by(thread_id=thread_id).all()
    form = ThreadEditForm()
    form.text.data = t.text

    return render_template("threads/one.html", thread = t, form = form, commentForm = CommentForm(), comments = comments)

@app.route("/threads/<thread_id>/", methods=["POST"])
@login_required()
def thread_edit(thread_id):
    form = ThreadEditForm(request.form)
    t = Thread.query.get(thread_id)

    if t.account_id != current_user.id:
        return login_manager.unauthorized()

    comments = Comment.query.filter_by(thread_id=thread_id).all()

    if not form.validate():
        return render_template("threads/one.html", thread = t, form = form, commentForm = CommentForm(), comments = comments)

    
    t.text = form.text.data
    db.session().commit()

    return redirect(url_for("thread_show", thread_id=t.id))


@app.route("/threads/new", methods=["GET", "POST"])
@login_required()
def threads_create():
    form = ThreadForm()
    form.category.choices = [(c.id, c.name) for c in Category.query.all()]

    if form.validate_on_submit():
        t = Thread(form.title.data, form.text.data)
        t.creator = current_user.username
        t.account_id = current_user.id
        t.category_id = form.category.data
        t.category_name = Category.query.filter_by(id = form.category.data).first().name
        db.session().add(t)
        db.session().commit()
        return redirect(url_for("threads_index"))
        
    return render_template("threads/new.html", form = form)



@app.route("/threads/delete/<thread_id>/", methods=["POST"])
@login_required()
def thread_delete(thread_id):
    t = Thread.query.get(thread_id)

    if t.account_id != current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    Comment.query.filter_by(thread_id = thread_id).delete()

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("threads_index"))

