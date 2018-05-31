from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db
from application.threads.models import Thread
from application.threads.forms import ThreadForm

@app.route("/threads", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads = Thread.query.all())

@app.route("/threads/new")
@login_required
def thread_form():
    return render_template("threads/new.html", form = ThreadForm())

@app.route("/threads/<thread_id>")
def thread_show(thread_id):
    t = Thread.query.get(thread_id)
    return render_template("threads/one.html", thread = t)

@app.route("/threads/<thread_id>/", methods=["POST"])
@login_required
def thread_edit(thread_id):
    t = Thread.query.get(thread_id)
    
    t.text = request.form.get("text")
    t.date_modified = db.func.current_timestamp()
    db.session().commit()

    return redirect(url_for("thread_show", thread_id=t.id))


@app.route("/threads/", methods=["POST"])
@login_required
def threads_create():
    form = ThreadForm(request.form)

    if not form.validate():
        return render_template("threads/new.html", form = form)
    
    t = Thread(form.title.data, form.text.data)

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("threads_index"))