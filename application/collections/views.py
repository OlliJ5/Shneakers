from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required, login_manager

from application.collections.forms import CollectionForm
from application.collections.models import Collection

from application.shoes.models import Shoe

from application.auth.models import User


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
    
    return render_template("collections/new.html", form = form,
                                                user = current_user.id)

@app.route("/collections/<user_id>", methods=["GET"])
def list_user_collections(user_id):
    u = User.query.get(user_id)

    collections = Collection.query.filter_by(account_id = user_id).all()

    return render_template("collections/list.html", user = u,
                                                    collections = collections)


@app.route("/collections/<user_id>/<collection_id>", methods=["GET"])
def collections_show_one(collection_id, user_id):
    u = User.query.get(user_id)
    c = Collection.query.get(collection_id)

    shoes = Shoe.query.filter_by(collection_id = collection_id).all()

    return render_template("collections/one.html", collection = c,
                                                  shoes = shoes,
                                                  user = u)