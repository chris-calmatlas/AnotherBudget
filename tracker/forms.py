from django import forms

class newTransaction(forms.Form):
    date=forms.DateField(
        widget=forms.DateInput(
            attrs={
                "required": True,
                "class": "transactionData"
            }
        )
    )

    amount=forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "required": True,
                "class": "transactionData"
            }
        )
    )

    description=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "transactionData"
            }
        )
    )

class newAccount(forms.Form):
    Name=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "accountData"
            }
        )
    )

    startingBalance=forms.DecimalField(
        max_digits=14,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "required": True,
                "class": "accountData"
            }
        )
    )

    description=forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "accountData"
            }
        )
    )