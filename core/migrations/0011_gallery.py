# Generated by Django 5.2.1 on 2025-05-28 09:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_certificate'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gallery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.CharField(max_length=124)),
                ('bio', models.CharField(max_length=255)),
                ('image', models.ImageField(max_length=500, upload_to='images/gallery')),
            ],
        ),
    ]
