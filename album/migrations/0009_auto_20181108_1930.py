# Generated by Django 2.1.1 on 2018-11-08 18:30

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0008_auto_20181107_0304'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Image',
            new_name='PostImage',
        ),
    ]