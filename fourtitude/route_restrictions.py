from functools import update_wrapper
from flask import g, flash, request, redirect, url_for, abort
from fourtitude import user_models


def restrict(group_name):
    def decorator(fn):
        def wrapped_function(*args, **kwargs):
            if hasattr(g.user, "username") is not True:
                msg = "The page you're attempting to access requires you to be logged in"
                flash(msg)
                return redirect(url_for('login', next=request.url))
            else:
                group = user_models.UserGroup.query.filter_by(name=group_name).first()
                if group is None:
                    msg = "Can't find a group with name=" + group_name
                    flash(msg)
                    return redirect(url_for('index'))
                if group.has_member(g.user) is False:
                    msg = "User name=" + g.user.username + " does not belong to group name=" + group_name
                    flash(msg)
                    abort(403)
            return fn(*args, **kwargs)
        return update_wrapper(wrapped_function, fn)
    return decorator
