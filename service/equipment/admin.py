from django.contrib import admin
from .models import Equipment

# Register your models here.

class EquipmentAdmin(admin.ModelAdmin):
    fields  = ('name', 'desc', 'pic', 'own', 'available', 'picked', 'category')
    list_display  = ('id', 'name', 'own', 'available', 'create_datetime', 'picked', 'category')
    search_fields = ('name', 'own', 'available', 'create_datetime', 'picked', 'category')

admin.site.register(Equipment, EquipmentAdmin)
