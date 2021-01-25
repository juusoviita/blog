from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile
# a signal that gets fired, when an object is saved (i.e. create a profile when a user is created)
# need to also include a receiver for this signal

# creates a Profile every time a new User is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwarks):
    if created:
        Profile.objects.create(user=instance)


# updates an existing profile, when a User updates it
@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwarks):
    instance.profile.save()
