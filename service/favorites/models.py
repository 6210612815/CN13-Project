from django.db import models
from equipment.models import Equipment
from student.models import Student

class Favorite(models.Model):
    user = models.ForeignKey(Student, on_delete=models.CASCADE)
    item = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id}"