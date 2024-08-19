from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from tracker.models import Transaction
from tracker.forms import newTransaction

@login_required
def listAll(request): 
    # Get this users' transaction
    transactions = Transaction.objects.filter(owner=request.user)
    
    context = {
        "transactions": transactions,
        "transactionForm": newTransaction()
    }

    return render(request, "tracker/transactions.html", context)

@login_required
def api(request, transactionId):
    response = {
        "method": request.method
    }
    
    # Create a new
    if request.method == "POST":
        # Return an error immediatly if a post is made with arguments
        if transactionId is not None:
            return genericJsonError()
        
        # Validate data
        try:
            data = json.loads(request.body)
            transactionForm = newTransaction(data)
            if transactionForm.is_valid():
                cleanedData = transactionForm.cleaned_data
                # Form is valid, build an object
                transaction = Transaction(
                    description = cleanedData["description"],
                    amount = cleanedData["amount"],
                    date = cleanedData["date"],
                    owner = request.user
                )
                
            else:
                # There were errors
                return JsonResponse(transactionForm.errors.as_json(), safe=False)
        except:
            return genericJsonError()
        
        return genericJsonError()

    # Read the transaction
    if request.method == "GET":
        return JsonResponse(response)

    # Update the transaction
    if request.method == "PUT":
        return JsonResponse(response)

    # Delete the transaction
    if request.method == "DELETE":
        return JsonResponse(response)
    
    return genericJsonError()
    
def genericJsonError():
    return JsonResponse({"error": "true"})