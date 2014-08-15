from flask import render_template, flash, redirect, url_for
from app import app, db, route_restrictions
from app.models import Beer, BeerStyle, BeerStyleType
from app.forms import BeerStyleForm, BeerStyleTypeForm


@app.route('/beer', methods=['GET', 'POST'])
def beers():
    all_beers = Beer.query.all()
    all_styles = BeerStyle.query.all()
    all_style_types = BeerStyleType.query.all()
    return render_template(
        'beer/page.html',
        beers=all_beers,
        styles=all_styles,
        style_types=all_style_types,
        title='Beers')


@app.route('/beer/admin', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def beer_admin():
    all_beers = Beer.query.all()
    all_styles = BeerStyle.query.all()
    all_style_types = BeerStyleType.query.all()
    return render_template(
        'beer/page.html',
        admin=True,
        beers=all_beers,
        styles=all_styles,
        style_types=all_style_types,
        title='Beer Management')


@app.route('/beer/new_style', methods=['GET', 'POST'])
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
        'beer/page_new_style.html',
        problem=problem,
        title='Add A New Style',
        form=form)


@app.route('/beer/edit/style/', methods=['GET', 'POST'], defaults={'style_type_id': None})
@app.route('/beer/edit/style/<int:style_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def edit_style(style_id):
    problem = None
    form = BeerStyleForm()
    if style_id is None:
        style = BeerStyle()
    else:
        style = BeerStyle.query.get(style_id)
    try:
        if form.validate_on_submit():
            style.name = form.name.data
            style.style_type = form.style_type.data
            style.description = form.description.data
            style.link_beeradvocate = form.link_beeradvocate.data
            style.link_ratebeer = form.link_ratebeer.data
            db.session.add(style)
            db.session.commit()
            flash("Style: '" + style.name + "' Saved!")
            return redirect(url_for('beer_admin'))
        else:
            form.name.data = style.name
            form.description.data = style.description
            form.link_beeradvocate.data = style.link_beeradvocate
            form.link_ratebeer.data = style.link_ratebeer
            form.style_type.data = style.style_type
    except Exception as error:
        print(error)
        flash(error)
    return render_template(
        'beer/page_new_style.html',
        problem=problem,
        title='Edit Style',
        form=form)


@app.route('/beer/edit/style_type/', methods=['GET', 'POST'], defaults={'style_type_id': None})
@app.route('/beer/edit/style_type/<int:style_type_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def edit_style_type(style_type_id):
    problem = None
    form = BeerStyleTypeForm()
    if style_type_id is None:
        style_type = BeerStyleType()
    else:
        style_type = BeerStyleType.query.get(style_type_id)
    try:
        if form.validate_on_submit():
            style_type.name = form.name.data
            db.session.add(style_type)
            db.session.commit()
            flash("Style Type: '" + style_type.name + "' Saved!")
            return redirect(url_for('beer_admin'))
        else:
            form.name.data = style_type.name
    except Exception as error:
        flash(error)
    return render_template(
        'beer/page_new_style_type.html',
        problem=problem,
        title='Add A New Style Type',
        form=form)