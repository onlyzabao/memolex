from django.db import models
from django.contrib.auth.models import User
from PIL import Image

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

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.avatar.path)
        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.avatar.path)