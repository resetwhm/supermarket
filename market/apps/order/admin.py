from django.contrib import admin

# Register your models here.
from order.models import Paymethod


@admin.register(Paymethod)
class PaymethodAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ['pay_name','logo']