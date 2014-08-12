from flask import render_template, flash, redirect, url_for
from app import app, db, route_restrictions
from app.models import Beer, BeerStyle, BeerStyleType
from app.forms import BeerStyleForm, BeerStyleTypeForm

@app.route('/beers', methods=['GET', 'POST'])
def beers():
    """
    This is the route that a user accesses when viewing beers
    :return:
    """
    all_beers = Beer.query.all()
    return render_template(
        'beers/page.html',
        beers=all_beers,
        title='Beers')


@app.route('/beers/admin', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def beer_admin():
    """
    This is the route that a beer admin accesses when managing beers
    :return:
    """
    all_beers = Beer.query.all()
    all_styles = BeerStyle.query.all()
    all_style_types = BeerStyleType.query.all()
    return render_template(
        'beers/page.html',
        admin=True,
        beers=all_beers,
        styles=all_styles,
        style_types=all_style_types,
        title='Beer Management')

@app.route('/beers/new_style', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def new_style():
    problem = None
    form = BeerStyleForm()
    try:
        if form.validate_on_submit():
            style = BeerStyle()
    except Exception as error:
        flash(error)
    return render_template(
        'beers/page_new_style.html',
        problem=problem,
        title='Add A New Style',
        form=form)


@app.route('/beers/new_style_type', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def new_style_type():
    problem = None
    form = BeerStyleTypeForm()
    try:
        if form.validate_on_submit():
            style_type = BeerStyleType(name=form.name.data)
            db.session.add(style_type)
            db.session.commit()
            flash("New Style Type: '" + style_type.name + "' added!")
            return redirect(url_for('beer_admin'))
    except Exception as error:
        flash(error)
    return render_template(
        'beers/page_new_style_type.html',
        problem=problem,
        title='Add A New Style Type',
        form=form)