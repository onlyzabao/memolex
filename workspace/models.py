from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Word(models.Model):
    word = models.CharField(max_length=50)
    uuid = models.CharField(max_length=50)
    sn = models.CharField(max_length=10)

class Package(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    PRIVACY_CHOICES = [
        (0, 'Private'),
        (1, 'Public')
    ]
    privacy = models.SmallIntegerField(choices=PRIVACY_CHOICES, default=1)

class User_Package(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    progress = models.SmallIntegerField()
    STAR_CHOICES = [
        (0, 'Not started'),
        (1, 'Remembered'),
        (2, 'Understood'),
        (3, 'Applying')
    ]
    star = models.SmallIntegerField(choices=STAR_CHOICES, default=0)

class Word_Package(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.RESTRICT)