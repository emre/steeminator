import datetime
from django import template
from django.conf import settings
register = template.Library()

@register.simple_tag
def steem_link(username):
    return f"{settings.STEEM_INTERFACE_URL}/@{username}"