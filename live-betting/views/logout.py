"""
Insta485 logout view.

URLs include:
/accounts/logout/
"""
import flask
import insta485


@insta485.app.route('/accounts/logout/')
def show_logout():
    """Display /accounts/logout/ route."""
    # logout stuff
    flask.session["logname"] = None
    return flask.redirect("/accounts/login/")
