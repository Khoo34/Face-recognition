from django.db import models

class Employee(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='faces/')

    def __str__(self):
        return self.name

