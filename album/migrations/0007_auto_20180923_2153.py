# Generated by Django 2.1.1 on 2018-09-23 19:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0006_calendar_tags'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tag',
            old_name='posts',
            new_name='post',
        ),
    ]
