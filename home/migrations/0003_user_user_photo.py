# Generated by Django 2.1.1 on 2018-11-09 03:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_auto_20181107_1607'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_photo',
            field=models.CharField(default=django.utils.timezone.now, max_length=50),
            preserve_default=False,
        ),
    ]