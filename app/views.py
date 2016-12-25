from app import app, db
from .models import Restaurant, MenuItem
from .forms import DeleteForm, RestaurantForm, MenuForm
from flask import render_template, flash, redirect, request, url_for, jsonify


@app.route('/')
@app.route('/restaurants')
def restaurants():
    restaurants = Restaurant.query.all()
    menu_items = MenuItem.query.all()
    return render_template('restaurants.html',
                           restaurants=restaurants,
                           menu_items=menu_items)


@app.route('/restaurant/new', methods=['GET', 'POST'])
def new_restaurant():
    form = RestaurantForm()
    if request.method == "POST" and form.validate_on_submit():
        restaurant = Restaurant(name=request.form['name'])
        db.session.add(restaurant)
        db.session.commit()
        flash('You added {}'.format(request.form['name']))
        return redirect('/restaurants')
    return render_template('new_restaurant.html', form=form)


@app.route('/restaurant/<int:id>/edit', methods=['GET', 'POST'])
def edit_restaurant(id):
    form = RestaurantForm()
    restaurant = Restaurant.query.filter_by(id=id).first()
    old_restaurant_name = restaurant.name
    form.name.data = old_restaurant_name
    if request.method == "POST" and form.validate_on_submit():
        restaurant.name = request.form['name']
        db.session.commit()
        flash('Updated name from {0} to {1}'.format(old_restaurant_name,
                                                    restaurant.name))
        return redirect('/restaurants')
    return render_template('edit_restaurant.html',
                           form=form,
                           old_restaurant_name=old_restaurant_name)


@app.route('/restaurant/<int:id>/delete', methods=['GET', 'POST'])
def delete_restaurant(id):
    form = DeleteForm()
    restaurant = Restaurant.query.filter_by(id=id).first()
    restaurant_name = restaurant.name
    if request.method == "POST":
        db.session.delete(restaurant)
        db.session.commit()
        flash('Deleted {0}'.format(restaurant_name))
        return redirect('/restaurants')
    return render_template('delete_restaurant.html',
                           form=form,
                           restaurant_name=restaurant_name)


@app.route('/restaurant/<int:id>/menu')
def show_restaurant_menu(id):
    menu_items = MenuItem.query.filter_by(restaurant_id=id)
    appetizers = menu_items.filter_by(course="Appetizer").all()
    entrees = menu_items.filter_by(course="Entree").all()
    desserts = menu_items.filter_by(course="Dessert").all()
    beverages = menu_items.filter_by(course="Beverage").all()
    restaurant_name = Restaurant.query.filter_by(id=id).first().name
    return render_template('show_restaurant_menu.html',
                           appetizers=appetizers,
                           entrees=entrees,
                           desserts=desserts,
                           beverages=beverages,
                           restaurant_id=id,
                           restaurant_name=restaurant_name)


@app.route('/restaurant/<int:id>/menu/new', methods=['GET', 'POST'])
def new_menu_item(id):
    form = MenuForm()
    if request.method == "POST" and form.validate_on_submit():
        menu_item = MenuItem(name=request.form['name'],
                             description=request.form['description'],
                             price=request.form['price'],
                             course=request.form['course'],
                             restaurant=Restaurant.query.filter_by(id=id).first())
        db.session.add(menu_item)
        db.session.commit()
        flash('You created a new menu item!')
        return redirect(url_for('show_restaurant_menu',id=id))
    return render_template('new_menu_item.html',
                           form=form,
                           restaurant_id=id)


@app.route('/restaurant/<int:id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
def edit_menu_item(id, menu_id):
    form = MenuForm()
    menu_item = MenuItem.query.filter_by(restaurant_id=id).\
                                   filter_by(id=menu_id).first()
    if request.method == "GET":
        form.name.data = menu_item.name
        form.description.data = menu_item.description
        form.price.data = menu_item.price
        form.course.data = menu_item.course
    if request.method == "POST" and form.validate_on_submit():
        menu_item.name = request.form['name']
        menu_item.description = request.form['description']
        menu_item.price = request.form['price']
        menu_item.course = request.form['course']
        db.session.commit()
        flash('Updated the menu item!')
        return redirect('/restaurants')
    return render_template('edit_menu_item.html',
                           form=form,
                           restaurant_id=id)


@app.route('/restaurant/<int:id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
def delete_menu_item(id, menu_id):
    form = DeleteForm()
    if request.method == "POST":
        menu_item = MenuItem.query.filter_by(restaurant_id=id).\
                                   filter_by(id=menu_id).first()
        menu_item_name = menu_item.name
        db.session.delete(menu_item)
        db.session.commit()
        flash("You delete {} from the menu".format(menu_item_name))
        return redirect(url_for('show_restaurant_menu', id=id))
    return render_template('delete_menu_item.html',
                           form=form)


@app.route('/restaurants/JSON')
def restaurants_json():
    restaurants = Restaurant.query.all()
    return jsonify(Restaurants=[r.serialize for r in restaurants])


@app.route('/restaurant/<int:id>/menu/JSON')
def menu_json(id):
    menu_items = MenuItem.query.filter_by(restaurant_id=id)
    return jsonify(MenuItem=[m.serialize for m in menu_items])
