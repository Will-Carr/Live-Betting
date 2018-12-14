"""
Insta485 post view.

URLs include:
/p/<postid_slug>/
"""
import os
import flask
import arrow
import insta485
from insta485.model import get_db


@insta485.app.route('/p/<postid_slug>/', methods=['GET', 'POST'])
def show_post(postid_slug):
    """Display /p/<postid_slug>/ route."""
    if flask.request.method == 'POST':
        conn = get_db()
        con = conn.cursor()

        if flask.request.form.get("comment") is not None:
            postid = flask.request.form.get('postid')
            text = flask.request.form.get('text')
            owner = flask.session['logname']

            con.execute("INSERT INTO comments VALUES \
                        (NULL, ?,?,?, CURRENT_TIMESTAMP)",
                        (owner, postid, text))

        elif flask.request.form.get("uncomment") is not None:
            commentid = flask.request.form.get("commentid")
            con.execute("DELETE FROM comments WHERE commentid=?",
                        (int(commentid), ))

        elif flask.request.form.get("like") is not None:
            postid = flask.request.form.get('postid')
            con.execute("INSERT INTO likes VALUES \
                        (?,?, CURRENT_TIMESTAMP)",
                        (flask.session['logname'], postid))

        elif flask.request.form.get("unlike") is not None:
            postid = flask.request.form.get("postid")
            con.execute("DELETE FROM likes WHERE postid=?", (int(postid), ))

        elif flask.request.form.get("delete") is not None:
            postid = flask.request.form.get("postid")

            con.execute("SELECT filename FROM posts WHERE postid=?",
                        (int(postid), ))
            filename = con.fetchone()["filename"]
            filepath = os.path.join(
                insta485.app.config["UPLOAD_FOLDER"],
                filename
            )
            os.remove(filepath)

            con.execute("DELETE FROM posts WHERE postid=?", (int(postid), ))

            return flask.redirect('/u/' + flask.session['logname'] + '/')

    # Normal GET
    if "logname" not in flask.session or flask.session["logname"] is None:
        return flask.redirect(flask.url_for('show_login'))

    conn = get_db()
    con = conn.cursor()

    # Owner
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    all_post_info = con.fetchone()

    context = {
        "logname": flask.session["logname"],
        "postid": postid_slug,
        "owner": all_post_info["owner"],
    }
    # Owner prof pic
    # Snag that HOT prof pic
    con.execute("SELECT filename FROM users WHERE username=?",
                (all_post_info["owner"],))
    upp = "/uploads/"
    context["owner_img_url"] = upp+con.fetchone()['filename']

    # img_url
    context["img_url"] = upp+all_post_info["filename"]

    # timestamp using Arrow (ALL POSTS TRACKED ON UTC, NOT EST)
    time = all_post_info["created"]
    arrow_time = arrow.get(time, 'YYYY-MM-DD HH:mm:ss')
    context["timestamp"] = arrow_time.humanize()

    # Likes
    con.execute("SELECT COUNT(owner) as num FROM likes WHERE postid=?",
                (postid_slug,))
    context["likes"] = con.fetchone()['num']

    # Logname liked? T/F
    con.execute("SELECT owner FROM likes WHERE postid=?",
                (postid_slug,))
    owners_of_likes = con.fetchall()
    # Extract owner list
    owners_of_likes = [thing["owner"] for
                       thing in owners_of_likes]
    context["logname_liked"] = flask.session['logname'] in owners_of_likes

    # Comments
    con.execute("SELECT owner, text, commentid FROM \
                comments WHERE postid=?",
                (postid_slug, ))
    context["comments"] = con.fetchall()

    return flask.render_template("post.html", **context)
