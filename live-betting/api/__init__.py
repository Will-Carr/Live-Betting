"""Insta485 REST API."""

from insta485.api.api import get_api
from insta485.api.posts import get_posts
from insta485.api.postid import get_post
from insta485.api.comments import get_comments, post_comments
from insta485.api.likes import get_likes, post_like, delete_like
