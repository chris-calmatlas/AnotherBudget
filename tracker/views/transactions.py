from django.shortcuts import render, redirect
import json
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, MultipleObjectsReturned
from django.core import serializers
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required

from tracker.models import Transaction
from tracker.forms import newTransactionForm

@login_required
def listAll(request): 
    # Get this users' transaction
    transactions = Transaction.objects.filter(owner=request.user)
    
    context = {
        "transactions": transactions,
        "transactionForm": newTransactionForm()
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
        except:
            # Something is wrong with the request.body
            return genericJsonError()
        
        transactionForm = newTransactionForm(data)
        if transactionForm.is_valid():
            cleanedData = transactionForm.cleaned_data
            account = cleanedData["account"]

            # Form is valid, build an object
            transaction = Transaction(
                description = cleanedData["description"],
                amount = cleanedData["amount"],
                date = cleanedData["date"],
                owner = request.user,
                account = account, 
                isIncome = cleanedData["isIncome"]
            )

        else:
            # There were form validation errors
            return JsonResponse(transactionForm.errors.as_json(), safe=False)

        # save the transaction
        try:
            transaction.save()
        except IntegrityError as e:
            if("UNIQUE constraint failed" in f'{e}'):
                return JsonResponse({
                    "message": f'Possible duplicate.',
                    "success": "false"
                })
            print(e)
            return genericJsonError()
        except Exception as e:
            # db error
            # TODO: check if account was updated and rollback as neccessary
            print(e)
            return genericJsonError()

        return JsonResponse({
            "message": f'Transaction added',
            "success": "true", 
            "record": serializers.serialize("json", [transaction])
        })

    # Read the transaction
    if request.method == "GET":
        return JsonResponse(response)

    # Update the transaction
    if request.method == "PUT":
        return JsonResponse(response)

    # Delete the transaction
    if request.method == "DELETE":
        print(f'transactionId: {transactionId}')
        print(type(transactionId))
        # Try to get transaction. Error if a single transaction is not matched
        try:
            transaction = Transaction.objects.get(pk=transactionId)
        except Exception as e:
            print(e)
            raise PermissionDenied
        
        # Validate owner matches this user or error
        if transaction.owner == request.user:
            try:
                transaction.delete()
            except Exception as e:
                print(e)
                return JsonResponse({
                    "message": f'Something went wrong',
                    "success": "false"
                })
            
            return JsonResponse({
                "message": f'Transaction Deleted',
                "success": "true",
                "record": serializers.serialize("json", [transaction])
            })
        else:
            print("transction owner doesn't match current user")
            raise PermissionDenied
    
    return genericJsonError()
    
def genericJsonError():
    return JsonResponse({"error": "true"})