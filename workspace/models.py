from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

User._meta.get_field('email')._unique = True
# Create your models here.
class Package(models.Model):
    # Foreign Key
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    # Identity
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=255, blank=True, null=True)
    # Attribute
    date = models.DateField(blank=True, null=True)
    LEVEL_CHOICES = [
        (0, 'Not started'),
        (1, 'Remembered'),
        (2, 'Understood'),
        (3, 'Applying')
    ]
    level = models.SmallIntegerField(choices=LEVEL_CHOICES, default=0)
    PRIVACY_CHOICES = [
        (0, 'Private'),
        (1, 'Public')
    ]
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)
    
    def __str__(self):
        return self.name
    
    def has_words(self):
        return self.word_set.exists()
    
    def total_words(self):
        return self.word_set.count()

class Word(models.Model):
    # Foreign Key
    package = models.ForeignKey(Package, on_delete=models.CASCADE, default=None)
    # Identity
    spelling = models.CharField(max_length=64)
    # Attribute
    progress = models.SmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])