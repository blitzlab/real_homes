from django.contrib import admin
import json
from .models import Property, Gallery
from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields
# Register your models here.
# admin.site.register(Property)
admin.site.register(Gallery)

# admin.site.register(Gallery)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ["address", "category", "type", "price", "city", "published_on"]
    search_fields = ["address", "category", "type", "city"]
    filter_horizontal = ()
    fieldsets = ()

admin.site.register(Property, PropertyAdmin)
