"""
Insta485 create view.

URLs include:
/accounts/create/
"""
import hashlib
import uuid
import flask
import insta485
from insta485.model import get_db
from insta485.views.upload_file import upload_file


@insta485.app.route('/accounts/create/', methods=['GET', 'POST'])
def show_create():
    """Display /accounts/create/ route."""
    if flask.request.method == 'POST':

        if flask.request.form.get('password') == '':
            flask.abort(400)

        c_db = get_db().cursor()
        logname = flask.request.form.get('username')
        password = flask.request.form.get('password')

        file = flask.request.files["file"]
        _, hash_filename_basename = upload_file(file)

        salt = uuid.uuid4().hex
        hash_obj = hashlib.new('sha512')
        password_salted = salt + password
        hash_obj.update(password_salted.encode('utf-8'))
        password_hash = hash_obj.hexdigest()
        password = "$".join(['sha512', salt, password_hash])

        # Check if user already exists
        c_db.execute("SELECT username FROM users WHERE username=?", (logname,))
        my_user = c_db.fetchall()

        # User already exists
        if my_user != []:
            flask.abort(409)

        c_db.execute("INSERT INTO 'users' VALUES \
                     (?,?,?,?,?, CURRENT_TIMESTAMP)",
                     (logname, flask.request.form.get('fullname'),
                      flask.request.form.get('email'), hash_filename_basename,
                      password))

        flask.session['logname'] = flask.request.form.get('username')

        return flask.redirect('/')

    # If GET
    if "logname" in flask.session and flask.session["logname"] is not None:
        return flask.redirect("/accounts/edit/")

    return flask.render_template("create.html")
