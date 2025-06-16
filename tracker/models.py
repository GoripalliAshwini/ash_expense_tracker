from django.db import models
from django.contrib.auth.models import User

class Transaction(models.Model):
    Amount = models.IntegerField()
    Description= models.CharField(max_length=100)
    Type = models.CharField(
        max_length=100,
        choices=(("Income", "Income"), ("Expense", "Expense"))
    )
    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Travel', 'Travel'),
        ('Shopping', 'Shopping'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other'),
    ]
    Category= models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='Other')
    Date = models.DateField()
    def __str__(self) -> str:
        return f"The amount is {self.Amount} and the type is {self.Type} and the category is {self.Category} and the date is {self.Date}"
    
class RequestLogs(models.Model):
    request_info= models.TextField()
    request_type= models.CharField(max_length=20)
    request_method= models.CharField(max_length=50)
    created_at= models.DateTimeField(auto_now_add=True)