from flask import render_template, redirect, url_for

from application import app, db, login_required
from application.categories.models import Category
from application.categories.forms import CategoryForm

@app.route("/category/new", methods=["GET", "POST"])
@login_required("ADMIN")
def category_create():
    form = CategoryForm()
    
    if form.validate_on_submit():
        c = Category(form.name.data)
        db.session().add(c)
        db.session().commit()
        
        return redirect(url_for("category_create"))
    
    categories = Category.query.all()

    return render_template("categories/new.html", form = form, categories = categories)