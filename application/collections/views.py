from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager

from application.collections.forms import CollectionForm
from application.collections.models import Collection


@app.route("/collections/new", methods=["GET", "POST"])
@login_required()
def collections_create():
    form = CollectionForm()
    
    if form.validate_on_submit():
        c = Collection(form.name.data)
        c.description = form.description.data
        c.account_id = current_user.id

        db.session().add(c)
        db.session().commit()

        return redirect(url_for("user_profile", user_id = current_user.id))
    
    return render_template("collections/new.html", form = form)