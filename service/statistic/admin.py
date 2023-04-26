from django.contrib import admin
from .models import Statistic

# Register your models here.

class StatisticAdmin(admin.ModelAdmin):
    fields  = ('item', 'owner', 'booking_datetime', 'due_datetime','return_datetime')
    list_display  = ('item', 'owner', 'booking_datetime', 'due_datetime','return_datetime')
    search_fields = ('item', 'owner', 'booking_datetime', 'due_datetime','return_datetime')

admin.site.register(Statistic, StatisticAdmin)




