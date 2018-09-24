# Generated by Django 2.1.1 on 2018-09-23 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0008_remove_calendar_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='post',
        ),
        migrations.AddField(
            model_name='calendar',
            name='tag',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
