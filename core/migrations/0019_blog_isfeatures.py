# Generated by Django 5.2.1 on 2025-06-01 09:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_blog_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='blog',
            name='isFeatures',
            field=models.BooleanField(default=False),
        ),
    ]
