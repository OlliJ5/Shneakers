from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager

from application.shoes.models import Shoe
from application.shoes.forms import ShoeForm

from application.collections.models import Collection

@app.route("/shoes/new", methods=["GET", "POST"])
@login_required()
def shoes_new():
    form = ShoeForm()
    form.collection.choices = [(c.id, c.name) for c in Collection.query.filter_by(account_id = current_user.id)]

    if form.validate_on_submit():
        s = Shoe(form.model.data, form.brand.data, form.release_year.data)
        s.collection_id = form.collection.data

        db.session().add(s)
        db.session().commit()

        return redirect(url_for("user_profile", user_id = current_user.id))

    return render_template("shoes/new.html", form = form)