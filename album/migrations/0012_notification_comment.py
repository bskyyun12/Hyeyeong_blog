# Generated by Django 2.1.1 on 2018-10-10 22:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0011_auto_20181011_0027'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='comment',
            field=models.CharField(default=123, max_length=200),
            preserve_default=False,
        ),
    ]
