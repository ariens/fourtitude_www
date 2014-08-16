from flask import render_template, flash, redirect, url_for
from fourtitude import app, db, route_restrictions
from fourtitude.models import Beer, BeerStyle, BeerStyleType
from fourtitude.forms import BeerForm, BeerStyleForm, BeerStyleTypeForm


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


@app.route('/beer/manage', methods=['GET', 'POST'])
#@route_restrictions.restrict(group_name='beer_admin')
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


@app.route('/beer/manage/<object_class>/', methods=['GET', 'POST'], defaults={'object_id': None})
@app.route('/beer/manage/<object_class>/<int:object_id>', methods=['GET', 'POST'])
#@route_restrictions.restrict(group_name='beer_admin')
def manage_beer_object(object_class, object_id):
    """
    Associates a registry of managed object to their class name and form name
    When an object_id is specified the existing object's form is presented for editing
    When no object_id is specified a blank form is presented for creating a new object
    :param object_class: The class name of the managed object
    :param object_id: The object's id when editing existing
    :return: Rendered form when editing/creating, redirects upon commit
    :raise Exception: Any error
    """
    auto_manage_registry = {
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

    if not object_class in auto_manage_registry:
        raise Exception("The object '%s' is not auto-managed" % object_class)

    ManagedClass = auto_manage_registry[object_class]['class_name']
    managed_obj = ManagedClass()

    if object_id is not None:
        managed_obj = ManagedClass.query.get(object_id)

    ManagedClassForm = auto_manage_registry[object_class]['class_form']
    form = ManagedClassForm(obj=managed_obj)

    try:
        if form.validate_on_submit():
            form.populate_obj(managed_obj)
            print("date_brewed val: %s date_brewed type: %s" % (managed_obj.date_brewed, managed_obj.date_brewed.__class__))
            if hasattr(managed_obj, 'form_populate_helper'):
                managed_obj.form_populate_helper()
            print("after helper call")
            db.session.add(managed_obj)
            db.session.commit()
            flash("Object: '%s' Saved!" % managed_obj.get_auto_manage_label())
            return redirect(url_for('beer_admin'))
    except Exception as error:
        flash(error)
    return render_template(
        ManagedClass.get_template(),
        title=managed_obj.get_auto_manage_title(),
        form=form)

@app.route('/beer/delete/style_type/<int:style_type_id>', methods=['GET', 'POST'])
@route_restrictions.restrict(group_name='beer_admin')
def delete_style_type(style_type_id):
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