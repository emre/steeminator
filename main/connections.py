from beem import Steem

from django.conf import settings

_beem_instance = None

def get_beem():
    global _beem_instance
    if not _beem_instance:
       _beem_instance = Steem(node=settings.STEEM_NODES)
    return _beem_instance
