# Generated by Django 5.2.1 on 2025-05-28 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_remove_gallery_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='gallery',
            old_name='video',
            new_name='file',
        ),
    ]
