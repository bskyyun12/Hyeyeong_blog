# Generated by Django 2.1.1 on 2018-11-06 22:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('album', '0003_auto_20181026_1019'),
    ]

    operations = [
        migrations.CreateModel(
            name='YunList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=200)),
                ('content', models.CharField(blank=True, max_length=200)),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('check', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sub_content', to='album.YunList')),
            ],
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
