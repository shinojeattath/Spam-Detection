from django.db import models

# Create your models here.
class User_Detail(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.username
    

class Message(models.Model):
    sender = models.CharField(max_length=100, blank=True, null=True)
    receiver = models.CharField(max_length=100, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_spam = models.BooleanField(default=False, null=True, blank=True)

    def __str__(self):
        return f"{self.sender} to {self.receiver}: {self.content[:30]}"
