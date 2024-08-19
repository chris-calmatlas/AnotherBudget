from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from tracker.utils import genericJsonError

from tracker.models import Account
from tracker.forms import newAccount

@login_required
def listAll(request): 
    # Get this users' account
    accounts = Account.objects.filter(owner=request.user)
    
    context = {
        "accounts": accounts,
        "accountForm": newAccount()
    }

    return render(request, "tracker/accounts.html", context)

@login_required
def api(request, accountId):
    response = {
        "method": request.method
    }
    
    # Create a new
    if request.method == "POST":
        # Return an error immediatly if a post is made with arguments
        if accountId is not None:
            return genericJsonError()
        
        # Validate data
        try:
            data = json.loads(request.body)
            accountForm = newAccount(data)
            if accountForm.is_valid():
                cleanedData = accountForm.cleaned_data
                # Form is valid, build an object
                account = Account(
                    description = cleanedData["description"],
                    amount = cleanedData["amount"],
                    date = cleanedData["date"],
                    owner = request.user
                )
                
            else:
                # There were errors
                return JsonResponse(accountForm.errors.as_json(), safe=False)
        except:
            return genericJsonError()
        
        return genericJsonError()

    # Read the account
    if request.method == "GET":
        return JsonResponse(response)

    # Update the account
    if request.method == "PUT":
        return JsonResponse(response)

    # Delete the account
    if request.method == "DELETE":
        return JsonResponse(response)
    
    return genericJsonError()