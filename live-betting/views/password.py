"""
Insta485 password view.

URLs include:
/accounts/password/
"""
import uuid
import hashlib
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/accounts/password/', methods=['GET', 'POST'])
def show_password():
    """Display /accounts/password/ route."""
    if flask.request.method == 'POST':

        # Check for empty password
        if flask.request.form.get('new_password1') == '':
            flask.abort(400)

        # Check if new passwords match
        # Pylint fix
        truething = (flask.request.form.get('new_password1') !=
                     flask.request.form.get('new_password2'))
        if truething:
            flask.abort(401)

        logname = flask.session["logname"]
        password = flask.request.form.get('password')
        new_password = flask.request.form.get('new_password1')

        conn = get_db()
        con = conn.cursor()

        con.execute("SELECT username, password FROM users WHERE username=?",
                    (logname, ))
        my_user = con.fetchall()[0]

        password_split = my_user["password"].split("$")

        algorithm = password_split[0]
        salt = password_split[1]
        hash_obj = hashlib.new(algorithm)
        # Comment 1
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()

        if password_split[2] == password_hash:

            algorithm = 'sha512'
            salt = uuid.uuid4().hex
            hash_obj = hashlib.new(algorithm)
            password_salted = salt + new_password
            hash_obj.update(password_salted.encode('utf-8'))
            password_hash = hash_obj.hexdigest()
            password_db_string = "$".join([algorithm, salt, password_hash])

            con.execute("UPDATE users SET password=? WHERE username=?",
                        (password_db_string, logname))

            return flask.redirect('/accounts/edit/')

        # Password is wrong
        flask.abort(403)

    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    # Comment
    context = {
        "logname": flask.session["logname"]
    }
    return flask.render_template("password.html", **context)
