# Generated by Django 2.1.1 on 2018-10-10 03:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0004_auto_20181010_0520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.CharField(max_length=100),
        ),
    ]
