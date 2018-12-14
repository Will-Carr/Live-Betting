"""REST API for a single post."""
import flask
import insta485
from insta485.model import get_db


@insta485.app.route('/api/v1/p/<int:postid_slug>/', methods=["GET"])
def get_post(postid_slug):
    """Return post metadata: URL, username, etc.

    Example:
    {
      "age": "2017-09-28 04:33:28",
      "img_url": "/uploads/9887e06812ef434d291e4936417d125cd594b38a.jpg",
      "owner": "awdeorio",
      "owner_img_url": "/uploads/e1a7c5c32973862ee15173b0259e3efdb6a391af.jpg",
      "owner_show_url": "/u/awdeorio/",
      "post_show_url": "/p/3/",
      "url": "/api/v1/p/3/"
    }
    """
    if "logname" not in flask.session or flask.session["logname"] is None:
        context = {
            "message": "Forbidden",
            "status_code": 403
        }

        return flask.jsonify(**context), 403

    conn = get_db()
    # Get posts from db
    con = conn.cursor()

    # Get post
    con.execute("SELECT * FROM posts WHERE postid=?",
                (postid_slug, ))
    post_info = con.fetchone()

    context = {}

    # If post doesn't exist
    if post_info is None:

        # Set the error context
        context = {
            # This stuff doesn't exist
            "message": "Not Found",
            "status_code": 404
        }
        # Return error

        return flask.jsonify(**context), 404

    # Get owner propic
    con.execute("SELECT filename FROM users WHERE username=?",
                (post_info["owner"],))
    propic = "/uploads/" + con.fetchone()['filename']

    context["age"] = post_info["created"]
    context["img_url"] = "/uploads/" + post_info["filename"]
    context["owner"] = post_info["owner"]
    context["owner_img_url"] = propic
    context["owner_show_url"] = "/u/" + post_info["owner"] + "/"
    context["post_show_url"] = "/p/" + str(post_info["postid"]) + "/"
    context["url"] = "/api/v1/p/" + str(post_info["postid"]) + "/"

    return flask.jsonify(**context)
