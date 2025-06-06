from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)
    alt_email = models.CharField(max_length=255, blank=True)
    email_chg_time = models.DateTimeField(blank=True, null=True)
    disabled = models.BooleanField(default=False)
    last_ip = models.CharField(max_length=50, blank=True)
    # other fields...

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()