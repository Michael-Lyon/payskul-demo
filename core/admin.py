from django.contrib import admin
from . models import *
# Register your models here.
admin.site.register(Service)
admin.site.register(Service_Category)
admin.site.register(Transaction)
admin.site.register(Bank)
admin.site.register(Wallet)
admin.site.register(Loan)
admin.site.register(Card)

