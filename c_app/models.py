from django.db import models

# Create your models here.
class Task(models.Model):
    name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    def __str__(self):
        return self.name