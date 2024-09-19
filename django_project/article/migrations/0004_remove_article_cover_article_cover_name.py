# Generated by Django 4.2 on 2024-09-15 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0003_article_cover_alter_article_content'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='cover',
        ),
        migrations.AddField(
            model_name='article',
            name='cover_name',
            field=models.CharField(max_length=120, null=True),
        ),
    ]