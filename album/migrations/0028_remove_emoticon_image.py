# Generated by Django 2.1.1 on 2018-10-02 01:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0027_auto_20181002_0222'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='emoticon',
            name='image',
        ),
    ]
