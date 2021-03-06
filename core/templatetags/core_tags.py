
from django.template import Library
from redis import ConnectionError

from core.models import Drawing
from core.utils import redis


register = Library()

@register.filter
def photo_for_user(user):
    """
    Just returns the path to the user's photo since we can't
    combined values in a template to pass to the thumbnail tag.
    """
    return "photos/%s" % user.id

@register.filter
def image_for_drawing(drawing):
    """
    Just returns the path to the drawing's image since we can't
    combined values in a template to pass to the thumbnail tag.
    """
    return "drawings/%s" % drawing.id

@register.simple_tag(takes_context=True)
def load_in_progress(context):
    """
    Returns the keys and numbers of users for each of the drawings
    in progress.
    """
    progress = []
    try:
        for key in redis.keys("users-*"):
            progress.append({
                "key": key.split("-")[1],
                "users": [u.split(",")[0] for u in redis.smembers(key)],
            })
    except ConnectionError:
        pass
    context["progress"] = sorted(progress, key=lambda x: len(x["users"]), reverse=True)
    return ""
