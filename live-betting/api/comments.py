"""REST API for a post's comments."""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/api/v1/p/<int:postid_slug>/comments/', methods=["GET"])
def get_comments(postid_slug):
    """Return comments for one post.

    Example:
    {
      "comments": [
        {
          "commentid": 1,
          "owner": "awdeorio",
          "owner_show_url": "/u/awdeorio/",
          "postid": 3,
          "text": "#chickensofinstagram"
        },
        {
          "commentid": 2,
          "owner": "jflinn",
          "owner_show_url": "/u/jflinn/",
          "postid": 3,
          "text": "I <3 chickens"
        },
        {
          "commentid": 3,
          "owner": "michjc",
          "owner_show_url": "/u/michjc/",
          "postid": 3,
          "text": "Cute overload!"
        }
      ],
      "url": "/api/v1/p/3/comments/"
    }
    """
    if ("logname" not in flask.session) or flask.session["logname"] is None:
        context2 = {
            "message": "Forbidden",
            "status_code": 403  # More errors
        }

        return flask.jsonify(**context2), 403

    context = {
        "comments": [],
        "url": "/api/v1/p/" + str(postid_slug) + "/comments/"
    }

    # Establish connection
    conn = get_db()
    # Establish it some more
    con = conn.cursor()

    # Check if post exists
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    # Grab the post
    post_info = con.fetchone()

    # If post doesn't exist
    if post_info is None:
        # Set the context
        context = {
            "message": "Not Found",
            "status_code": 404
        }

        # Return not found
        return flask.jsonify(**context), 404

    # Get comments
    con.execute("SELECT owner, text, commentid FROM \
                comments WHERE postid=?",
                (postid_slug, ))
    comments = con.fetchall()

    # Add some data to comments
    for comment in comments:
        comment["postid"] = postid_slug
        comment["owner_show_url"] = "/u/" + comment["owner"] + "/"

    context["comments"] = comments

    return flask.jsonify(**context)


@insta485.app.route('/api/v1/p/<int:postid_slug>/comments/', methods=["POST"])
def post_comments(postid_slug):
    """Post the comment, then returns the DB entry of the comment.

    Example:
    POST:
    {
      "text": "Comment sent from curl"
    }

    Return:
    {
      "commentid": 8,
      "owner": "awdeorio",
      "owner_show_url": "/u/awdeorio/",
      "postid": 3,
      "text": "Comment sent from curl"
    }
    """
    if "logname" not in flask.session or flask.session["logname"] is None:
        context = {
            "message": "Forbidden",
            # Error is 403
            "status_code": 403
        }

        return flask.jsonify(**context), 403

    postid = postid_slug
    text = flask.request.get_json()['text']
    owner = flask.session['logname']

    # Establish connection
    conn = get_db()
    # More establishing
    con = conn.cursor()
    # Check if post exists
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    new_post_info = con.fetchone()
    # Now that we have the info,
    # Check if post doesn't exist
    if new_post_info is None:
        context = {
            "message": "Not Found",
            "status_code": 404
        }

        # Return 404
        return flask.jsonify(**context), 404

    # Insert comment
    con.execute("INSERT INTO comments VALUES \
                (NULL, ?,?,?, CURRENT_TIMESTAMP)",
                (owner, postid, text))

    # Get last inserted comment
    con.execute("SELECT owner, text, commentid FROM \
                comments WHERE commentid = last_insert_rowid()")
    comment = con.fetchone()

    # Add data
    comment["postid"] = postid_slug
    comment["owner_show_url"] = "/u/" + comment["owner"] + "/"

    context = comment

    return flask.jsonify(**context), 201
