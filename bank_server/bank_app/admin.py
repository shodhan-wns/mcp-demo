from django.contrib import admin
from .models import Person, BankAccount, Transaction

admin.site.register(Person)
admin.site.register(BankAccount)
admin.site.register(Transaction)