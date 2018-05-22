from application import app
from flask import render_template, request

@app.route("/threads/new")
def thread_form():
    return render_template("threads/new.html")

@app.route("/threads/", methods=["POST"])
def threads_create():
    print(request.form.get("title"))

    return "hello world"