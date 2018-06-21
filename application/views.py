from flask import render_template
from application import app, login_required
from application.auth.models import User

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/statistics")
def statistics():
    return render_template("statistics.html",
                            leading_posters = User.top_five_posters_and_amount_of_posts(),
                            leading_commenters = User.top_five_commenters_and_amount_of_comments())

@app.route("/admin")
@login_required("ADMIN")
def admin_view():
    return render_template("admin.html")