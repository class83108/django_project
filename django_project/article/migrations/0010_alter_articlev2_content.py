# Generated by Django 4.2 on 2024-09-20 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0009_alter_article_content_alter_articlev2_content'),
    ]

    operations = [
        migrations.AlterField(
            model_name='articlev2',
            name='content',
            field=models.JSONField(default=dict, verbose_name='內容'),
        ),
    ]
