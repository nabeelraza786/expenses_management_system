from django.contrib import admin

# Register your models here.
from .models import Client_details, add_providers_details , Expense , Funds


admin.site.register(Client_details)
admin.site.register(add_providers_details)
admin.site.register(Expense)
admin.site.register(Funds)
