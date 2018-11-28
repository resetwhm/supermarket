from django.contrib import admin

from person.models import Address


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_per_page = 3
    list_display = ["name", "tel", 'hcity', 'hproper', 'harea', 'brief', 'isDefault']
