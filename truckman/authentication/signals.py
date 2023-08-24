from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

#setting the profile photo default to 'default.png'
@receiver(pre_save, sender=CustomUser)
def set_default_profile_photo(sender, instance, **kwargs):
    if not instance.profile_photo:
        instance.profile_photo = 'default.png'
# --ends