from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class HelpRequest(models.Model):
    User = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50) 
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=200)

class Reply(models.Model):
    help_request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE, related_name='replies')
    responder = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
class Skill(models.Model):
    name = models.CharField(max_length=100)
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subjects = models.TextField(blank=True)
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    request = models.ForeignKey(HelpRequest, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
