"""Login callback overwrites for flask-login"""

import flask
from bussiness_dao import User
from app_factory import login_manager


@login_manager.user_loader
def user_loader(user_id):
    """user loader callback

    Args:
        user_id (string): unicode id

    Returns:
        _type_: user
    """
    quried_user = User.query.filter_by(id=user_id).first()
    if quried_user is None:
        return
    else:
        return quried_user


@login_manager.request_loader
def request_loader(request):
    """request loader callback

    Args:
        request (flask request): request data

    Returns:
        user: user
    """
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        quried_user = User.query.filter_by(username=username).first()
        if quried_user is None:
            print("user is none")
            return
        elif quried_user.password != password:
            print("password not equal")
            return
        else:
            return quried_user


@login_manager.unauthorized_handler
def unauthorized_handler():
    """Unauthorized handler

    Returns:
        _type_: html response
    """
    return flask.redirect(flask.url_for("signup"))
