from flask import render_template, request, flash, redirect, url_for
from fourtitude import db
from fourtitude.user_forms import ConfirmForm


class ManagedObjectException(Exception):
    pass


class ForeignKeyDependency(Exception):
    pass


class ManagedObject():

    @staticmethod
    def get_auto_manage_label():
        raise ManagedObjectException("Implementer doesn't support get_auto_manage_label()")

    @staticmethod
    def manage_template():
        raise ManagedObjectException("Implementer doesn't support manage_template()")

    @staticmethod
    def delete_template():
        raise ManagedObjectException("Implementer doesn't support delete_template()")

    def foreign_key_protected(self):
        raise ForeignKeyDependency("Implementer doesn't support foreign_key_protection()")


def manage_object(object_registry, object_class, object_id, next_url):
    """
    Associates a registry of managed object to their class name and form name
    When an object_id is specified the existing object's form is presented for editing
    When no object_id is specified a blank form is presented for creating a new object
    :param object_class: The class name of the managed object
    :param object_id: The object's id when editing existing
    :return: Rendered form when editing/creating, redirects upon commit
    :raise Exception: Any error
    """
    if not object_class in object_registry:
        raise Exception("The object '%s' is not auto-managed" % object_class)

    ManagedClass = object_registry[object_class]['class_name']
    managed_obj = ManagedClass()

    verb = 'Create'
    if object_id is not None:
        verb = 'Update'
        managed_obj = ManagedClass.query.get(object_id)

    ManagedClassForm = object_registry[object_class]['class_form']
    form = ManagedClassForm(obj=managed_obj)

    try:
        if form.validate_on_submit():
            form.populate_obj(managed_obj)
            if hasattr(managed_obj, 'form_populate_helper'):
                managed_obj.form_populate_helper()
            db.session.add(managed_obj)
            db.session.commit()
            flash("Object: '%s' Saved!" % managed_obj.get_auto_manage_label())
            return redirect(url_for(next_url))
    except Exception as error:
        flash(error)
    return render_template(
        ManagedClass.manage_template(),
        title="%s %s" % (verb, managed_obj.get_auto_manage_label()),
        form=form)


def delete_object(object_registry, object_class, object_id, next_url):
    """
    Associates a registry of managed object to their class name
    Displays a confirmation before deletion
    :param object_class: The class name of the managed object
    :param object_id: The object's id when editing existing
    :return: Rendered form when confirming, redirects upon commit
    :raise Exception: Any error
    """
    if not object_class in object_registry:
        raise Exception("The object '%s' is not auto-managed" % object_class)

    ManagedClass = object_registry[object_class]['class_name']
    managed_obj = ManagedClass.query.get(object_id)
    form = ConfirmForm()
    try:
        if object_id is None:
            raise Exception("Missing object_id")
        if request.method == 'POST':
            if request.form['action'] == 'Cancel':
                return redirect(url_for('beer_admin'))
            if request.form['action'] == 'Confirm':
                if managed_obj.foreign_key_protected():
                    db.session.delete(managed_obj)
                    db.session.commit()
                    flash("%s is gone" % managed_obj)
                    return redirect(url_for(next_url))
                else:
                    flash("We can't delete that because there are related records")

    except Exception as error:
        flash(error)
    return render_template(
        ManagedClass.delete_template(),
        form=form,
        managed_obj=managed_obj,
        title="Please Confirm")
