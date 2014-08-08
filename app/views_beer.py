from flask import render_template
from app import app
from .models import Beer

@app.route('/beers', methods=['GET', 'POST'])
def beers():
    """
    This is the route that a user accesses when viewing/managing beers
    :return:
    """
    beers = Beer.query.all()
    return render_template(
        'beers.html',
        beers=beers,
        title='Beers')