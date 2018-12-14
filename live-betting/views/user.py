"""
Insta485 user view.

URLs include:
/u/<user_url_slug>/
"""
import flask
import insta485
from insta485.model import get_db
from insta485.views.upload_file import upload_file


@insta485.app.route('/u/<user_url_slug>/', methods=['GET', 'POST'])
def show_user(user_url_slug):
    """Display /u/<user_url_slug>/ route."""
    con = get_db().cursor()
    if flask.request.method == 'POST':
        if "logname" not in flask.session or flask.session["logname"] is None:
            flask.abort(403)

        if flask.session['logname'] == user_url_slug:

            _, hash_filename_base = upload_file(flask.request.files["file"])

            con.execute("INSERT INTO 'posts' VALUES (NULL,?,?, \
                        CURRENT_TIMESTAMP)",
                        (hash_filename_base, flask.session['logname'],))

            # Get all logname follows
            con.execute("SELECT username2 FROM following WHERE username1=?",
                        (flask.session["logname"], ))
            # Extract the usernames
            logname_following = [followee["username2"] for
                                 followee in con.fetchall()]
            log_follows_user = (user_url_slug in logname_following)

            # Full Name
            con.execute("SELECT fullname FROM users WHERE username=?",
                        (user_url_slug, ))
            fullname = con.fetchone()["fullname"]

            # Number following
            # Get all username follows
            con.execute("SELECT username2 FROM following WHERE username1=?",
                        (user_url_slug, ))
            num_following = len(con.fetchall())

            # Number followers
            # Get all who follow username
            con.execute("SELECT username1 FROM following WHERE username2=?",
                        (user_url_slug, ))
            num_followers = len(con.fetchall())

            # Number Posts, plus other post stuff
            # Get all who follow username
            # Pylint fix
            con.execute("SELECT postid, filename as img_url \
                        FROM posts WHERE owner=?", (user_url_slug, ))
            u_posts, n_posts = con.fetchall(), len(con.fetchall())

            # Add "/uploads/" to all images
            for post in u_posts:
                post["img_url"] = "/uploads/"+post["img_url"]

            return flask.render_template('user.html', **{
                "logname": flask.session["logname"],
                "username": user_url_slug,
                "logname_follows_username": log_follows_user,
                "fullname": fullname,
                "following": num_following,
                "followers": num_followers,
                "total_posts": n_posts,
                "posts": u_posts
            })

        # else:
        follow_name = flask.request.form.get("username")

        if flask.request.form.get("follow") is not None:
            con.execute("INSERT INTO following VALUES \
                        (?,?, CURRENT_TIMESTAMP)",
                        (flask.session["logname"], follow_name))

        elif flask.request.form.get("unfollow") is not None:
            con.execute("DELETE FROM following WHERE username1=? AND \
                        username2=?", (flask.session["logname"], follow_name))

        # Get all logname follows
        con.execute("SELECT username2 FROM following WHERE username1=?",
                    (flask.session["logname"], ))
        # Extract the usernames
        logname_following = [followee["username2"] for
                             followee in con.fetchall()]
        log_follows_user = (user_url_slug in logname_following)

        # Full Name
        con.execute("SELECT fullname FROM users WHERE username=?",
                    (user_url_slug, ))
        fullname = con.fetchone()["fullname"]

        # Number following
        # Get all username follows
        con.execute("SELECT username2 FROM following WHERE username1=?",
                    (user_url_slug, ))
        num_following = len(con.fetchall())

        # Number followers
        # Get all who follow username
        con.execute("SELECT username1 FROM following WHERE username2=?",
                    (user_url_slug, ))
        num_followers = len(con.fetchall())

        # Number Posts, plus other post stuff
        # Get all who follow username
        con.execute("SELECT postid, filename as img_url FROM \
                    posts WHERE owner=?",
                    (user_url_slug, ))
        u_posts, n_posts = con.fetchall(), len(con.fetchall())

        # Add "/uploads/" to all images
        for post in u_posts:
            post["img_url"] = "/uploads/"+post["img_url"]

        return flask.render_template('user.html', **{
            "logname": flask.session["logname"],
            "username": user_url_slug,
            "logname_follows_username": log_follows_user,
            "fullname": fullname,
            "following": num_following,
            "followers": num_followers,
            "total_posts": n_posts,
            "posts": u_posts
        })

    # else:
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    # Get all logname follows
    con.execute("SELECT username2 FROM following WHERE username1=?",
                (flask.session["logname"], ))
    # Extract the usernames
    logname_following = [followee["username2"] for
                         followee in con.fetchall()]
    log_follows_user = (user_url_slug in logname_following)

    # Full Name
    con.execute("SELECT fullname FROM users WHERE username=?",
                (user_url_slug, ))
    fullname = con.fetchone()["fullname"]

    # Number following
    # Get all username follows
    con.execute("SELECT username2 FROM following WHERE username1=?",
                (user_url_slug, ))
    num_following = len(con.fetchall())

    # Number followers
    # Get all who follow username
    con.execute("SELECT username1 FROM following WHERE username2=?",
                (user_url_slug, ))
    num_followers = len(con.fetchall())

    # Number Posts, plus other post stuff
    # Get all who follow username
    con.execute("SELECT postid, filename FROM posts WHERE owner=?",
                (user_url_slug, ))
    u_posts, n_posts = con.fetchall(), len(con.execute(
        "SELECT postid, filename FROM posts WHERE owner=?",
        (user_url_slug, )).fetchall())

    # Add "/uploads/" to all images
    for post in u_posts:
        post["filename"] = "/uploads/"+post["filename"]

    return flask.render_template("user.html", **{
        "logname": flask.session["logname"],
        "username": user_url_slug,
        "logname_follows_username": log_follows_user,
        "fullname": fullname,
        "following": num_following,
        "followers": num_followers,
        "total_posts": n_posts,
        "posts": u_posts
    })
