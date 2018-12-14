"""
Insta485 login view.

URLs include:
/accounts/login/
"""
import hashlib
# import uuid
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/accounts/login/', methods=['GET', 'POST'])
def show_login():
    """Display /accounts/login/ route."""
    if flask.request.method == 'POST':

        logname = flask.request.form.get('username')
        password = flask.request.form.get('password')

        # No password
        if not password:
            flask.abort(403)

        conn = get_db()
        con = conn.cursor()

        con.execute("SELECT username, password FROM users WHERE username=?",
                    (logname, ))
        my_user = con.fetchall()

        # User doesn't exist
        if not my_user:
            flask.abort(403)

        my_user = my_user[0]

        password_split = my_user["password"].split("$")

        algorithm = password_split[0]
        salt = password_split[1]
        hash_obj = hashlib.new(algorithm)
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()

        if password_split[2] == password_hash:
            flask.session['logname'] = logname
            return flask.redirect('/')

        # Password is wrong
        flask.abort(403)

    if "logname" in flask.session and flask.session["logname"] is not None:
        return flask.redirect("/")

    return flask.render_template("login.html")
