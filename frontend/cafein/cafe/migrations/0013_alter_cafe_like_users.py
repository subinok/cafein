# Generated by Django 3.2 on 2022-12-31 06:45

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cafe', '0012_merge_20221230_1438'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe',
            name='like_users',
            field=models.ManyToManyField(blank=True, related_name='like_users', to=settings.AUTH_USER_MODEL),
        ),
    ]
