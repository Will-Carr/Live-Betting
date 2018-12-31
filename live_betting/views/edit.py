"""
Insta485 edit view.

URLs include:
/accounts/edit/
"""
import hashlib
import flask
import insta485
from insta485.model import get_db
from insta485.views.upload_file import upload_file


def sha256sum(filename):
    """Return sha256 hash of file content, similar to UNIX sha256sum."""
    content = open(filename, 'rb').read()
    sha256_obj = hashlib.sha256(content)
    return sha256_obj.hexdigest()


@insta485.app.route('/accounts/edit/', methods=['GET', 'POST'])
def show_edit():
    """Display /accounts/edit/ route."""
    if flask.request.method == 'POST':

        c_db = get_db().cursor()
        new_name = flask.request.form.get('fullname')
        new_email = flask.request.form.get('email')

        file = flask.request.files["file"]
        _, hash_filename_basename = upload_file(file)

        # Needed to shorten line for pylint
        shrt = "fullname=?, email=?, filename=?"
        hfb = hash_filename_basename
        c_db.execute("UPDATE users SET "+shrt+" WHERE username=?",
                     (new_name, new_email, hfb, flask.session['logname']))

        c_db.execute("SELECT * FROM users WHERE username=?",
                     (flask.session['logname'],))
        all_qualities = c_db.fetchone()

        context = {
            "logname": flask.session["logname"],
            "logname_img_url": "/uploads/"+all_qualities['filename'],
            "name": all_qualities['fullname'],
            "email": all_qualities['email']
        }

        return flask.render_template('edit.html', **context)

    # Else GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    conn = get_db()
    c_db = conn.cursor()

    c_db.execute("SELECT * FROM users WHERE username=?",
                 (flask.session["logname"],))

    all_qualities = c_db.fetchone()

    context = {
        "logname": flask.session["logname"],
        "logname_img_url": "/uploads/"+all_qualities['filename'],
        "name": all_qualities['fullname'],
        "email": all_qualities['email']
    }

    return flask.render_template("edit.html", **context)
