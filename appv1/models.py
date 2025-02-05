from django.db import models
import uuid

# Create your models here.
class User(models.Model):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    subject = models.TextField()
    message = models.TextField()

    def __str__(self):
        return self.email