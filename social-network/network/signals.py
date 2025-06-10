from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import User


@receiver(post_save, sender=User)
def make_first_user_admin(sender, instance, created, **kwargs):
    if created:
        # Only if this is the first real (not bot) user
        if not instance.is_bot and User.objects.filter(is_bot=False).count() == 1:
            instance.is_superuser = True
            instance.is_staff = True
            instance.save(update_fields=["is_superuser", "is_staff"])
