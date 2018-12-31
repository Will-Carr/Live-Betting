"""
Insta485 delete view.

URLs include:
/accounts/delete/
"""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/accounts/delete/', methods=['GET', 'POST'])
def show_delete():
    """Display /accounts/delete/ route."""
    if flask.request.method == 'POST':

        logname = flask.session["logname"]

        conn = get_db()
        c_db = conn.cursor()

        c_db.execute("DELETE FROM users WHERE username=?", (logname,))

        flask.session["logname"] = None
        return flask.redirect(flask.url_for('show_login'))

    # Else GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    context = {
        "logname": flask.session["logname"]
    }
    return flask.render_template("delete.html", **context)
