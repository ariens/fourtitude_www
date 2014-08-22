from flask import render_template
from fourtitude import app, route_restrictions
from fourtitude.beer_forms import BeerForm, BeerStyleForm, BeerStyleTypeForm
from fourtitude.beer_models import Beer, BeerStyle, BeerStyleType
from fourtitude.managed_object import manage_object, delete_object


def get_beer_registry():
    return {
        'BeerStyleType': {
            'class_name': BeerStyleType,
            'class_form': BeerStyleTypeForm
        },
        'BeerStyle': {
            'class_name': BeerStyle,
            'class_form': BeerStyleForm
        },
        'Beer': {
            'class_name': Beer,
            'class_form': BeerForm
        }
    }


@app.route('/beer', methods=['GET', 'POST'])
def list_beers(admin=False):
    all_beers = Beer.query.all()
    all_styles = BeerStyle.query.all()
    all_style_types = BeerStyleType.query.all()
    return render_template(
        'beer/page.html',
        admin=admin,
            beers=all_beers,
        styles=all_styles,
        style_types=all_style_types,
        title='Beers')


@app.route('/beer/manage', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def beer_admin():
    return list_beers(admin=True)


@app.route('/beer/manage/<object_class>/', methods=['GET', 'POST'], defaults={'object_id': None})
@app.route('/beer/manage/<object_class>/<int:object_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def manage_beer_object(object_class, object_id):
    return manage_object(get_beer_registry(), object_class, object_id)


@app.route('/beer/delete/<object_class>/<int:object_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def delete_beer_object(object_class, object_id):
    return delete_object(get_beer_registry(), object_class, object_id)