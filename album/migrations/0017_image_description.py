# Generated by Django 2.1.1 on 2018-09-29 02:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0016_auto_20180928_0243'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
