"""REST API for likes."""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/api/v1/p/<int:postid_slug>/likes/', methods=["GET"])
def get_likes(postid_slug):
    """Return likes on postid.

    Example:
    {
      "logname_likes_this": 1,
      "likes_count": 3,
      "postid": 1,
      "url": "/api/v1/p/1/likes/"
    }
    """
    if "logname" not in flask.session or flask.session["logname"] is None:
        context6 = {
            "message": "Forbidden",
            "status_code": 403
        }
        # Wow, errors

        # Return the error
        return flask.jsonify(**context6), 403

    # User
    logname = flask.session["logname"]
    context = {}

    # url
    context["url"] = flask.request.path

    # Post
    postid = postid_slug
    context["postid"] = postid

    conn = get_db()
    con = conn.cursor()

    # Check if post exists
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    post_info = con.fetchone()

    # If post doesn't exist
    if post_info is None:
        context = {
            "message": "Not Found",
            "status_code": 404
        }

        return flask.jsonify(**context), 404

    # Did this user like this post?
    connection = insta485.model.get_db()
    cur = connection.execute(
        "SELECT EXISTS( "
        "  SELECT 1 FROM likes "
        "    WHERE postid = ? "
        "    AND owner = ? "
        "    LIMIT 1"
        ") AS logname_likes_this ",
        (postid, logname)
    )
    logname_likes_this = cur.fetchone()
    context.update(logname_likes_this)

    # Likes
    cur = connection.execute(
        "SELECT COUNT(*) AS likes_count FROM likes WHERE postid = ? ",
        (postid,)
    )
    likes_count = cur.fetchone()
    context.update(likes_count)

    return flask.jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid_slug>/likes/', methods=["POST"])
def post_like(postid_slug):
    """Add like on postid and return.

    Example return:
    {
      "logname": "awdeorio",
      "postid": 3
    }
    """
    if "logname" not in flask.session or (flask.session["logname"] is None):
        context3 = {
            "message": "Forbidden",
            "status_code": 403
        }

        return flask.jsonify(**context3), 403

    # User
    logname = flask.session["logname"]
    postid = postid_slug

    conn = get_db()
    con = conn.cursor()

    # Check if post exists
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    post_info = con.fetchone()

    # If post doesn't exist
    if post_info is None:
        context = {
            "message": "Not Found",
            "status_code": 404
        }

        return flask.jsonify(**context), 404

    # Check if like already exists (T/F)
    con.execute("SELECT owner FROM likes WHERE postid=?",
                (postid,))
    owners_of_likes = con.fetchall()

    # Extract owner list
    owners_of_likes = [thing["owner"] for thing in owners_of_likes]

    # Error if already liked
    if logname in owners_of_likes:
        context = {
            "logname": logname,
            "message": "Conflict",
            "postid": postid,
            "status_code": 409
        }

        return flask.jsonify(**context), 409

    # Add like to DB
    con.execute("INSERT INTO likes VALUES \
                (?,?, CURRENT_TIMESTAMP)",
                (logname, postid))

    context = {
        "logname": logname,
        "postid": postid
    }

    return flask.jsonify(**context), 201


@insta485.app.route('/api/v1/p/<int:postid_slug>/likes/', methods=["DELETE"])
def delete_like(postid_slug):
    """Delete like on postid."""
    if ("logname" not in flask.session or flask.session["logname"] is None):
        context4 = {
            "message": "Forbidden",
            "status_code": 403
        }

        return flask.jsonify(**context4), 403

    logname = flask.session["logname"]
    postid = postid_slug

    conn = get_db()
    con = conn.cursor()

    # Check if post exists
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    post_info = con.fetchone()

    # If post doesn't exist
    if post_info is None:
        context = {
            "message": "Not Found",
            "status_code": 404
        }

        return flask.jsonify(**context), 404

    # Delete like from DB
    con.execute("DELETE FROM likes WHERE postid=? \
                AND owner=?", (postid, logname))

    return '', 204
