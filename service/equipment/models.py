from django.db import models
from django import forms
from student.models import Student

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
    pic = models.ImageField(upload_to='images/')
    available = models.BooleanField(default=True)
    own = models.ForeignKey(Student, on_delete=models.SET_NULL, blank=True, null=True)

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
        }

