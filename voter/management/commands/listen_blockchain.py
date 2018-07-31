import logging
import time

from beem import Steem
from django.conf import settings
from django.core.management.base import BaseCommand

from voter.models import VotingRule

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()


class Command(BaseCommand):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.s = Steem(nodes=settings.STEEM_NODES)
        self.target_accounts = set()
        self.latest_target_account_refresh_time = None
        self.refresh_target_accounts()

    def refresh_target_accounts(self):
        if self.latest_target_account_refresh_time:
            data_age = int(
                time.time()) - self.latest_target_account_refresh_time

            if data_age < 300:
                logger.info(
                    f"No need to refresh. Old data is on "
                    f"the life span. ({data_age})")
                return

        self.target_accounts = set(list(VotingRule.objects.filter(
            is_active=True).values_list('target_account', flat=True)))
        self.latest_target_account_refresh_time = int(time.time())
        logger.info("Set target_accounts.")

    def get_account_rules(self, target_account):
        return VotingRule.objects.filter(target_account=target_account)

    def get_last_block_height(self):
        try:
            props = self.s.rpc.get_dynamic_global_properties()
            return props['head_block_number']
        except Exception as e:
            return self.get_last_block_height()

    def parse_block(self, block_id):
        logger.info("Parsing %s", block_id)

        # get all operations in the related block id
        operation_data = self.s.rpc.get_ops_in_block(
            block_id, False)

        for operation in operation_data:
            self.handle_operation(*operation['op'][0:2])

    def handle_operation(self, op_type, op_value):
        if op_type != "comment":
            # only interested in comment operations, at the moment.
            return

        if op_value["author"] not in self.target_accounts:
            # if the author is nobodie
            return

        self.upvote(op_value)

    def upvote(self, op_value):
        print(op_value)
        # @todo

    def listen_blocks(self, starting_point=None):
        if not starting_point:
            starting_point = self.get_last_block_height()
        while True:
            print(self.get_last_block_height() - starting_point)
            while (self.get_last_block_height() - starting_point) > 0:
                starting_point += 1
                self.parse_block(starting_point)

            logger.info("Sleeping...")
            self.refresh_target_accounts()
            logger.info("Refreshed target accounts.")
            time.sleep(2)


    def handle(self, *args, **options):
        self.listen_blocks()