from django.db import models
from django import forms

class Student(models.Model):
    userId = models.CharField(max_length=50, unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    sid = models.CharField(max_length=10)
    tel = models.CharField(max_length=10)

    def __str__(self):
        return self.fname

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = '__all__'
        labels = {
            'userId' : 'User Id',
            'fname' : 'First Name',
            'lname' : 'Last Name',
            'email' : 'Email',
            'sid' : 'Student ID',
            'tel' : 'Telephone',
        }