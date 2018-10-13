# Generated by Django 2.1.1 on 2018-10-11 17:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('album', '0016_remove_notification_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='image_comment',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='image_comments_notification', to='album.ImageComment'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='post_comment',
            field=models.ForeignKey(blank=True, default=1, on_delete=django.db.models.deletion.CASCADE, related_name='post_comments_notification', to='album.Comment'),
            preserve_default=False,
        ),
    ]