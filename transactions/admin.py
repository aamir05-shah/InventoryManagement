from django.contrib import admin
from .models import TransactionHeader, TransactionItems
# Register your models here.
admin.site.register(TransactionHeader)
admin.site.register(TransactionItems)