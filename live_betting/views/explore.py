"""
Insta485 explore view.

URLs include:
/explore/
"""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/explore/', methods=['GET', 'POST'])
def show_explore():
    """Display /explore/ route."""
    if flask.request.method == 'POST':
        if "logname" not in flask.session or flask.session["logname"] is None:
            flask.abort(403)

        # Check for follow/unfollow here and do whatever
        logname = flask.session["logname"]

        # If User presses Follow:
        follow_name = flask.request.form.get("username")
        print("FOLLOW NAME", follow_name, logname)
        conn = get_db()
        c_db = conn.cursor()

        c_db.execute("INSERT INTO following VALUES (?,?, CURRENT_TIMESTAMP)",
                     (logname, follow_name))

    # GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    conn = get_db()
    c_db = conn.cursor()

    logname = flask.session["logname"]

    # Get all users != logged_in
    # WHERE username <>?  means:
    # WHERE username != ?
    # and the ? gets logname
    c_db.execute("SELECT username FROM users WHERE username<>?", (logname, ))
    all_users = c_db.fetchall()
    print("all_users:\n", all_users)

    # Get all followers of logged_in
    c_db.execute("SELECT username2 FROM following WHERE username1=?",
                 (logname, ))
    following = c_db.fetchall()
    # Extract the usernames
    following = [followee["username2"] for followee in following]

    list_of_nonfollowers = []
    for username_dict in all_users:
        indexed_user = username_dict["username"]
        if indexed_user not in following:
            complete_entry = {}
            complete_entry["username"] = indexed_user

            c_db.execute("SELECT filename FROM users WHERE username=?",
                         (indexed_user,))
            u_shrt = "/uploads/"
            complete_entry["user_img_url"] = u_shrt+c_db.fetchone()['filename']
            list_of_nonfollowers.append(complete_entry)

    context = {
        "logname": flask.session["logname"],
        "not_following": list_of_nonfollowers
    }
    return flask.render_template("explore.html", **context)
