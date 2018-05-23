from application import app, db
from flask import render_template, request, redirect, url_for
from application.threads.models import Thread

@app.route("/threads", methods=["GET"])
def threads_index():
    return render_template("threads/list.html", threads = Thread.query.all())

@app.route("/threads/new")
def thread_form():
    return render_template("threads/new.html")

@app.route("/threads/<thread_id>")
def thread_show(thread_id):
    t = Thread.query.get(thread_id)
    return render_template("threads/one.html", thread = t)

@app.route("/threads/<thread_id>/", methods=["POST"])
def thread_edit(thread_id):
    t = Thread.query.get(thread_id)
    
    t.text = request.form.get("text")
    t.date_modified = db.func.current_timestamp()
    db.session().commit()

    return redirect(url_for("thread_show", thread_id=t.id))


@app.route("/threads/", methods=["POST"])
def threads_create():
    t = Thread(request.form.get("title"), request.form.get("text"))

    db.session().add(t)
    db.session().commit()

    return redirect(url_for("threads_index"))