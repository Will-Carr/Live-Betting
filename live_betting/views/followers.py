"""
Insta485 followers view.

URLs include:
/u/<user_url_slug>/followers/
"""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/u/<user_url_slug>/followers/', methods=['GET', 'POST'])
def show_followers(user_url_slug):
    """Display /u/<user_url_slug>/followers/ route."""
    if flask.request.method == 'POST':
        if "logname" not in flask.session or flask.session["logname"] is None:
            # Abort
            flask.abort(403)

        logname = flask.session["logname"]
        follow_name = flask.request.form.get("username")

        c_db = get_db().cursor()

        if flask.request.form.get("follow") is not None:
            c_db.execute("INSERT INTO following VALUES \
                         (?,?, CURRENT_TIMESTAMP)", (logname, follow_name))

        # Pylint?
        elif flask.request.form.get("unfollow") is not None:
            # Pylint fix
            usernames = " username1=? AND username2=?"
            # Pylint?
            c_db.execute("DELETE FROM following WHERE"+usernames,
                         (logname, follow_name))

    # Else GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    c_db = get_db().cursor()

    logname = flask.session["logname"]

    c_db.execute("SELECT username FROM users WHERE username<>?",
                 (user_url_slug, ))

    # Get all followers of user_url_slug
    string_thing = "following WHERE username2=?"
    c_db.execute("SELECT username1 as username FROM "+string_thing,
                 (user_url_slug, ))
    following = c_db.fetchall()

    # Get all logname follows
    c_db.execute("SELECT username2 FROM following WHERE username1=?",
                 (logname, ))
    logname_following = c_db.fetchall()
    # Extract the usernames
    logname_following = [followee["username2"] for
                         followee in logname_following]

    list_of_followers = []
    for username_dict in following:
        indexed_user = username_dict["username"]

        # Snag that HOT prof pic
        c_db.execute("SELECT filename FROM users WHERE username=?",
                     (indexed_user,))
        u_shrt = "/uploads/"
        username_dict["user_img_url"] = u_shrt+c_db.fetchone()['filename']

        # Does the logged in user follow this user?
        log_follows = "logname_follows_username"
        username_dict[log_follows] = (indexed_user in logname_following)

        list_of_followers.append(username_dict)

    context = {
        "logname": flask.session["logname"],
        "followers": list_of_followers
    }

    return flask.render_template("followers.html", **context)
