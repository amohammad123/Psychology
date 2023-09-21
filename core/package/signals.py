from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Package


@receiver(post_save, sender=Package)
def update_package_time(sender, instance, **kwargs):
    # Update the package time
    package = instance.parent_package
    if package:
        package.time += instance.time
        package.save()


@receiver(pre_save, sender=Package)
def set_category_from_parent(sender, instance, **kwargs):
    if not instance.category.exists() and instance.parent_package.category:
        instance.category.set(instance.parent_package.category)
