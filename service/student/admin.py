from django.contrib import admin
from .models import Student

# Register your models here.

class StudentAdmin(admin.ModelAdmin):
    fields  = ('userId', 'fname', 'lname', 'tel', 'email', 'sid')
    list_display  = ('sid', 'fname', 'lname', 'tel', 'userId')
    search_fields = ('sid', 'fname', 'lname', 'email', 'tel')

admin.site.register(Student, StudentAdmin)
