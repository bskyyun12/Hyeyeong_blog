# Generated by Django 2.1.1 on 2018-10-10 23:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0013_remove_notification_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
