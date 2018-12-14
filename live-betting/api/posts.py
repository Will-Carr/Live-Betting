"""REST API for posts."""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/api/v1/p/', methods=["GET"])
def get_posts():
    """Return posts.

    Example:
    {
      "next": "",
      "results": [
        {
          "postid": 3,
          "url": "/api/v1/p/3/"
        },
        {
          "postid": 2,
          "url": "/api/v1/p/2/"
        },
        {
          "postid": 1,
          "url": "/api/v1/p/1/"
        }
      ],
      "url": "/api/v1/p/"
    }
    """
    if "logname" not in flask.session or flask.session["logname"] is None:
        # Error: forbidden
        context = {
            "message": "Forbidden",
            "status_code": 403
        }

        # Return the error
        return flask.jsonify(**context), 403

    logname = flask.session["logname"]

    # Get size and page from url
    size = flask.request.args.get('size', None)
    page = flask.request.args.get('page', None)

    try:
        if size is not None:
            size = int(size)
        if page is not None:
            page = int(page)
    except ValueError:
        context8 = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context8), 400

    # If size isn't set, default to 10 results
    if size is None:
        size = 10

    # If page isn't set, default to the 0th page
    if page is None:
        page = 0

    # Bad request if not non-negative
    # Should size be 1 or 0?
    if size < 1 or page < 0:
        context = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context), 400

    context = {
        "next": "",
        "results": []
    }

    offset_rows = page * size

    # Get posts from db
    conn = get_db()
    con = conn.cursor()

    # Get posts (followers + logname)
    con.execute("SELECT postid, owner FROM posts \
                WHERE owner IN \
                (SELECT username2 FROM following WHERE username1=?) \
                OR owner = ? \
                ORDER BY postid DESC LIMIT ? OFFSET ?",
                (logname, logname, size, offset_rows))
    posts_info = con.fetchall()

    for post in posts_info:
        results_row = {
            "postid": post["postid"],
            "url": "/api/v1/p/" + str(post["postid"]) + "/"
        }
        context["results"].append(results_row)

    if context["results"] == []:
        context9 = {
            "message": "Bad Request",
            "status_code": 400
        }
        return flask.jsonify(**context9), 400

    # See if there's a next page
    con.execute("SELECT COUNT(*) FROM posts \
                WHERE owner IN \
                (SELECT username2 FROM following WHERE username1=?) \
                OR owner = ?",
                (logname, logname))
    post_count = con.fetchall()[0]['COUNT(*)']

    # Update next
    if post_count > (offset_rows + size):
        context['next'] = "/api/v1/p/?size=" + str(size) + "&page=" \
                          + str(page + 1)

    return flask.jsonify(**context)
