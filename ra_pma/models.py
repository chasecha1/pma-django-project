from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_RA = models.BooleanField(default=False)
    is_SR = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    background_color = models.CharField(max_length=7, default='#FFFFFF')
    def __str__(self) -> str:
        return self.user.username
    

# Signal to create or update UserProfile when User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    # Use get_or_create to ensure the profile exists for every user
    UserProfile.objects.get_or_create(user=instance)
