# Generated by Django 3.2 on 2022-12-23 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafe', '0002_remove_cafe_review_review_id2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cafe_comment',
            name='content',
            field=models.TextField(verbose_name='리뷰내용'),
        ),
        migrations.AlterField(
            model_name='cafe_review',
            name='content',
            field=models.TextField(verbose_name='리뷰내용'),
        ),
    ]
