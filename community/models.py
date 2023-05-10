from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from datetime import date, timedelta

User._meta.get_field('email')._unique = True
# Create your models here.
class Profile(models.Model):
    # Foreign Key
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    # Identity
    avatar = models.ImageField(default="avatar.jpg", upload_to="profile_avatars")
    bio = models.TextField(blank=True)
    # Attribute
    score = models.IntegerField(default=0)
    streak = models.SmallIntegerField(default=0)
    last_study_date = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        if self.pk:  # instance already exists, check if avatar has changed
            old_profile = Profile.objects.get(pk=self.pk)
            if not self.avatar or self.avatar == old_profile.avatar:
                super().save(*args, **kwargs)
                return
            
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)

    def update_streak(self, tested):
        today = date.today()
        if tested:
            if today - self.last_study_date == timedelta(days=1):
                self.streak += 1
            else:
                self.streak = 1

            self.last_study_date = today
        else:
            if today - self.last_study_date > timedelta(days=1):
                self.streak = 0
        
        self.save()
    
    def update_score(self, score):
        self.score += score + self.streak * 10
        self.save()