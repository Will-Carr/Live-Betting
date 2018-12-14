"""
Insta485 index (main) view.

URLs include:
/
"""
import flask
import arrow
import insta485
from insta485.model import get_db


@insta485.app.route('/', methods=['GET', 'POST'])
def show_index():
    """Display / route."""
    if flask.request.method == 'POST':
        if "logname" not in flask.session or flask.session["logname"] is None:
            flask.abort(403)

        conn = get_db()
        con = conn.cursor()
        logname = flask.session["logname"]

        # Check for like or comment post here and do whatever
        if flask.request.form.get('comment') is not None:
            text = flask.request.form.get('text')
            # Pylint fix
            ts123 = "CURRENT_TIMESTAMP"
            con.execute("INSERT INTO comments VALUES (NULL, ?,?,?, "+ts123+")",
                        (logname, flask.request.form.get('postid'), text))

        elif flask.request.form.get('like') is not None:
            con.execute("INSERT INTO likes VALUES (?,?, CURRENT_TIMESTAMP)",
                        (logname, flask.request.form.get('postid')))

        elif flask.request.form.get('unlike') is not None:
            con.execute("DELETE FROM likes WHERE postid=? AND owner=?",
                        (flask.request.form.get('postid'), logname))

    # GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    # Just have to pull all posts... should be simple
    conn = get_db()
    con = conn.cursor()
    logname = flask.session["logname"]

    # Get ALL posts

    con.execute("SELECT filename as img_url, owner, \
                postid, created FROM posts")
    posts_info = con.fetchall()

    # ***Only keep the posts of the people you're following
    # Get all followers of logname

    con.execute("SELECT username2 \
                FROM following WHERE username1=?",
                (logname, ))
    followers = con.fetchall()
    followers = [foll["username2"] for
                 foll in followers]
    followers.append(logname)

    # Throw out any info from a post whose owner not follower
    new_post_info = []
    for post in posts_info:
        if post["owner"] in followers:
            new_post_info.append(post)
    posts_info = new_post_info

    # We'll work with post_info to add the rest of the info
    context = {
        "logname": flask.session["logname"]
    }
    for post in posts_info:
        # Snag that HOT prof pic
        owner = post["owner"]
        con.execute("SELECT filename FROM users WHERE username=?",
                    (owner,))
        upp = "/uploads/"
        post["owner_img_url"] = upp+con.fetchone()['filename']

        # Add /uploads/ to actual post pic
        post["img_url"] = upp+post["img_url"]

        # timestamp using Arrow (ALL POSTS TRACKED ON UTC, NOT EST)
        time = post["created"]
        post["timestamp"] = arrow.get(time,
                                      'YYYY-MM-DD HH:mm:ss').humanize()
        post.pop('created', None)

        # Likes
        con.execute("SELECT COUNT(owner) as num FROM likes WHERE postid=?",
                    (post["postid"],))
        post["likes"] = con.fetchone()['num']

        # Logname liked? T/F
        con.execute("SELECT owner FROM likes WHERE postid=?",
                    (post["postid"],))
        owners_of_likes = con.fetchall()
        owners_of_likes = [i["owner"] for
                           i in owners_of_likes]
        post["logname_liked"] = logname in owners_of_likes

        # Comments
        con.execute("SELECT owner, text FROM comments WHERE postid=?",
                    (post["postid"], ))
        comments_info = con.fetchall()
        post["comments"] = comments_info
        # print("\n\nNEW POST SQL READ\n\n", post)

        context = {
            "logname": flask.session["logname"],
            "posts": posts_info
        }

    return flask.render_template("index.html", **context)
