# Generated by Django 2.1.1 on 2018-10-10 22:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0008_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='location_pk',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]