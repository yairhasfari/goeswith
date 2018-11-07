from django.contrib import admin
from .models import matches,Object,Rate,AddressRate

# Register your models here.
admin.site.register(Object)
admin.site.register(Rate)
admin.site.register(AddressRate)