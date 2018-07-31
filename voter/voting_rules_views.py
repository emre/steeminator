from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from .forms import VotingRuleForm
from .models import VotingRule


@login_required
def voting_rules(request):
    voting_rules = VotingRule.objects.filter(
        voter_account__user=request.user)
    return render(request, "voting-rules.html", {"voting_rules": voting_rules})

@login_required
def add_voting_rule(request):
    form = VotingRuleForm()

    if request.method == 'POST':
        form = VotingRuleForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Voting Rule has been added to the system.'
            )
            return redirect('voting-rules')

    return render(request, "voting-rule-form.html", {
        "form": form,
        "action": "add"})


@login_required
def delete_voting_rule(request, voting_rule_id):
    try:
        voting_rule = VotingRule.objects.get(
            pk=voting_rule_id,
            voter_account__user=request.user)
    except VotingRule.DoesNotExist:
        raise Http404

    voting_rule.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        'Voting rule has been removed from the system.'
    )

    return redirect('voting-rules')
@login_required
def edit_voting_rule(request, voting_rule_id):
    try:
        voting_rule = VotingRule.objects.get(
            pk=voting_rule_id,
            voter_account__user=request.user)
    except VotingRule.DoesNotExist:
        raise Http404

    form = VotingRuleForm(instance=voting_rule)

    if request.method == "POST":
        form = VotingRuleForm(data=request.POST, instance=voting_rule)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Voting rule has been updated.'
            )
            return redirect('voting-rules')

    return render(request, "voting-rule-form.html", {
        "form": form,
        "action": "edit",
    })


@login_required
def disable_voting_rule(request, voting_rule_id):
    return toggle_voting_rule_status(request, voting_rule_id, action="disable")

@login_required
def enable_voting_rule(request, voting_rule_id):
    return toggle_voting_rule_status(request, voting_rule_id, action="enable")

def toggle_voting_rule_status(request, voting_rule_id, action):
    try:
        voting_rule = VotingRule.objects.get(
            pk=voting_rule_id,
            voter_account__user=request.user)
    except VotingRule.DoesNotExist:
        raise Http404

    voting_rule.is_active = action == "enable"
    voting_rule.save()

    messages.add_message(
        request,
        messages.SUCCESS,
        f'Voting rule for {voting_rule.target_account} has been {action}d.'
    )

    return redirect('voting-rules')

