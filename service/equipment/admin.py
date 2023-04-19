from django.contrib import admin
from .models import Equipment

# Register your models here.

class EquipmentAdmin(admin.ModelAdmin):
    fields  = ('name', 'desc', 'pic', 'own','available')
    list_display  = ('name', 'desc', 'pic', 'own','available')
    search_fields = ('name', 'own','available')

admin.site.register(Equipment, EquipmentAdmin)
