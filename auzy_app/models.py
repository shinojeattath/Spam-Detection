from django.db import models

# Create your models here.
class User_Detail(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.username