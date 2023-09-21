from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Package


@receiver(post_save, sender=Package)
def update_package_time(sender, instance, **kwargs):
    # Update the package time
    package = instance.parent_package
    package.time += instance.time
    package.save()
