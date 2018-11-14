from django.contrib import admin
from .models import Object,Rate,ClientRate

def approve(modeladmin, request, queryset):
    for rate in queryset:
        rate.approved = True
        rate.save()
approve.short_description = 'Approve Selected'
def disapprove(modeladmin, request, queryset):
    for rate in queryset:
        rate.approved = False
        rate.save()
disapprove.short_description = 'Disapprove Selected'
class RateAdmin(admin.ModelAdmin):
    list_display = ['object1', 'object2','approved','modified',]
    actions = [approve, disapprove,]  # <-- Add the list action function here
# Register your models here.
admin.site.register(Object)
admin.site.register(Rate,RateAdmin)
admin.site.register(ClientRate)
