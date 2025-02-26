import os
from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Item

@receiver(pre_save, sender=Item)
def auto_delete_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return

    try:
        old_item = Item.objects.get(pk=instance.pk)
    except Item.DoesNotExist:
        return

    old_file = old_item.image
    new_file = instance.image

    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)
