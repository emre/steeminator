from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index, name="home"),
    path('login', auth_views.login, {"template_name": "login.html"},
         name="login"),
    path('logout', auth_views.logout, {'template_name': 'logged_out.html'},
         name='logout'),
    path('settings', views.settings),
    path('accounts', views.accounts, name="accounts"),
    path('accounts/add', views.add_account, name="add-account"),
    path('accounts/delete/<account_id>', views.delete_account,
         name="delete-account"),
    path('accounts/edit/<account_id>', views.edit_account, name="edit-account"),
    path('accounts/disable/<account_id>', views.disable_account,
         name="disable-account"),
    path('accounts/enable/<account_id>', views.enable_account,
         name="enable-account"),

    path('voting-rules', views.voting_rules, name="voting-rules"),
    path('voting-rules/add', views.add_voting_rule, name="add-voting-rule"),
    path('voting-rules/delete/<voting_rule_id>', views.delete_voting_rule,
         name="delete-voting-rule"),
    path('voting-rules/edit/<voting_rule_id>', views.edit_voting_rule,
         name="edit-voting-rule"),
    path('voting-rules/disable/<voting_rule_id>', views.disable_voting_rule,
         name="disable-voting-rule"),
    path('voting-rules/enable/<voting_rule_id>', views.enable_voting_rule,
         name="enable-voting-rule"),
]
