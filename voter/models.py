from django.db import models
from django.contrib.auth.models import User

from main.models import BaseModel


class SteemAccount(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    steem_username = models.CharField(max_length=255)
    posting_key = models.CharField(
        max_length=51,
        help_text="Private posting key. "
                  "See it at https://steemit.com/@<username>/permissions"
    )
    auto_claim_rewards = models.BooleanField(default=False)
    vp_limit = models.PositiveIntegerField(default=80, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username


class VotingRule(BaseModel):
    voter_account = models.ForeignKey(
        SteemAccount, on_delete=models.DO_NOTHING)
    target_account = models.CharField(
        max_length=255,
        help_text="Account to vote"
    )
    weight = models.IntegerField(
        default=100,
        help_text="Should be between -100 and +100"
    )
    delay = models.IntegerField(
        default=20, help_text="Minutes to wait before casting a vote")
    daily_maximum = models.IntegerField(
        default=3,
        help_text="Maximum number of votes spendable on a daily basis"
    )
    upvote_comments = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)



VOTING_RULE_UPVOTE_ACTION_ID = 1
VOTING_RULE_UPVOTE_ACTION_DESC = 'Upvote (Voting Rule)'

ACTION_TYPES = (
    (VOTING_RULE_UPVOTE_ACTION_ID, VOTING_RULE_UPVOTE_ACTION_DESC),
)


class ActionLog(BaseModel):
    action_type = models.IntegerField(
        default=VOTING_RULE_UPVOTE_ACTION_ID,
        choices=ACTION_TYPES)
    actor = models.ForeignKey(SteemAccount, on_delete=models.DO_NOTHING,
                              related_name="actor")
    affected = models.ForeignKey(SteemAccount, null=True, blank=True,
                                 on_delete=models.DO_NOTHING,
                                 related_name="affected")
    metadata = models.TextField()

    def get_action_description(self, action_type):
        for action_id, action_desc in ACTION_TYPES:
            if action_type == action_id:
                return action_desc

        raise ValueError("Invalid action")

    def __str__(self):
        action_description = self.get_action_description(self.action_type)
        return f"{action_description} - actor: {self.actor}"
