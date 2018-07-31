from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404

from .forms import AccountForm
from .models import SteemAccount


@login_required
def accounts(request):
    steem_accounts = SteemAccount.objects.filter(user=request.user)
    return render(request, "accounts.html", {"steem_accounts": steem_accounts})

@login_required
def add_account(request):
    if request.method == 'GET':
        form = AccountForm()

    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            account.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Account has been added to the system.'
            )
            return redirect('accounts')

    return render(request, "account_form.html", {
        "form": form,
        "action": "add"})

@login_required
def delete_account(request, account_id):
    try:
        account = SteemAccount.objects.get(
            pk=account_id,
            user=request.user)
    except SteemAccount.DoesNotExist:
        raise Http404

    account.delete()
    messages.add_message(
        request,
        messages.SUCCESS,
        'Account has been removed from the system.'
    )

    return redirect('accounts')

@login_required
def edit_account(request, account_id):
    try:
        account = SteemAccount.objects.get(
            pk=account_id,
            user=request.user)
    except SteemAccount.DoesNotExist:
        raise Http404

    form = AccountForm(instance=account)

    if request.method == "POST":
        form = AccountForm(data=request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Account has been updated.'
            )
            return redirect('accounts')

    return render(request, "account_form.html", {
        "form": form,
        "account": account,
        "action": "edit",
    })


@login_required
def disable_account(request, account_id):
    return toggle_account_status(request, account_id, action="disable")

@login_required
def enable_account(request, account_id):
    return toggle_account_status(request, account_id, action="enable")

def toggle_account_status(request, account_id, action):
    try:
        account = SteemAccount.objects.get(
            pk=account_id,
            user=request.user)
    except SteemAccount.DoesNotExist:
        raise Http404

    account.is_active = action == "enable"
    account.save()

    messages.add_message(
        request,
        messages.SUCCESS,
        f'Account {account.steem_username} has been {action}d.'
    )

    return redirect('accounts')
@login_required
def settings():
    pass

