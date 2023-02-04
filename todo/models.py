from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from datetime import timezone

# Create your models here.
def validate_date(value):
    if value < timezone.now():
        raise ValidationError("Completion Date cannot be in the past")
    
class Todo(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=225)
    created = models.DateTimeField(auto_now_add=True)
    completiondate = models.DateField(validators=[validate_date])
    completed = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    