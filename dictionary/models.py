from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class SearchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.CharField(max_length=50)
    search_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} searched for '{self.word}' on {self.search_date}"