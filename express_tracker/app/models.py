from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses', null=True, blank=True)
    amount = models.IntegerField()
    category = models.CharField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    desc = models.TextField()  

    def __str__(self):
        return f"{self.amount} - {self.category} - {self.date.strftime('%Y-%m-%d')} - {self.desc}"

    
