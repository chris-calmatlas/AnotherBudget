from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    pass

class AccountAdmin(admin.ModelAdmin):
    pass

class EntityAdmin(admin.ModelAdmin):
    pass

class TransactionAdmin(admin.ModelAdmin):
    pass

class ReminderAdmin(admin.ModelAdmin):
    pass

admin.site.register(User, UserAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(Entity, EntityAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Reminder, ReminderAdmin)
