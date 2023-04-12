from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.
class Package(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Identity
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=255, blank=True, null=True)
    # Attribute
    progress = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    PRIVACY_CHOICES = [
        (0, 'Private'),
        (1, 'Public')
    ]
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)
    
    def __str__(self):
        return self.name

class Word(models.Model):
    # Foreign Key
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    # Identity
    word = models.CharField(max_length=64)