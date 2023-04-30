from django.db import models
from django import forms
from datetime import datetime, timedelta
from student.models import Student

class Equipment(models.Model):
    CATEGORY = (
            ('Laptops', 'Laptops'),
            ('Mouse', 'Mouse'),
            ('Keyboards', 'Keyboards'),
            ('Monitors', 'Monitors'),
            ('Speaker', 'Speaker'),
            ('Headsets', 'Headsets'),     
    )

    name = models.CharField(max_length=100)
    desc = models.TextField(max_length=1000)
    pic = models.ImageField(upload_to='images/')
    available = models.BooleanField(default=True)
    own = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)
    picked = models.IntegerField(default=0)
    create_datetime = models.DateTimeField(default=datetime.now())
    category = models.CharField(max_length=20, choices=CATEGORY)

    def __str__(self):
        return self.name

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = '__all__'
        labels = {
            'name' : 'Name',
            'desc' : 'Description',
            'pic' : 'Picture',
            'available' : 'Status for booking',
            'own' : 'Owner',
            'picked' : 'Popular variable',
            'create_datetime' : 'Create this item date',
            'category': 'Category',
        }

