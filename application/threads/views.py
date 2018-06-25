from flask import render_template, request, redirect, url_for
from flask_login import current_user

from sqlalchemy import desc

from application import app, db, login_required, login_manager
from application.threads.models import Thread
from application.threads.forms import ThreadForm, ThreadEditForm

from application.comments.forms import CommentForm
from application.comments.models import Comment

from application.categories.models import Category

from application.auth.models import User

from application.user_thread.models import UserThread

@app.route("/threads/<int:page_num>", methods=["GET"])
def threads_index(page_num):
    return render_template("threads/list.html",
                            threads = Thread.query
                                    .order_by(Thread.date_created.desc())
                                    .paginate(per_page=5, page=page_num, error_out=True),
                            categories = Category.query.all())

@app.route("/threads/oldest/<int:page_num>", methods=["GET"])
def threads_old(page_num):
    return render_template("threads/list.html",
                            threads = Thread.query
                                    .paginate(per_page=5, page=page_num, error_out=True),
                            categories = Category.query.all())   

@app.route("/threads/all/<category_name>/<int:page_num>", methods=["GET"])
def threads_by_category(category_name, page_num):
    return render_template("threads/list.html",
                            threads = Thread.query
                                            .filter_by(category_name=category_name)
                                            .order_by(Thread.date_created.desc())
                                            .paginate(per_page=5, page=page_num, error_out=True),
                            category = category_name,
                            categories = Category.query.all())

@app.route("/auth/users/<user_id>", methods=["GET"])
def user_profile(user_id):
    u = User.query.get(user_id)
    posts = Thread.query.filter_by(account_id = user_id).all()

    return render_template("threads/profileThreads.html", user = u,
                                                posts = posts)

@app.route("/threads/one/<thread_id>")
def thread_show(thread_id):
    t = Thread.query.get(thread_id)

    if t:
        user_thread = UserThread(thread_id)

        if current_user.is_authenticated:
            user_thread.account_id = current_user.id

        db.session().add(user_thread)
        db.session().commit()    

    comments = Comment.query.filter_by(thread_id=thread_id).all()
    comment_amount = Comment.threads_comments(thread_id)

    views = UserThread.how_many_viewers_a_thread_has(thread_id)
    unique_views = UserThread.how_many_unique_viewers_a_thread_has(thread_id)

    return render_template("threads/one.html", 
                            thread = t,
                            views = views,
                            unique_views=unique_views,
                            commentForm = CommentForm(),
                            comment_amount = comment_amount,
                            comments = comments)

@app.route("/thread/<thread_id>/edit")
def thread_editform(thread_id):
    t = Thread.query.get(thread_id)
    comments = Comment.query.filter_by(thread_id=thread_id).all()
    form = ThreadEditForm()
    form.text.data = t.text

    return render_template("threads/edit.html", thread = t, form = form)

@app.route("/threads/<thread_id>/edit", methods=["POST"])
@login_required()
def thread_edit(thread_id):
    form = ThreadEditForm(request.form)
    t = Thread.query.get(thread_id)

    if t.account_id != current_user.id:
        return login_manager.unauthorized()

    comments = Comment.query.filter_by(thread_id=thread_id).all()

    if not form.validate():
        return render_template("threads/edit.html", thread = t, form = form)

    
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
        
        return redirect(url_for("threads_index", page_num=1))
        
    return render_template("threads/new.html", form = form)



@app.route("/threads/delete/<thread_id>/", methods=["POST"])
@login_required()
def thread_delete(thread_id):
    t = Thread.query.get(thread_id)

    if t.account_id != current_user.id and current_user.role != "ADMIN":
        return login_manager.unauthorized()

    Comment.query.filter_by(thread_id = thread_id).delete()
    UserThread.query.filter_by(thread_id = thread_id).delete()

    db.session().delete(t)
    db.session().commit()

    return redirect(url_for("threads_index", page_num=1))

