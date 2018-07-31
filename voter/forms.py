from django.forms import ModelForm
from django.db import models
from django.forms import ValidationError
from django.forms import PasswordInput

from .models import SteemAccount, VotingRule
from beemgraphenebase.account import PrivateKey
from main.connections import get_beem

class AccountForm(ModelForm):

    class Meta:
        model = SteemAccount
        fields = ('steem_username', 'posting_key', 'vp_limit')
        widgets = {
            "posting_key": PasswordInput(render_value=True),
        }

    def clean_posting_key(self):
        beem = get_beem()
        try:
            public_key = str(
                PrivateKey(self.cleaned_data.get("posting_key")).pubkey)
        except ValueError as e:
            if 'Base58' in e.args[0]:
                raise ValidationError("Invalid posting key.")
            raise

        accounts = list(beem.wallet.getAccountsFromPublicKey(public_key))

        if self.cleaned_data.get("steem_username") not in accounts:
            raise ValidationError("Incorrect posting key.")

        return self.cleaned_data["posting_key"]

    def clean_vp_limit(self):
        if not (0 < self.cleaned_data.get("vp_limit") < 100):
            raise ValidationError("Vp Limit must be between 0 and 100.")

        return self.cleaned_data["vp_limit"]

class VotingRuleForm(ModelForm):

    class Meta:
        model = VotingRule
        fields = [
            "target_account",
            "voter_account",
            "weight",
            "delay",
            "daily_maximum",
            "upvote_comments"
        ]
