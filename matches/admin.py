from django.contrib import admin
from .models import Object,Rate,ClientRate,Category

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
def categorize(modeladmin, request, queryset):
    for o in queryset:
        o.category = 4
        o.save()
categorize.short_description = 'Generalize Selected'
class RateAdmin(admin.ModelAdmin):
    list_display = ['object1', 'object2','approved','modified',]
    actions = [approve, disapprove,]  # <-- Add the list action function here
# Register your models here.
class ObjectAdmin(admin.ModelAdmin):
    list_display=['name']
    actions=[categorize,]
admin.site.register(Object,ObjectAdmin)
admin.site.register(Rate,RateAdmin)
admin.site.register(ClientRate)
admin.site.register(Category)
