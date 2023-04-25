from django.contrib import admin
from .models import Favorite

# Register your models here.

class FavoriteAdmin(admin.ModelAdmin):
    fields  = ('user', 'item', 'date_added')
    list_display  = ('user', 'item', 'date_added')
    search_fields = ('user', 'item', 'date_added')

admin.site.register(Favorite, FavoriteAdmin)
