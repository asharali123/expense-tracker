from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=15, blank=True, null=True)
    password = models.CharField(max_length=250)
    
    def __str__(self):
        return self.user.username
