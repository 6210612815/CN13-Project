from django.db import models
from django import forms
from student.models import Student
from equipment.models import Equipment
from datetime import datetime, timedelta

class Statistic(models.Model):
    item = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    owner = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=True)
    booking_datetime = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    due_datetime = models.DateTimeField(default=datetime.now() + timedelta(days=7))
    return_datetime = models.DateTimeField(default=datetime.now() + timedelta(days=7))

    def __str__(self):
        return self.item


