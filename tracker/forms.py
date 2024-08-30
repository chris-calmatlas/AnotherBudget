from django import forms
from tracker.models import Account
from datetime import date

class newTransactionForm(forms.Form):
    date=forms.DateField(
        initial=date.today(),
        widget=forms.DateInput(
            attrs={
                "class": "form-control transactionData", 
                "type": "Date"
            }
        )
    )

    amount=forms.DecimalField(
        initial=0.00,
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control transactionData"
            }
        )
    )

    description=forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control transactionData"
            }
        )
    )

    account=forms.ModelChoiceField(
        queryset=Account.objects.all(),
        widget=forms.Select(
            attrs={
                "class": "form-control transactionData",
            }
        )
    )

class newAccountForm(forms.Form):
    name=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control accountData"
            }
        )
    )

    startingBalance=forms.DecimalField(
        initial=0.00,
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control accountData"
            }
        )
    )

    description=forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control accountData"
            }
        )
    )