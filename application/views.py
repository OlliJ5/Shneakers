from flask import render_template
from application import app
from application.auth.models import User

@app.route("/")
def index():
    return render_template("index.html", leading_posters=User.find_how_many_tasks_each_user_has())