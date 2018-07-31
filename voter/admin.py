from django.contrib import admin

from .models import VotingRule, SteemAccount

admin.site.register(SteemAccount)
admin.site.register(VotingRule)
