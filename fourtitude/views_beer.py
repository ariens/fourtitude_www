from flask import render_template, request, flash, redirect, url_for
from fourtitude import app, db, route_restrictions
from fourtitude.models import Beer, BeerStyle, BeerStyleType
from fourtitude.forms import ConfirmForm, BeerForm, BeerStyleForm, BeerStyleTypeForm


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

    verb = 'Create'
    if object_id is not None:
        verb = 'Update'
        managed_obj = ManagedClass.query.get(object_id)

    ManagedClassForm = auto_manage_registry[object_class]['class_form']
    form = ManagedClassForm(obj=managed_obj)

    try:
        if form.validate_on_submit():
            form.populate_obj(managed_obj)
            if hasattr(managed_obj, 'form_populate_helper'):
                managed_obj.form_populate_helper()
            db.session.add(managed_obj)
            db.session.commit()
            flash("Object: '%s' Saved!" % managed_obj.get_auto_manage_label())
            return redirect(url_for('beer_admin'))
    except Exception as error:
        flash(error)
    return render_template(
        ManagedClass.manage_template(),
        title="%s %s" % (verb, managed_obj.get_auto_manage_label()),
        form=form)

@app.route('/beer/delete/<object_class>/<int:object_id>', methods=['GET', 'POST'])
#@route_restrictions.restrict(group_name='beer_admin')
def delete_beer_object(object_class, object_id):
    """
    Associates a registry of managed object to their class name
    Displays a confirmation before deletion
    :param object_class: The class name of the managed object
    :param object_id: The object's id when editing existing
    :return: Rendered form when confirming, redirects upon commit
    :raise Exception: Any error
    """
    auto_manage_registry = {
        'BeerStyleType': {
            'class_name': BeerStyleType,
        },
        'BeerStyle': {
            'class_name': BeerStyle,
        },
        'Beer': {
            'class_name': Beer,
        }
    }

    if not object_class in auto_manage_registry:
        raise Exception("The object '%s' is not auto-managed" % object_class)

    ManagedClass = auto_manage_registry[object_class]['class_name']
    managed_obj = ManagedClass.query.get(object_id)

    try:
        form = ConfirmForm()
        if object_id is None:
            raise Exception("Missing object_id")

        if request.method == 'POST':
            flash(request.form['action'])
            #return redirect(url_for('beer_admin'))
    except Exception as error:
        flash(error)
    return render_template(
        ManagedClass.delete_template(),
        form=form,
        managed_obj=managed_obj,
        title="Please Confirm")
