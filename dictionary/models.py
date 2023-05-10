from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=64)
    description = models.TextField(max_length=255, blank=True, null=True)
    wallpaper = models.ImageField(default="wallpaper.svg", upload_to="topic_wallpapers")

class Word(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, default=None)
    spelling = models.CharField(max_length=64)