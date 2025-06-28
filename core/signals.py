import os
import zipfile
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Certification
import shutil

@receiver(post_save, sender=Certification)
def unzip_images(sender, instance, **kwargs):
    if not instance.image_zip:
        return

    zip_path = instance.image_zip.path
    extract_path = os.path.join(settings.MEDIA_ROOT, 'pdf_images', instance.slug)

    # Clean previous images if any
    if os.path.exists(extract_path):
        for f in os.listdir(extract_path):
            path = os.path.join(extract_path, f)
            if os.path.isfile(path) or os.path.islink(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
    else:
        os.makedirs(extract_path)

    # Unzip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)
