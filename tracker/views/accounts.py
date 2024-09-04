from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.core import serializers
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from tracker.utils import genericJsonError

from tracker.models import Account
from tracker.forms import newAccountForm

@login_required
def list(request):
    if request.method == "GET":
        # Get this users' account
        accounts = Account.objects.filter(owner=request.user)
        
        context = {
            "accounts": accounts,
            "accountForm": newAccountForm()
        }

        return render(request, "tracker/accounts.html", context)
    
    if request.method == "POST":
        # Validate data
        try:
            data = json.loads(request.body)
        except Exception as e:
            print("acounts validate data exception")
            raise PermissionDenied
        
        accountForm = newAccountForm(data)
        context = {
            "accounts": accounts,
            "accountForm": accountForm
        }
        if accountForm.is_valid():
            cleanedData = accountForm.cleaned_data
            # Form is valid, build an object
            account = Account(
                name = cleanedData["name"],
                startingBalance = cleanedData["startingBalance"],
                endingBalance = cleanedData["startingBalance"],
                description = cleanedData["description"],
                owner = request.user
            )
        else:
            # There were form validation errors
            return render(request, "tracker/accounts.html", context)
        
        try:            
            account.save()
        except IntegrityError as e:
            if("UNIQUE constraint failed" in f'{e}'):
                return JsonResponse({
                    "message": f'{cleanedData["name"]} already exists',
                    "success": "false"
                })
            print(e)
            return genericJsonError()
        except Exception as e:
            # db error
            print(e)
            return genericJsonError()

        return JsonResponse({
            "message": f'{cleanedData["name"]} added',
            "success": "true", 
            "record": serializers.serialize("json", [account])
        })

@login_required
def getAccount(request, accountId):
    if request.method == "GET":
        try:
            account = Account.objects.get(pk=accountId)
        except ObjectDoesNotExist as e:
            print(e)
            raise PermissionDenied
        
        context = {
            "account": account
        }

        if account.owner == request.user:
            return render(request, "tracker/getAccount.html", context)
        else:
            raise PermissionDenied

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
        except:
            # Something is wrong with the request.body
            return genericJsonError()
        
        accountForm = newAccountForm(data)
        if accountForm.is_valid():
            cleanedData = accountForm.cleaned_data
            # Form is valid, build an object
            account = Account(
                name = cleanedData["name"],
                startingBalance = cleanedData["startingBalance"],
                endingBalance = cleanedData["startingBalance"],
                description = cleanedData["description"],
                owner = request.user
            )
        else:
            # There were form validation errors
            return JsonResponse(accountForm.errors.as_json(), safe=False)
        
        try:            
            account.save()
        except IntegrityError as e:
            if("UNIQUE constraint failed" in f'{e}'):
                return JsonResponse({
                    "message": f'{cleanedData["name"]} already exists',
                    "success": "false"
                })
            print(e)
            return genericJsonError()
        except Exception as e:
            # db error
            print(e)
            return genericJsonError()

        return JsonResponse({
            "message": f'{cleanedData["name"]} added',
            "success": "true", 
            "record": serializers.serialize("json", [account])
        })

    # Read the account
    if request.method == "GET":
        try:
            account = Account.objects.get(pk=accountId)
        except ObjectDoesNotExist as e:
            print(e)
            raise PermissionDenied
        
        if account.owner == request.user:
            return JsonResponse(serializers.serialize("json", [account]))
        else:
            raise PermissionDenied

    # Update the account
    if request.method == "PUT":
        return JsonResponse(response)

    # Delete the account
    if request.method == "DELETE":
        return JsonResponse(response)
    
    return genericJsonError()