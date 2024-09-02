from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class User(AbstractUser):
    username = models.EmailField(unique=True)
    email = models.EmailField(unique=True)

class Account(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    description = models.CharField(max_length=64, default="")
    startingBalance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    currentBalance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    modifiedOn = models.DateTimeField(auto_now=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_account_name'),
        ]

    def __str__(self):
        return f"{self.name} ({self.currentBalance})"
    
class Entity(models.Model):
    name = models.CharField(max_length=64)
    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    modifiedOn = models.DateTimeField(auto_now=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'owner'], name='unique_entity_name'),
        ]

class Transaction(models.Model):
    description = models.CharField(max_length=64, default="")
    account = models.ForeignKey('Account', on_delete=models.RESTRICT, related_name="transactions")
    entity = models.ForeignKey('Entity', null=True, on_delete=models.SET_NULL)
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    isIncome = models.BooleanField(default='False')
    date = models.DateField(default=date.today)

    owner = models.ForeignKey('User', on_delete=models.CASCADE)
    modifiedOn = models.DateTimeField(auto_now=True)
    createdOn = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['createdOn', 'owner'], name='one_transactions_at_a_time'),
        ]
    
    def __str__(self):
        if self.isIncome == True:
            return f"{self.amount} to ({self.account.name})"
        else:
            return f"{self.amount} from ({self.account.name})"
        
    def save(self, **kwargs):
        # update account currentBalance
        # TODO: error checking account updated correctly
        if self.isIncome == True:
            self.account.currentBalance += self.amount
        else:
            self.account.currentBalance -= self.amount
        self.account.save()

        super().save(**kwargs)

    def delete(self, **kwargs):
        # update account currentBalance
        # TODO: error checking account updated correctly
        if self.isIncome == True:
            self.account.currentBalance -= self.amount
        else:
            self.account.currentBalance += self.amount
        self.account.save()

        super().delete(**kwargs)
        
class Reminder(Transaction):
    startDate = models.DateTimeField(null=True)
    endDate = models.DateTimeField(null=True)
    quantity = models.IntegerField(null=True)
    
    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(endDate__isnull=True, quantity__isnull=False) | models.Q(endDate__isnull=False, quantity__isnull=True), name='endDate_or_quantity'),
        ]