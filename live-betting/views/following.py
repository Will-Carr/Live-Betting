"""
Insta485 following view.

URLs include:
/u/<user_url_slug>/following/
"""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/u/<user_url_slug>/following/', methods=['GET', 'POST'])
def show_following(user_url_slug):
    """Display /u/<user_url_slug>/following/ route."""
    if flask.request.method == 'POST':
        if "logname" not in flask.session or flask.session["logname"] is None:
            flask.abort(403)

        logname = flask.session["logname"]
        follow_name = flask.request.form.get("username")

        conn = get_db()
        c_db = conn.cursor()

        if flask.request.form.get("follow") is not None:
            c_db.execute("INSERT INTO following VALUES \
                         (?,?, CURRENT_TIMESTAMP)", (logname, follow_name))

        elif flask.request.form.get("unfollow") is not None:
            # Pylint fix
            usernames = " username1=? AND username2=?"
            c_db.execute("DELETE FROM following WHERE"+usernames,
                         (logname, follow_name))

    # Else GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        # Comment
        return flask.redirect(flask.url_for('show_login'))

    conn = get_db()
    # Other comment
    c_db = conn.cursor()

    logname = flask.session["logname"]
    # Following
    # Pylint fix
    lala = "FROM following WHERE username1=?"
    c_db.execute("SELECT username2 as username "+lala,
                 (user_url_slug, ))
    following = c_db.fetchall()

    # For each person the user_slug is following, get some info
    for follower in following:

        # user_img_url
        # Snag that HOT prof pic
        c_db.execute("SELECT filename FROM users WHERE username=?",
                     (follower["username"],))
        u_shrt = "/uploads/"
        follower["user_img_url"] = u_shrt+c_db.fetchone()['filename']

        # Logname follows username?
        # Pylint fix
        where12 = "WHERE username1=? AND username2=?"
        c_db.execute("SELECT username2 FROM following "+where12,
                     (logname, follower["username"]))
        following_logname = c_db.fetchone()
        follower["logname_follows_username"] = bool(following_logname)

    context = {
        "logname": flask.session["logname"],
        "following": following
    }

    return flask.render_template("following.html", **context)
