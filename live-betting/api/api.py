"""REST API for api."""
import flask
import insta485


@insta485.app.route('/api/v1/', methods=["GET"])
def get_api():
    """Return API resource URLs.

    Example:
    {
      "posts": "/api/v1/p/",
      "url": "/api/v1/"
    }
    """
    if "logname" not in flask.session or flask.session["logname"] is None:
        # The context
        # More context
        context1 = {
            "message": "Forbidden",
            "status_code": 403  # With an error
        }

        return flask.jsonify(**context1), 403

    context = {}

    # posts
    context["postid"] = "/api/v1/p/"

    # url
    context["url"] = "/api/v1/"

    return flask.jsonify(**context)
