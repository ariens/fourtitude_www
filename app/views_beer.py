from flask import render_template
from app import app, route_restrictions
from .models import Beer


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
    return render_template(
        'beers/admin.html',
        title='Beer Management')